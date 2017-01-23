from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from model.model import connect_to_db, db
from model.user import User
from model.pet import Pet, PetUser
from model.activity import Activity
from model.entry import Entry
from datetime import datetime

app = Flask(__name__)
app.secret_key = '\x7f\xebu\xc2\xef\x1a\xdf\x95%\x87{h]\xc2\x8b\x94\xad\xfd7\xdf\tb\x869'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    """Displays homepage."""

    user = None
    try:
        if session['user_id']:
            user = User.query.get(session['user_id'])
    except KeyError:
        "No user is logged in."

    return render_template('cover.html', user=user)


@app.route('/about')
def show_about_page():
    """Displays about page. """

    return render_template('about.html')


@app.route('/<username>')
def show_profile(username):
    """Displays a user's profile. """

    current_user = User.get_user_by_user_id(session['user_id'])

    if current_user:
        if current_user.username == username:
            pets = current_user.get_all_pets()
            return render_template('user.html', current_user=current_user, pets=pets)
        else:
            flash("I'm sorry, you're not signed in as that user.")
            return redirect('/{}'.format(current_user.username))
    else:
        flash("Please login to see your user profile.")
        return redirect('/')


@app.route('/<username>/<first_name>-<last_name>')
def show_pet(username, first_name, last_name):
    """Displays a pet's profile. """

    period = request.args.get('period')
    print 'PERIOD: ', period
    current_user = User.get_user_by_user_id(session['user_id'])
    current_pet = Pet.get_pet_by_name_and_user(current_user, first_name, last_name)
    activities = Activity.get_all_activities()
    entries = Entry.find_entries(current_pet, period)
    stats = Entry.compile_stats(current_pet)

    return render_template('pet.html', pet=current_pet, entries=entries, user=current_user, activities=activities, period=period, stats=stats)


# --------------------------- RETREIVING CHART DATA -----------------------------

@app.route('/chart_data.json')
def get_chart_data():

    first_name = request.args.get('pet_fname')
    last_name = request.args.get('pet_lname')
    print 'NAME:', first_name, last_name
    current_user = User.get_user_by_user_id(session['user_id'])
    current_pet = Pet.get_pet_by_name_and_user(current_user, first_name, last_name)
    print 'CURRENT PET', current_pet

    chart_data = Entry.compile_chart_data(current_pet)

    return jsonify(chart_data)

# --------------------------- ADDING INSTANCES TO DB -----------------------------


@app.route('/add_entry', methods=['POST'])
def add_new_entry():
    """Adds new entry from form on pet's profile. """

    activity_id = request.form.get('activity').encode('latin-1')
    pet_id = request.form.get('pet_id').encode('latin-1')
    pet = Pet.query.get(pet_id)
    user_id = session['user_id']
    user = User.query.get(user_id)
    occurred_at = datetime.now()
    logged_at = datetime.now()

    entry = Entry.add_new_entry_to_db(user_id, pet_id, activity_id, occurred_at, logged_at)

    return redirect('/{}/{}-{}'.format(user.username, pet.first_name, pet.last_name))


@app.route('/add_pet', methods=['POST'])
def add_new_pet():
    """Adds new pet to the db and creates PetUser association."""

    first_name = request.form.get('fname')
    animal = request.form.get('animal')
    breed = request.form.get('breed')
    dob = request.form.get('dob')
    role = request.form.get('role')

    current_user = User.query.get(session['user_id'])
    last_name = current_user.last_name

    pet = Pet.add_new_pet_to_db(first_name, last_name, animal, breed, dob)
    pet_user = PetUser.add_new_pet_user_connection(current_user.user_id, pet.pet_id, role)
    return redirect('/{}/{}-{}'.format(current_user.username, pet.first_name, pet.last_name))


# MAY WANT THIS TO BE SPLIT OUT TO A SEPARATE DB TABLE WITH ADDITIONAL FIELD FOR
# FORIEGN KEY TO APPLICABLE PET. DEPENDS ON IT WE WANT CUSTOM BUILT ACTIVITIES TO
# BE ACCESSIBLE MORE GLOBALLY?
@app.route('/add_activity', methods=['POST'])
def add_new_activity():
    """Adds new custom activity."""

    activity = request.form.get('activity')
    minimum = request.form.get('minimum')
    maximum = request.form.get('maximum')
    time_period = request.form.get('time_period')

    current_user = User.query.get(session['user_id'])
    pet_id = request.form.get('pet_id')
    pet = Pet.query.get(pet_id)

    activity = Activity.add_new_activity_to_db(activity, minimum, maximum, time_period)
    return redirect('/{}/{}-{}'.format(current_user.username, pet.first_name, pet.last_name))


# --------------------------- PROFILE REGISTRATION -----------------------------


@app.route('/signup', methods=['GET'])
def get_signup_form():
    """Displays signup page for a new user."""

    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def process_signup():
    """Processes signup page form input to add a new user to the db. """

    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    # profile_img = session['img_upload_filepath']

    emails = db.session.query(User.email).all()

    if email in emails:
        flash("You already have an account. Please sign in.")
        session['img_upload_filepath'] = None
        return redirect('/#login')

    else:
        user = User.add_new_user_to_db(first_name, last_name, username, email, password)
        flash("Thank you for signing up for an account.")
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['img_upload_filepath'] = None

        return redirect('/{}'.format(user.username))

# ------------------------------- LOGGING IN/OUT -------------------------------


# ADDING BACK LOGIN TEMPLATE FOR WHEN LOGIN IS UNSUCCESSFUL
@app.route('/login', methods=['GET'])
def shows_login():
    """Displays login page for an existing user."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def process_login():
    """Processes login form input to validate a user login."""

    email = request.form.get('email')
    password = request.form.get('password')

    user_query = User.query.filter_by(email=email)
    try:
        user = user_query.one()
    except NoResultFound:
        print "No user instance found for this email in db."
        user = None
    except MultipleResultsFound:
        print "Multiple user instances found for this email in db."
        user = user_query.first()

    if user:
        if user.password == password:
            flash("You've successfully logged in!")
            session['user_id'] = user.user_id
            session['username'] = user.username
            return redirect('/{}'.format(user.username))
        else:
            flash("I'm sorry that password is incorrect. Please try again.")
            return redirect('/login')

    else:
        flash("""I'm sorry that email is not in our system. Please try again
                or go to our registration page to create a new account.""")
        return redirect('/login')


@app.route('/logout')
def processes_logout():
    """Processes a user logging out and resets any associated session keys."""

    session['user_id'] = None
    session['username'] = None
    flash("You've successfully logged out!")
    return redirect('/')

# ------------------------------ STARTING SERVER -------------------------------
if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    # app.run(host='127.0.0.1')
