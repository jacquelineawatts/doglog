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

    return render_template('cover.html')


@app.route('/about')
def show_about_page():
    """Displays about page. """

    return render_template('about.html')


@app.route('/<username>')
def show_profile(username):
    """Displays a user's profile. """

    current_user = User.get_user_by_user_id(session['user_id'])
    pets = current_user.get_all_pets()

    return render_template('user.html', current_user=current_user, pets=pets)


@app.route('/<username>/<first_name>-<last_name>')
def show_pet(username, first_name, last_name):
    """Displays a pet's profile. """

    print 'UN: ', username
    print 'FN: ', first_name
    print 'LN: ', last_name
    current_user = User.get_user_by_user_id(session['user_id'])
    print 'CU:', current_user
    current_pet = Pet.get_pet_by_name_and_user(current_user, first_name, last_name)
    activities = Activity.get_all_activities()
    print 'CURRENT PET: ', current_pet
    entries = Entry.get_all_entries(current_pet)

    return render_template('pet.html', pet=current_pet, entries=entries, user=current_user, activities=activities)


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
        user = User.add_user_to_db(email, password, first_name, last_name, username, profile_img)
        flash("Thank you for signing up for an account.")
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['img_upload_filepath'] = None

        return redirect('/{}'.format(user.username))

# ------------------------------- LOGGING IN/OUT -------------------------------


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
    flash("You've successfully logged out!")
    return redirect('/')

# ------------------------------ STARTING SERVER -------------------------------
if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(host='127.0.0.1')
