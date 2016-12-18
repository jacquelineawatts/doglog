from model import connect_to_db, db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import flash

class Pet(db.Model):
    """Class for pets"""

    __tablename__ = "pets"

    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    animal = db.Column(db.String(30), nullable=False)
    breed = db.Column(db.String(30), nullable=True)
    birthdate = db.Column(db.DateTime, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    profile_img = db.Column(db.String(256), nullable=True)

    users = db.relationship('User',
                            secondary="pets_users",
                            backref="pets")

    def __repr__(self):
        return "<Pet: {} {} {}>".format(self.pet_id,
                                        self.first_name,
                                        self.last_name,
                                        )

    @classmethod
    def add_new_pet_to_db(cls, first_name, last_name, animal, breed, birthdate, profile_img=None):
        """Adds a new pet instance to the db. """

        pet = Pet(first_name=first_name,
                  last_name=last_name,
                  animal=animal,
                  breed=breed,
                  birthdate=birthdate,
                  profile_img=profile_img,
                  )

        db.session.add(pet)
        db.session.commit()

        return pet


class PetUser(db.Model):
    """Class for association table between users and pets."""

    __tablename__ = "pets_users"

    petuser_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'), nullable=False)
    role = db.Column(db.String(30), nullable=False)

    user = db.relationship('User', backref='pets_users')
    pet = db.relationship('Pet', backref='pets_users')

    def __repr__(self):
        return "<Pet ID: {}, User ID: {}>".format(self.pet_id,
                                                  self.user_id,
                                                  )

    @classmethod
    def add_new_pet_user_connection(cls, user_id, pet_id, role):
        """Creates new connection between user and pet."""

        pet_user = PetUser(user_id=user_id,
                           pet_id=pet_id,
                           role=role
                           )

        db.session.add(pet_user)
        db.session.commit()

        return pet_user
