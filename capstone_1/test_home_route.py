from unittest import TestCase
from app import app

class ReelReportHomeTests(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('REEL REPORT', html)
    
    def test_features_page(self):
        with app.test_client() as client:
            res = client.get('/features')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Features:', html)



