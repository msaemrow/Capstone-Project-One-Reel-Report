import os
from unittest import TestCase
from models import db, connect_db, User, Lake, FishSpecies, FishCatch, Lure
from flask import Flask

class TestModels(TestCase):
    """Test cases for models"""

    def setUp(self):
        """Set up test environment"""
        app = Flask(__name__)
        os.environ['ENV'] = 'testing'
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///reel_report_test'
        connect_db(app)
        db.create_all()

    def tearDown(self):
        """Clean up after test"""
        db.session.remove()
        db.drop_all()

    def test_user_signup(self):
        """Test user signup"""
        user = User.signup('testuser', 'test@example.com', 'password')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.username, 'testuser')

    def test_get_lake_lat_long(self):
        """Test get_lake_lat_long method"""
        lat_long = Lake.get_lake_lat_long('Townsville', 'TX')
        self.assertIsNotNone(lat_long)

    def test_get_forecast_data(self):
        """Test get_forecast_data method"""
        forecast_data = Lake.get_forecast_data(29.423017, -98.485374)
        self.assertIsNotNone(forecast_data)

    def test_check_master_angler_status(self):
        """Test check_master_angler_status method"""
        species = FishSpecies(name='fish', master_angler_length=25.0)
        db.session.add(species)
        db.session.commit()
        status = FishCatch.check_master_angler_status(1, 30.0)
        self.assertTrue(status)

    def test_get_weather_data(self):
        """Test get_weather_data method"""
        weather_data = FishCatch.get_weather_data(29.423017, -98.485374, 1622745600)
        self.assertIsNotNone(weather_data)

    def test_convert_to_unix(self):
        """Test convert_to_unix method"""
        unix_time = FishCatch.convert_to_unix('2024-06-03', '12:00:00')
        self.assertIsNotNone(unix_time)

    def test_new_fish_catch(self):
        """Test new_fish_catch method"""
        user = User.signup('faking_user', 'faker2@email.com', 'mmmmmm')
        db.session.commit()
        lure = Lure(user_id=user.id, name='lure', brand='brand', color='color', size='size')
        lake = Lake(name='lake', state='MN', closest_town='town', latitude=50.1, longitude= 25.5)
        species = FishSpecies(name='species',master_angler_length=10.5)
        db.session.add_all([lake, species, lure])
        db.session.commit()
        catch = FishCatch.new_fish_catch(1, 1, 1, 20.0, 5.0, '2024-06-03', '12:00:00', 1, '')
        db.session.add(catch)
        db.session.commit()
        self.assertIsNotNone(catch)

    def test_most_caught_species(self):
        """Test most_caught_species method"""
        species_counts = FishCatch.most_caught_species(1)
        self.assertIsNotNone(species_counts)

    def test_popular_weather_conditions(self):
        """Test popular_weather_conditions method"""
        weather_conditions = FishCatch.popular_weather_conditions(1)
        self.assertIsNotNone(weather_conditions)

    def test_popular_wind_direction(self):
        """Test popular_wind_direction method"""
        wind_conditions = FishCatch.popular_wind_direction(1)
        self.assertIsNotNone(wind_conditions)

    def test_popular_barometric_pressure(self):
        """Test popular_barometric_pressure method"""
        pressure_conditions = FishCatch.popular_barometric_pressure(1)
        print(pressure_conditions)
        self.assertIsNotNone(pressure_conditions)
