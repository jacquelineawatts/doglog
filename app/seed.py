from model.model import connect_to_db, db
from model.user import User
from model.pet import Pet, PetUser
from model.activity import Activity


def load_seed_users_and_pets():
    """Sample users."""

    jacqui = User.add_new_user_to_db(first_name='Jacqui',
                                     last_name='Watts',
                                     username='jacquelineawatts',
                                     email='jacqui@test.org',
                                     password='test',
                                     profile_img=None)

    pam = User.add_new_user_to_db(first_name='Pam',
                                  last_name='Watts',
                                  username='pamrwatts',
                                  email='pam@test.org',
                                  password='test',
                                  profile_img=None)

    db.session.add(jacqui)
    db.session.add(pam)
    db.session.commit()

    zoe = Pet.add_new_pet_to_db(first_name='Zoe',
                                last_name='Watts',
                                animal='dog',
                                breed='dachshund',
                                birthdate='',
                                profile_img=None,
                                )

    cali = Pet.add_new_pet_to_db(first_name='Cali',
                                 last_name='Watts',
                                 animal='cat',
                                 breed='calico',
                                 birthdate='',
                                 profile_img=None,
                                 )

    db.session.add(zoe)
    db.session.add(cali)
    db.session.commit()

    zoe_jacqui = PetUser.add_new_pet_user_connection(user_id=jacqui.user_id,
                                                     pet_id=zoe.pet_id,
                                                     role='secondary',
                                                     )

    zoe_pam = PetUser.add_new_pet_user_connection(user_id=pam.user_id,
                                                  pet_id=zoe.pet_id,
                                                  role='primary',
                                                  )

    cali_jacqui = PetUser.add_new_pet_user_connection(user_id=jacqui.user_id,
                                                      pet_id=cali.pet_id,
                                                      role='secondary',
                                                      )

    cali_pam = PetUser.add_new_pet_user_connection(user_id=pam.user_id,
                                                   pet_id=cali.pet_id,
                                                   role='primary',
                                                   )

    db.session.add(zoe_jacqui)
    db.session.add(zoe_pam)
    db.session.add(cali_jacqui)
    db.session.add(cali_pam)
    db.session.commit()


def load_seed_activities():

    no1 = Activity.add_new_activity_to_db(activity='#1',
                                          min_daily=None,
                                          max_daily=None,
                                          )

    no2 = Activity.add_new_activity_to_db(activity='#2',
                                          min_daily=None,
                                          max_daily=None,
                                          )

    food = Activity.add_new_activity_to_db(activity='food',
                                           min_daily=1,
                                           max_daily=2,
                                           )

    walk = Activity.add_new_activity_to_db(activity='walk',
                                           min_daily=None,
                                           max_daily=None,
                                           )

    db.session.add(no1)
    db.session.add(no2)
    db.session.add(food)
    db.session.add(walk)
    db.session.commit()


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."

    load_seed_users_and_pets()
    load_seed_activities()
