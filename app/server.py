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


# ------------------------------ STARTING SERVER -------------------------------
if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    # DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(host='127.0.0.1')
