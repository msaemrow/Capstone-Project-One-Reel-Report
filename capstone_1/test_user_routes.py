import os
from unittest import TestCase, main
from app import app, db
from models import User

class UserRouteTests(TestCase):
    def setUp(self):
        os.environ['ENV'] = 'testing'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///reel_report_test'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_render_signup_form(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)    

    def test_signup_process(self):
        form_data = {
            'username': 'test_user',
            'password': 'password123',
            'password2': 'password123',
            'email': 'test@example.com'
        }
        response = self.app.post('/signup', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b' <h1 class="text-center ">test_user</h1>', response.data)

    def test_username_taken(self):
        # Create a user with the same username
        user = User(username='test_user', password='password', email='existing@example.com')
        db.session.add(user)
        db.session.commit()

        form_data = {
            'username': 'test_user',
            'password': 'password123',
            'password2': 'password123',
            'email': 'new@example.com'
        }
        response = self.app.post('/signup', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username taken. Select a different username', response.data) 
    
    def test_invalid_form(self):
        form_data={
            'username': '',
            'password': 'password123',
            'password2': 'password123',
            'email': 'new@example.com'            
        }
        response = self.app.post('/signup', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required', response.data)
    
    def test_render_login_form(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_valid_login(self):
        User.signup('testing_user', 'test22@email.com', 'password')
        db.session.commit()

        login_data = {'username': 'testing_user','password': 'password'}
        response = self.app.post('/login', data=login_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back testing_user!', response.data)

    def test_view_profile(self):
        User.signup('faking_user', 'faker2@email.com', 'mmmmmm')
        db.session.commit()

        login_data = {'username': 'faking_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        res = self.app.get('/user/view/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'faking_user', res.data)

    def test_view_profile_does_not_exist(self):
        User.signup('faking_user', 'faker2@email.com', 'mmmmmm')
        db.session.commit()

        login_data = {'username': 'faking_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        res = self.app.get('/user/view/2')
        self.assertEqual(res.status_code, 404)
        self.assertIn(b'This page does not exist', res.data)

    def test_view_profile_unauthorized(self):
        User.signup('faking_user', 'faker2@email.com', 'mmmmmm')
        User.signup('faking_user2', 'faker22@email.com', 'mmmmmm')
        db.session.commit()
        login_data = {'username': 'faking_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)
        
        res = self.app.get('/user/view/2')
        self.assertEqual(res.status_code, 401)
        self.assertIn(b'Unauthorized.', res.data)
    
    def test_edit_user_form(self):
        User.signup('faking_user', 'faker2@email.com', 'mmmmmm')
        db.session.commit()
        login_data = {'username': 'faking_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        res = self.app.get('/user/edit')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Update Information', res.data)

    def test_delete_user(self):
        user = User.signup('faking_user', 'faker2@email.com', 'mmmmmm')
        db.session.commit()
        login_data = {'username': 'faking_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

        response = self.app.post(f'/user/delete/{user.id}')
        self.assertEqual(response.status_code, 302)

        deleted_user = User.query.filter_by(id=user.id).first()
        self.assertIsNone(deleted_user)