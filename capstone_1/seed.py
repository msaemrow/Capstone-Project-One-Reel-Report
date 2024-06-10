from app import db
from models import User, Lake, FishSpecies, Lure
from csv import DictReader

db.drop_all()
db.create_all()

with open('base-data/fish-species.csv') as species:
    db.session.bulk_insert_mappings(FishSpecies, DictReader(species))

# demo admin user
User.signup('admin', 'test@test.com', 'mmmmmm', True)
# demo non admin user
User.signup('non_admin', 'test2@test.com', 'mmmmmm', False)

db.session.commit()

lake1 = Lake(name='Horsehoe Lake', state='MN', closest_town='Waterville', latitude=44.2189914, longitude=-93.56797)
lake2 = Lake(name='Leech Lake', state='MN', closest_town='Walker', latitude=47.101709, longitude=-94.585026)
lake3 = Lake(name='Red Lake', state='MN', closest_town='Waskish', latitude=48.161352, longitude=-94.512455)
lake4 = Lake(name='Lake Minnetonka', state='MN', closest_town='Minnetonka', latitude=44.9405086, longitude=-93.4638936)

lure = Lure(user_id=1, brand='Rapala', name='Shad Rap', color='Fire Tiger', size='No. 5')
lure2 = Lure(user_id=1, brand='Keitech', name='Easy Shiner', color='Bluegill Flash', size='3 in.')
lure3 = Lure(user_id=1, brand='VMC', name='Moon Eye Jig', color='Glow Pink', size='1/8 oz.')
lure4 = Lure(user_id=1, brand='Cotton Cordell', name='Baby-O', color='Pearl', size='')

db.session.add_all([lure, lure2, lure3, lure4, lake1, lake2, lake3, lake4])
db.session.commit()