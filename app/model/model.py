from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app, db_uri="postgresql:///doglog"):
    """Connect application to the db."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == '__main__':

    from app.server import app

    connect_to_db(app)
    print "Connected to DB."

    db.create_all()
