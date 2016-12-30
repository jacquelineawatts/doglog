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

    @staticmethod
    def build_empty_dict():

        # Establish dict of chart data, keys are time slots per 1/2 hr and all activites.
        histogram_dict = {}
        hour_slots = [x/10.0 for x in range(0, 240, 5)]

        activities = Activity.get_all_activities()
        possible_activities = [activity.activity_id for activity in activities]

        for slot in hour_slots:
            histogram_dict[slot] = {}
            for activity in possible_activities:
                histogram_dict[slot][activity] = 0

        return histogram_dict

    @classmethod
    def compile_chart_data(cls, pet):
        """Get data for ChartJS chart on pets page. """

        histogram_dict = Entry.build_empty_dict()
        entries = Entry.get_all_entries(pet)

        for entry in entries:
            entry_time = entry.occurred_at.hour
            if entry.occurred_at.minute >= 30:
                entry_time += 0.5
            histogram_dict[entry_time][entry.activity_id] += 1

        no_1 = [(key, value[1]) for key, value in sorted(histogram_dict.iteritems())]
        print 'NO 1 LIST: ', no_1
        no_2 = [(key, value[2]) for key, value in histogram_dict.iteritems()]
        print 'NO 2 LIST: ', no_2
        no_3 = [(key, value[3]) for key, value in histogram_dict.iteritems()]
        print 'NO 3 LIST: ', no_3

        chart_data = {"labels": [x/10.0 for x in range(0, 240, 5)],
                      "datasets": [
                                  {"data": [value[1] for key, value in sorted(histogram_dict.iteritems())],
                                   "backgroundColor": '#ff9900',
                                   "hoverBackgroundColor": '#ffd699',
                                   "label": "No 1",
                                    },
                                  {"data": [value[2] for key, value in sorted(histogram_dict.iteritems())],
                                   "backgroundColor": '#0066ff',
                                   "hoverBackgroundColor": '#99c2ff',
                                   "label": "No 2",
                                    },
                                  {"data": [value[3] for key, value in sorted(histogram_dict.iteritems())],
                                   "backgroundColor": '#339966',
                                   "hoverBackgroundColor": '#9fdfbf',
                                   "label": "Food",
                                    }, ]
                      }

        return chart_data


if __name__ == '__main__':

    from server import app

    connect_to_db(app)
    print "Connected to DB."

    db.create_all()
