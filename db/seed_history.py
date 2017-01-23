"""All information seeded from doglog_seed_data.csv. Exported from Andrew's excel file.
Unknowns were assigned to jacqui to have enough seed data for testing.

All data has been backed up in doglog_db.sql file. But if this script needs to be
run again, must place this script next to server, seed data, and model files."""


from model import connect_to_db, db
from user import User
from entry import Entry
from datetime import datetime


def add_entries_to_db(all_entries):
    """Adds entries to db."""

    for entry in all_entries:
        timestamp = entry[0].split(' ')
        date = timestamp[0].split('/')
        time = timestamp[1].split(':')

        occurred_at = datetime(int(date[2]) + 2000, int(date[0]), int(date[1]), int(time[0]), int(time[1]))
        user = User.get_user_by_username(entry[2])
        Entry.add_new_entry_to_db(user.user_id, 1, entry[1], occurred_at, occurred_at)


def clean_entries(entries):
    """Cleans up entries by resolving username, activity ID, and dual entries."""

    all_entries = []
    usernames = {'Pam': 'pam',
                 'Andrew': 'andrew',
                 'Tom': 'tom',
                 'Guest': 'jacqui',
                 'Unknown': 'jacqui'
                 }
    for entry in entries:
        full_entry = entry.rstrip().split(',')
        timestamp = full_entry[0]
        no_1 = full_entry[3]
        no_2 = full_entry[4]
        food = full_entry[5]
        logger = full_entry[6]

        if no_1 == '1':
            all_entries.append([timestamp, 1, usernames[logger]])
        if no_2 == '1':
            all_entries.append([timestamp, 2, usernames[logger]])
        if food == '1':
            all_entries.append([timestamp, 3, usernames[logger]])

    return all_entries


def open_and_read_file(filename):
    """Takes file path; returns text as list of strings.
    """

    file_text = open(filename).read()
    entries = file_text.rstrip().split('\r')
    return entries


if __name__ == '__main__':

    from server import app

    connect_to_db(app)
    print "Connected to DB."

    entries = open_and_read_file('doglog_seed_data.csv')
    all_entries = clean_entries(entries)
    add_entries_to_db(all_entries)
