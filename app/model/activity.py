from model import connect_to_db, db
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import flash


class Activity(db.Model):
    """Class for pet's activities."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity = db.Column(db.String(30))
    min_daily = db.Column(db.Integer, nullable=True)
    max_daily = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "<Activity: {} {}>".format(self.activity_id,
                                          self.name,
                                          )

    @classmethod
    def add_new_activity_to_db(cls, activity, min_daily, max_daily):

        activity = Activity(activity=activity,
                            min_daily=min_daily,
                            max_daily=max_daily,
                            )

        db.session.add(activity)
        db.session.commit()

        return activity
