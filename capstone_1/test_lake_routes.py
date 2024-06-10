import os
from unittest import TestCase, main
from unittest.mock import patch
from app import app, db
from models import User, Lake
from flask import g

class LakeRouteTests(TestCase):
    def setUp(self):
        os.environ['ENV'] = 'testing'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        db.session.query(User).delete()
        db.session.query(Lake).delete()
        db.session.commit()
        User.signup('admin_user', 'faker2@email.com', 'mmmmmm', True)
        User.signup('non_admin_user', 'faking@email.com', 'mmmmmm', False)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_render_add_lake_form_as_admin(self):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        res = self.app.get('/lake/add')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Add Lake', res.data)

    @patch('models.Lake.get_lake_lat_long')
    def test_add_lake_as_admin(self, mock_get_lat_long):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        with self.app as client:
            with client.session_transaction() as sess:
                user = User.query.first()
                sess['user_id'] = user.id
                g.user = user

            mock_get_lat_long.return_value = {'lat': 41.7318, 'lon': 93.6001}

            form_data = {
                'name': 'Test Lake',
                'state': 'IA',
                'closest_town': 'Ankeny'
            }
            response = client.post('/lake/add', data=form_data, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Lakes', response.data)
            lake = Lake.query.filter_by(name='Test Lake').first()
            self.assertIsNotNone(lake)
            self.assertEqual(lake.state, 'IA')

    @patch('models.Lake.get_lake_lat_long')
    def test_add_lake_as_non_admin(self, mock_get_lat_long):
        login_data = {'username': 'non_admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        with self.app as client:
            with client.session_transaction() as sess:
                user = User.query.first()
                sess['user_id'] = user.id
                g.user = user

            mock_get_lat_long.return_value = {'lat': 41.7318, 'lon': 93.6001}

            form_data = {
                'name': 'Test Lake',
                'state': 'IA',
                'closest_town': 'Ankeny'
            }
            response = client.post('/lake/add', data=form_data, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'not authorized', response.data)

    def test_view_lakes_as_non_admin(self):
        login_data = {'username': 'non_admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        lake = Lake(name='Test Lake', state='IA', closest_town='Ankeny', latitude=41.7318, longitude=93.6001)
        db.session.add(lake)
        db.session.commit()

        res = self.app.get('/lake/view-all')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'All Lakes', res.data)

    def test_view_lakes_as_admin(self):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        lake = Lake(name='Test Lake', state='IA', closest_town='Ankeny', latitude=41.7318, longitude=93.6001)
        db.session.add(lake)
        db.session.commit()

        res = self.app.get('/lake/view-all')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'All Lakes', res.data)
        self.assertIn(b'delete-btn', res.data)

    def test_render_edit_lake_form_as_admin(self):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
        lake = Lake(name='Test Lake', state='IA', closest_town='Ankeny', latitude=41.7318, longitude=93.6001)
        db.session.add(lake)
        db.session.commit()
        res = self.app.get('/lake/edit/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Edit Lake', res.data)

    def test_edit_lake_as_admin(self):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
        lake = Lake(name='Test Lake', state='IA', closest_town='Ankeny', latitude=41.7318, longitude=93.6001)
        db.session.add(lake)
        db.session.commit()
        edit_data={'name': 'Best Lake', 'state':'IA', 'closest_town':'Ankeny'}
        res = self.app.post('/lake/edit/1', data=edit_data,follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Best Lake', res.data)

    def test_edit_lake_as_non_admin(self):
        login_data = {'username': 'non_admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
        lake = Lake(name='Test Lake', state='IA', closest_town='Ankeny', latitude=41.7318, longitude=93.6001)
        db.session.add(lake)
        db.session.commit()
        edit_data={'name': 'Best Lake', 'state':'IA', 'closest_town':'Ankeny'}
        res = self.app.post('/lake/edit/1', data=edit_data,follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'not authorized', res.data)

    def test_delete_lake_as_admin(self):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
        lake = Lake(name='Test Lake', state='IA', closest_town='Ankeny', latitude=41.7318, longitude=93.6001)
        db.session.add(lake)
        db.session.commit()

        res = self.app.post(f"/lake/delete/{lake.id}", follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        deleted_lake = Lake.query.filter_by(id=lake.id).first()
        self.assertIsNone(deleted_lake)

    def test_delete_lake_as_non_admin(self):
        login_data = {'username': 'non_admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
        lake = Lake(name='Test Lake', state='IA', closest_town='Ankeny', latitude=41.7318, longitude=93.6001)
        db.session.add(lake)
        db.session.commit()

        res = self.app.post(f"/lake/delete/{lake.id}", follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        self.assertIn(b'not authorized', res.data)



