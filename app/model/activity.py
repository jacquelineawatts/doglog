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
    time_period = db.Column(db.String(30), nullable=True)  # if null, defaults to daily

    def __repr__(self):
        return "<Activity: {} {}>".format(self.activity_id,
                                          self.activity,
                                          )

    @classmethod
    def add_new_activity_to_db(cls, activity, minimum, maximum, time_period):

        try:
            minimum = int(minimum)
        except ValueError:
            minimum = None

        try:
            maximum = int(maximum)
        except ValueError:
            maximum = None

         # BY LEGACY THESE ARE CALLED MIN AND MAX DAILY, BUT NOW THESE FIELDS CAN
        # HOLD MIN/MAX OF ANY SELECTED TIME PERIOD.
        activity = Activity(activity=activity,
                            min_daily=minimum,
                            max_daily=maximum,
                            time_period=time_period
                            )

        db.session.add(activity)
        db.session.commit()

        print 'Added new activity to DB.'
        return activity

    @classmethod
    def get_all_activities(cls):

        activities = Activity.query.all()

        return activities


if __name__ == '__main__':

    from server import app

    connect_to_db(app)
    print "Connected to DB."

    db.create_all()
