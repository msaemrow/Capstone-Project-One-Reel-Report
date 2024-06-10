import os
from unittest import TestCase
from unittest.mock import patch
from models import User, FishCatch, Lake, FishSpecies, Lure
from app import app, db
from werkzeug.datastructures import MultiDict

class ReelReportFishCatchTests(TestCase):
    def setUp(self):
        os.environ['ENV'] = 'testing'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        db.session.query(User).delete()
        db.session.query(Lake).delete()
        db.session.query(FishSpecies).delete()
        db.session.query(Lure).delete()
        db.session.commit()
        user = User.signup('faking_user', 'faker2@email.com', 'mmmmmm')
        db.session.commit()
        lure = Lure(user_id=user.id, name='lure', brand='brand', color='color', size='size')
        lake = Lake(name='lake', state='MN', closest_town='town', latitude=50.1, longitude= 25.5)
        species = FishSpecies(name='species',master_angler_length=10.5)
        db.session.add_all([lake, species, lure])
        db.session.commit()
 
    def tearDown(self):
        os.environ['ENV'] = 'production'
        db.session.remove()
        db.drop_all()
        db.session.close()

    def test_add_fish_catch_render_form(self):
        """Test GET request for add_fish_catch"""
        login_data = MultiDict([('username', 'faking_user'), ('password', 'mmmmmm')])
        res = self.app.post('/login', data=login_data, follow_redirects=True)
   
        res = self.app.get('/fishcatch/add')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Add New Catch', res.data)

    def test_add_fish_catch_post_route(self):

        """Test POST request for add_fish_catch"""

        login_data = MultiDict([('username', 'faking_user'), ('password', 'mmmmmm')])
        self.app.post('/login', data=login_data, follow_redirects=True)
   
        form_data = {
            'species': 1,
            'user_id': 1,
            'lake': 1,
            'length': 10,
            'weight': 5,
            'date': '2024-06-10',
            'time': '10:00',
            'lure': 1,
            'fish_image': 'example.jpg'
        }

        res = self.app.post('/fishcatch/add', data=form_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Successfully added', res.data)
    
    def test_view_fish_catch_all(self):
        login_data = {
        'username': 'faking_user',
        'password': 'mmmmmm'
    }
        self.app.post('/login', data=login_data, follow_redirects=True)

        form_data = {
            'species': 1,
            'user_id': 1,
            'lake': 1,
            'length': 10,
            'weight': 5,
            'date': '2024-06-10',
            'time': '10:00',
            'lure': 1,
            'fish_image': 'example.jpg'
        }
        self.app.post('/fishcatch/add', data=form_data, follow_redirects=True)

        res = self.app.get('/fishcatch/view/1')

        self.assertEqual(res.status_code, 200)
        self.assertIn(b'All Catches', res.data)

    def test_view_fish_catch_one(self):
        login_data = {'username': 'faking_user', 'password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
        form_data = {
            'species': 1,
            'user_id': 1,
            'lake': 1,
            'length': 10,
            'weight': 5,
            'date': '2024-06-10',
            'time': '10:00',
            'lure': 1,
            'fish_image': 'example.jpg'
        }
        self.app.post('/fishcatch/add', data=form_data, follow_redirects=True)

        res = self.app.get('/fishcatch/view/1/1')

        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Catch ID: 1', res.data)
     
    def test_view_edit_fish_catch_form(self):
        login_data = {'username': 'faking_user', 'password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        form_data = {
            'species': 1,
            'user_id': 1,
            'lake': 1,
            'length': 10,
            'weight': 5,
            'date': '2024-06-10',
            'time': '10:00',
            'lure': 1,
            'fish_image': 'example.jpg'
        }
        self.app.post('/fishcatch/add', data=form_data, follow_redirects=True)
        res= self.app.get('fishcatch/edit/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Update', res.data)
    
    def test_delete_fish_catch(self):
        login_data = {'username': 'faking_user', 'password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        form_data = {
            'species': 1,
            'user_id': 1,
            'lake': 1,
            'length': 10,
            'weight': 5,
            'date': '2024-06-10',
            'time': '10:00',
            'lure': 1,
            'fish_image': 'example.jpg'
        }
        self.app.post('/fishcatch/add', data=form_data, follow_redirects=True)

        res = self.app.post('/fishcatch/delete/1')
        self.assertEqual(res.status_code, 302)

        deleted_catch = FishCatch.query.filter_by(id=1).first()
        self.assertIsNone(deleted_catch)
