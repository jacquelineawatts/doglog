from flask.ext.sqlalchemy import SQLAlchemy
import os
import psycopg2
import urlparse

db = SQLAlchemy()

urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])


def connect_to_db(app, db_uri="postgresql:///doglog"):
    """Connect application to the db."""

    # conn = psycopg2.connect(database=url.path[1:],
    #                         user=url.username,
    #                         password=url.password,
    #                         host=url.hostname,
    #                         port=url.port
    #                         )

    # ----- CONNECTING TO LOCAL DB: ----------

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == '__main__':

    from server import app

    connect_to_db(app)
    print "Connected to DB."


