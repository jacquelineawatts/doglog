from model import connect_to_db, db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import flash
from activity import Activity
from user import User
from pet import Pet

class Entry(db.Model):
    """Class for activity instance."""

    __tablename__ = "entries"

    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.pet_id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id'), nullable=False)
    occurred_at = db.Column(db.DateTime, nullable=False)
    logged_at = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref='entries')
    pet = db.relationship('Pet', backref='entries')
    activity = db.relationship('Activity', backref="entries")

    def __repr__(self):
        return "<User: {}, Pet: {}, Activity: {}>".format(self.user_id,
                                                          self.pet_id,
                                                          self.activity_id,
                                                          )

    @classmethod
    def add_new_entry_to_db(cls, user_id, pet_id, activity_id, occurred_at, logged_at, notes=None):

        entry = Entry(user_id=user_id,
                      pet_id=pet_id,
                      activity_id=activity_id,
                      occurred_at=occurred_at,
                      logged_at=logged_at,
                      notes=notes,
                      )

        db.session.add(entry)
        db.session.commit()

        return entry

    @classmethod
    def get_all_entries(cls, pet):

        try:
            return Entry.query.filter_by(pet_id=pet.pet_id).all()

        except NoResultFound:
            return None


if __name__ == '__main__':

    from server import app

    connect_to_db(app)
    print "Connected to DB."

    db.create_all()
