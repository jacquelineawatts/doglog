from model import connect_to_db, db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import flash
from activity import Activity
from user import User
from pet import Pet
from datetime import date, time, datetime, timedelta

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

        print 'Added new entry to DB.'
        return entry

    @classmethod
    def get_all_entries(cls, pet):

        try:
            return Entry.query.filter_by(pet_id=pet.pet_id).all()

        except NoResultFound:
            return None

    @classmethod
    def get_entry_segment(cls, pet, period):

        start_time = time.min
        end_time = time.max
        today = datetime.today()

        if period == 'today' or period is None:
            start_date = datetime.combine(today, start_time)
            end_date = datetime.combine(today, end_time)
        elif period == 'week':
            end_date = datetime.combine(today, end_time)
            start_date = end_date - timedelta(days=7)

        try:
            return Entry.query.filter(Entry.pet_id == pet.pet_id, Entry.logged_at >= start_date, Entry.logged_at <= end_date).all()

        except NoResultFound:
            return None

    @classmethod
    def find_entries(cls, current_pet, period):
        """Find entries by time period selected."""

        if period == 'all':
            entries = Entry.get_all_entries(current_pet)
        elif period == 'custom':
        # Find a good date picker library for here.
            entries = None
        else:
            entries = Entry.get_entry_segment(current_pet, period)

        return entries

    @classmethod
    def get_chart_data(cls, pet):
        """Get data for ChartJS chart on pets page. """

        entries = Entry.get_all_entries(pet)
        no_1, no_2, food, walk, meds, litter_change = [], [], [], [], [], []

        for entry in entries:
            for activity in [no_1, no_2, food, walk, meds, litter_change]:
                if entry.activity_id.activity == activity:
                    entry_time = entry.occurred_at.hour
                    if entry.occurred_at.minute >= 30:
                        entry_time += 0.5
                    activity.append(entry_time)
        print 'NO 1', no_1
        print 'NO 2', no_2

        chart_data = {"datasets": [{"data": [],
                                    # "backgroundColor": ['#ff9900', '#ff9900', '#ff9900'],
                                    # "hoverBackgroundColor": ['#ffd699', '#ffd699', '#ffd699'],
                                    # "label": "Notes Only",
                                    }],
                      }

        return chart_data


if __name__ == '__main__':

    from server import app

    connect_to_db(app)
    print "Connected to DB."

    db.create_all()
