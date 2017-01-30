from model import connect_to_db, db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import flash
from user import User

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

    @classmethod
    def get_pet_by_id(cls, pet_id):
        """Given a pet_id, returns the pet object. """

        try:
            return Pet.query.filter_by(pet_id=pet_id).one()

        except NoResultFound:
            return None

        except MultipleResultsFound:
            return None

    @classmethod
    def get_pets_by_user(cls, user_id):
        """Given a users id, returns the associated pets. """

        try:
            return Pet.query.filter_by(user_id=user_id).all()

        except NoResultFound:
            return None

    @classmethod
    def get_pet_by_name_and_user(cls, user, first_name, last_name):
        """Given a user and the pets name, return pet object."""

        current_pet = None
        all_pets = user.get_all_pets()
        for pet in all_pets:
            if (pet.first_name == first_name) and (pet.last_name == last_name):
                current_pet = pet
            else:
                continue
        return current_pet

    def compile_stats(self):

        sql_query = "SELECT AVG(daily_count) \
                    FROM (\
                        SELECT activity_id, \
                                COUNT(*) AS daily_count, \
                                EXTRACT(DAY FROM occurred_at) AS day, \
                                EXTRACT(MONTH FROM occurred_at) AS month \
                        FROM entries \
                        WHERE (pet_id = :pet_id) and \
                              (occurred_at - now() < interval '1 year') \
                              (activity_id = :activity_id) \
                        GROUP BY activity_id, month, day \
                        ORDER BY activity_id, month, day \
                    ) AS activity_query"

        stats = {}
        for activity_id in range(5):
            cursor = db.session.execute(sql_query, {'pet_id': self.id, 'activity_id': activity_id})
            avg = cursor.fetchone()
            stats[activity_id] = avg

        return stats


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

        print 'Added new pet to DB.'
        return pet_user


if __name__ == '__main__':

    from server import app

    connect_to_db(app)
    print "Connected to DB."

    db.create_all()

