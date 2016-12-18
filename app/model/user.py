from model import connect_to_db, db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import flash


class User(db.Model):
    """Class for users"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    profile_img = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.Datetime)

    def __repr__(self):
        return "<User: {} {} {} Email: {}>".format(self.user_id,
                                                   self.first_name,
                                                   self.last_name,
                                                   self.email,
                                                   )

    @classmethod
    def add_new_user_to_db(cls, first_name, last_name, title, email, password, profile_img=None):
        """Creates a new user instance in the db. """

        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    profile_img=profile_img,
                    )

        db.session.add(user)
        db.session.commit()

        return user
