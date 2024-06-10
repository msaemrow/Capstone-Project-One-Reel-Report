import os
from unittest import TestCase, main
from app import app, db
from models import User, FishSpecies

class FishSpeciesRouteTests(TestCase):
    def setUp(self):
        os.environ['ENV'] = 'testing'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        db.session.query(User).delete()
        db.session.query(FishSpecies).delete()
        db.session.commit()
        User.signup('admin_user', 'faker2@email.com', 'mmmmmm', True)
        User.signup('non_admin_user', 'faking@email.com', 'mmmmmm', False)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_render_add_fish_species_form_admin(self):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        res = self.app.get('/fishspecies/add')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Add Fish Species', res.data)

    def test_add_add_fish_species_admin(self):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        form_data = {
            'species': 'Test Fish',
            'master_angler_length': 10
        }
        res = self.app.post('/fishspecies/add', data=form_data, follow_redirects=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'All Fish Species', res.data)
        fish = FishSpecies.query.filter_by(name='Test Fish').first()
        self.assertIsNotNone(fish)
        self.assertEqual(fish.master_angler_length, 10)

    def test_add_add_fish_species_non_admin(self):
        login_data = {'username': 'non_admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        form_data = {
            'species': 'Test Fish',
            'master_angler_length': 10
        }
        res = self.app.post('/fishspecies/add', data=form_data, follow_redirects=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'not authorized', res.data)
    
    def test_view_fish_species_admin(self):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        res = self.app.get('/fishspecies/view-all')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'All Fish Species', res.data)
        self.assertIn(b'Add Species', res.data)

    def test_view_fish_species_non_admin(self):
        login_data = {'username': 'non_admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
        
        res = self.app.get('/fishspecies/view-all', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'All Fish Species', res.data)

    def test_render_edit_fish_species_form_admin(self):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
        fish=FishSpecies(name="crappie", master_angler_length=10)
        db.session.add(fish)
        db.session.commit()
        res = self.app.get(f"/fishspecies/edit/{fish.id}")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Edit Fish Species', res.data)

    def test_edit_fish_species_admin(self):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
        fish=FishSpecies(name="crappie", master_angler_length=10)
        db.session.add(fish)
        db.session.commit()
        edit_data={'new_species_name': 'Bass', 'master_angler_length':10}
        res = self.app.post('/fishspecies/edit/1', data=edit_data,follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Bass', res.data)
        self.assertIn(b'delete-btn', res.data)
    
    def test_edit_fish_species_non_admin(self):
        login_data = {'username': 'non_admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
        fish=FishSpecies(name="crappie", master_angler_length=10)
        db.session.add(fish)
        db.session.commit()
        edit_data={'name': 'Bass', 'master_angler_length':10}
        res = self.app.post('/fishspecies/edit/1', data=edit_data,follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'not authorized', res.data)
    
    def test_delete_fish_species_admin(self):
        login_data = {'username': 'admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        fish=FishSpecies(name="crappie", master_angler_length=10)
        db.session.add(fish)
        db.session.commit()

        res = self.app.post(f"/fishspecies/delete/{fish.id}", follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        deleted_species = FishSpecies.query.filter_by(id=fish.id).first()
        self.assertIsNone(deleted_species)

    def test_delete_fish_species_non_admin(self):
        login_data = {'username': 'non_admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
    
        fish=FishSpecies(name="crappie", master_angler_length=10)
        db.session.add(fish)
        db.session.commit()

        res = self.app.post(f"/fishspecies/delete/{fish.id}", follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'not authorized', res.data)
