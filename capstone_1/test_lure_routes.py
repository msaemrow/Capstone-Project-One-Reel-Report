import os
from unittest import TestCase
from app import app, db
from models import User, Lure

class LureRouteTests(TestCase):
    def setUp(self):
        os.environ['ENV'] = 'testing'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()
        db.session.query(User).delete()
        db.session.query(Lure).delete()
        db.session.commit()
        self.user = User.signup('non_admin_user', 'faker2@email.com', 'mmmmmm', True)
        db.session.commit()
        login_data = {'username': 'non_admin_user','password': 'mmmmmm'}
        self.app.post('/login', data=login_data, follow_redirects=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_render_add_lure_form(self):
        res = self.app.get('/tackle-box/add')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Add New Lure', res.data)
    
    def test_add_lure(self):
        lure_data = {'name': 'shad rap', 'brand':'rapala', 'color':'blue', 'size': 'number 5'}
        res = self.app.post('/tackle-box/add', data=lure_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Tackle Box', res.data)
    
    def test_view_lures(self):
        res = self.app.get(f"/tackle-box/view-all/{self.user.id}")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Tackle Box', res.data)