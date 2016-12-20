from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from model.model import connect_to_db, db
from model.user import User
from model.pet import Pet, PetUser
from model.activity import Activity
from model.entry import Entry


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


@app.route('/profile/<username>')
def show_profile(username):
    """Displays a user's profile. """

    current_user = User.get_user_by_username(username)

    return render_template('profile.html', current_user=current_user)


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
    profile_img = session['img_upload_filepath']

    emails = db.session.query(User.email).all()

    if email in emails:
        flash("You already have an account. Please sign in.")
        session['img_upload_filepath'] = None
        return redirect('/#login')

    else:
        user = User.add_user_to_db(email, password, first_name, last_name, username, profile_img)
        flash("Thank you for signing up for an account.")
        session['user_id'] = user.user_id
        session['img_upload_filepath'] = None

        return redirect('/user/{}'.format(user.username))

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
            return redirect('/user/{}'.format(user.username))
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
    # DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(host='127.0.0.1')
