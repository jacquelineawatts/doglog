from model import connect_to_db, db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import flash


class User(db.Model):
    """Class for users"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    profile_img = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return "<User: {} {} {} Email: {}>".format(self.user_id,
                                                   self.first_name,
                                                   self.last_name,
                                                   self.email,
                                                   )

    @classmethod
    def add_new_user_to_db(cls, first_name, last_name, username, email, password, profile_img=None):
        """Creates a new user instance in the db. """

        user = User(first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                    profile_img=profile_img,
                    )

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def get_user_by_user_id(cls, user_id):
        """Given user id, returns the user object. """

        try:
            return User.query.filter_by(user_id=user_id).one()

        except NoResultFound:
            return None

        except MultipleResultsFound:
            return None

    def get_all_pets(self):
        """Given a user, see all associated pets. """

        pets = [user_pet.pet for user_pet in self.pets_users]
        return pets


if __name__ == '__main__':

    from server import app

    connect_to_db(app)
    print "Connected to DB."

    db.create_all()

