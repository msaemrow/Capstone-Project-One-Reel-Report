from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import flash, request, jsonify, flash
from key import API_KEY
import requests
from sqlalchemy import func, desc, case


db=SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect this database to provided Flask app"""

    db.app = app
    db.init_app(app)
    app.app_context().push()

class User(db.Model):
    """Users in the platform
       Attributes: id, username, password, email, fish_catches, and is_admin
       Class Methods: signup, authenticate, passwords_match, increment_user_catch_total, decrement_user_catch_total, check_username_error
    """

    __tablename__='users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    fish_catches = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    is_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    @classmethod
    def signup(cls, username, email, password, admin=False):
        """
        Purpose:
            Accepts username, email and password and creates a new user in database. Hashes password and stores hashed password in db.
        Arguments:
            username (string): new user username
            email (string): new user email
            password (string): new user password
        Defaults: 
            is_admin = False, fish_catches = 0
        Returns:
            dict: username, email, hashed_password, fish_catches, is_admin
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username,
                    email=email,
                    password=hashed_pwd,
                    fish_catches=0,
                    is_admin=admin)
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """
        Purpose:
            Checks if entered password matches hashed password in database for given username
        Arguments:
            username(string): entered username
            password(string): entered password
        Returns:
            If userame and password are valid, returns True, otherwise returns Fal
        """
        user = cls.query.filter_by(username=username).first()

        if user:
            is_authorized = bcrypt.check_password_hash(user.password, password)
            if is_authorized:
                return user
        return False

    @classmethod
    def passwords_match(cls, password1, password2):
        """
        Purpose:
            Checks if 2 passwords match when creating a new password
        Arguments:
            password1(string): first entered password
            password2(string): second entered password
        Returns:
            True if passwords match
            If passwords don't match, flash message and return False
        """
        if password1 == password2:
            return True
        else:
            flash("Passwords don't match. Try again.", "danger")
            return False
        
    @classmethod
    def increment_user_catch_total(cls, user_id):
        """
        Purpose:
            Increments fish_catches by 1 for user
        Arguments: 
            user_id(int): User_id that will be incremented
        Returns:
            None
        """
        user = db.session.get(User, user_id)
        user.fish_catches = user.fish_catches + 1

        db.session.add(user)
        db.session.commit()

    @classmethod
    def decrement_user_catch_total(cls, user_id):
        """
        Purpose:
            Decrements fish_catches by 1 for user
        Arguments: 
            user_id(int): User_id that will be decremented
        Returns:
            None
        """
        user = db.session.get(User, user_id)
        user.fish_catches = user.fish_catches - 1

        db.session.add(user)
        db.session.commit()

    @classmethod
    def check_username_error(cls, e):
        """
        Purpose:
            Flashes message with specific issue depending on username error type
        Arguments:
            e: Error object
        Returns:
            None
        """

        if "users_username" in str(e).lower():
            flash("Username taken. Select a different username", 'danger')
        elif "users_email" in str(e).lower():
            flash("Email is already associated with an account. Go to login page to login", 'danger')
        else:
            flash(f"An error occurred. {e} Please try again.", "danger")  

class Lake(db.Model):
    """Model for a lake that a fish is caught from
       Attributes: id, name, closest_town, state, latitude, longitude
       Class Methods: get_lake_lat_long, get_forecast data
    """
    
    __tablename__ = 'lakes'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    state = db.Column(
        db.String(2),
        nullable=False
    )

    closest_town = db.Column(
        db.Text
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    @classmethod
    def get_lake_lat_long(cls, closest_town, state):
        """
        Purpose:
            Makes API call to openweathermap.org to get latitute and longitude for a lake
        Arguments:
            closest_town(string): name of nearest town for a lake
            state(string): state that the lake is located in
        Returns:
            If data is found return {"lat":lat, "lon":lon}
            Else return {'error': 'No data found'}
            If unable to reach API, return {'error': 'Failed to retrieve weather data'}
        """
        city = closest_town
        state= state
        country = 'US'
        res = requests.get(f"https://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=5&appid={API_KEY}")

        if res.status_code == 200:
            data = res.json()
            if data:
                city_data = data[0]
                lat = city_data['lat']
                lon = city_data['lon'] 
                lat_lon = {
                    "lat": lat,
                    "lon": lon
                }
                return lat_lon
            else:
                return jsonify({'error': 'No data found'})
        else:
            return jsonify({'error': 'Failed to retrieve latitude and longitude'}), res.status_code

    @classmethod
    def get_forecast_data(cls, lat, lon):
        """
        Purpose:
            Makes API call to openweathermap.org to get forecast data
        Arguments:
            lat(float): latitude of lake
            lon(float): longitude of lake
        Returns:
            Dict with 8 days of forecast data
            Forecast data for each day containes date, summary, high, low, pressure, wind_speed, wind_dir, and icon
        """
        res = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&units=imperial&appid={API_KEY}")
        if res.status_code == 200:
            weather_data = res.json()
            if weather_data:
                forecast_data = []
                daily_data = weather_data['daily']
                for day in daily_data:
                    full_date = datetime.fromtimestamp(day['dt'])
                    trimmed_date = full_date.strftime("%m/%d")
                    high = round(day['temp']['max'])
                    low = round(day['temp']['min'])
                    pressure = round(day['pressure'] * 0.02952998057228486, 2)
                    wind_speed = round(day['wind_speed'])
                    if day['wind_deg'] < 27:
                        wind_dir = "N"
                    elif day['wind_deg'] >= 27 and day['wind_deg'] < 135:
                        wind_dir = "E"
                    elif day['wind_deg'] >= 135 and day['wind_deg'] < 230:
                        wind_dir = "S"
                    elif day['wind_deg'] >= 230 and day['wind_deg'] < 315:
                        wind_dir = "W"
                    else:
                        wind_dir = "N" 
                    day_data={
                        'date':trimmed_date,
                        'summary': day['summary'],
                        'high': high,
                        'low': low,
                        'pressure': pressure,
                        'wind_speed': wind_speed,
                        'wind_dir': wind_dir,
                        'icon': day['weather'][0]['icon']
                        }
                    forecast_data.append(day_data)
                return forecast_data

class FishSpecies(db.Model):
    """Model for a fish species
        Attributes: id, name, master_angler_length
        Class Methods: None
    """

    __tablename__ = 'fish_species'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name= db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    master_angler_length = db.Column(
        db.Float,
        nullable = False
    )

class FishCatch(db.Model):
    """
    Model that shows details for a single fish catch and connects it to a user
    Attributes: 
        id, species_id, user_id, lake_id, length, weight, catch_date, catch_time, catch_timestamp, barometric, temperature, weather_conditions, wind_direction, wind_speed, lure_id, fish_image, is_master_angler 
    Relationships:
        user (User): The user who caught the fish; `user_id` foreign key.
        species(Species): They type of fish that was caught; `species_id` foreign key.
        lake(Lake): The lake the fish was caught on; `lake_id` foreign key.
        lure(Lure): The lure use to catch the fish; `lure_id` foreign key.
    Class Methods: 
        check_master_angler_status, get_weather_data, convert_to_unix, new_fish_catch, most_caught_species, popular_weather_conditions, popular_wind_direction,popular_barometric_pressure
    """

    __tablename__ = 'fish_catches'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    species_id = db.Column(
        db.Integer,
        db.ForeignKey('fish_species.id')
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    lake_id = db.Column(
        db.Integer,
        db.ForeignKey('lakes.id')
    )

    length = db.Column(
        db.Float
    )

    weight = db.Column(
        db.Float
    )

    catch_date = db.Column(
        db.Date
    )

    catch_time = db.Column(
        db.Time
    )
    
    catch_timestamp = db.Column(
        db.Integer,
        nullable=False,
        default=datetime.now
    )

    barometric = db.Column(
        db.Float
    )

    temperature = db.Column(
        db.Integer
    )

    weather_conditions = db.Column(
        db.Text
    )

    wind_direction = db.Column(
        db.String(2)
    )

    wind_speed = db.Column(
        db.Integer
    )

    lure_id = db.Column(
        db.Integer,
        db.ForeignKey('lures.id')
    )

    fish_image = db.Column(
        db.Text,
        default='/static/images/stock-fish.jpg'
    )

    is_master_angler = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    @classmethod
    def check_master_angler_status(cls, species_id, length):
        """
            Purpose:
                Check if a given fish catch qualifies as a Master Angler catch
            Arguments:
                species_id: ID of the fish species that was caught
                length: Length of the fish that was caught
            Returns:
                bool: True if fish qualifies as Master Angler catch, otherwise returns False
        """
        species = db.session.get(FishSpecies, species_id)
        min_length = species.master_angler_length
        if length >= min_length:
            return True
        else:
            False

    @classmethod
    def get_weather_data(cls, lat, long, dt):
        """
        Purpose:
            Makes API call to api.openweather.org to get weather data for a lake base based on a timestamp
        Arguments:
            lat(float):latitude of lake
            long(float):longitude of lake
            dt(int): date/time in unix
        Returns:
        """
        res = requests.get(f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={long}&dt={dt}&appid={API_KEY}&units=imperial')
        if res.status_code == 200:
            data = res.json()
            pressure = round(data['data'][0]['pressure'] * 0.02952998057228486, 2)
            temp = data['data'][0]['temp']
            wind_deg = data['data'][0]['wind_deg']
            desc = data['data'][0]['weather'][0]['description']
            speed = data['data'][0]['wind_speed']
            if wind_deg < 27:
                wind_dir = "N"
            elif wind_deg >= 27 and wind_deg < 135:
                wind_dir = "E"
            elif wind_deg >= 135 and wind_deg < 230:
                wind_dir = "S"
            elif wind_deg >= 230 and wind_deg < 315:
                wind_dir = "W"
            else:
                wind_dir = "N"                        
            weather_data ={
                "weather": desc, 
                "pressure": pressure,
                "temp": temp,
                "wind_dir": wind_dir,
                "wind_speed": speed
            }
            return weather_data
        else:
            print('Failed to get weather data')
            return jsonify({'error': 'Failed to retrieve weather data'}), res.status_code

    @classmethod
    def convert_to_unix(cls, date, time):
        """
        Purpose:
            Converts date and time to unix
        Arguments:
            date(date): date fish was caught
            time(time): time fish was caught
        Returns:
            int: unix timestamp for date/time fish was caught
        """
        date_time_str = f"{date} {time}"
        date_time_ojb = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        return int(date_time_ojb.timestamp())

    @classmethod
    def new_fish_catch(cls, species, user, lake_id, length, weight, date, time, lure, image):
        """
        Purpose:
            Creates a new fish catch for a user
        Arguments:
            species(int): id for species that was caught
            user(int): id for user that caught fish
            lake_id(int): lake id that fish was caught on
            length(float): length of fish that was caught
            weight(float): weight of fish that was caught
            date(date): date of fish catch
            time(time): time of fish catch
            lure(int): id of lure that fish was caught on
            image(string): url for image of fish
        Returns:
            Dict containing all fish properties
        """
        lake = db.session.get(Lake, lake_id)
        default_value = '/static/images/stock-fish.jpg'
        master_angler_status = FishCatch.check_master_angler_status(species, length)
        unix_time = FishCatch.convert_to_unix(date, time)
        weather_data = FishCatch.get_weather_data(lake.latitude, lake.longitude, unix_time)
        new_catch = FishCatch(species_id=species,
                                user_id=user,
                                lake_id=lake_id,
                                length=length,
                                weight=weight,
                                catch_date=date,
                                catch_time= time,
                                catch_timestamp=unix_time,
                                barometric=weather_data['pressure'],
                                temperature=weather_data['temp'],
                                weather_conditions=weather_data['weather'],
                                wind_direction=weather_data['wind_dir'],
                                wind_speed=weather_data['wind_speed'],
                                lure_id=lure,
                                fish_image=image if image != '' else default_value,
                                is_master_angler=master_angler_status)  
        db.session.add(new_catch)
        return(new_catch)

    @classmethod
    def most_caught_species(cls, user_id):
        """
        Purpose:
            find the most popular fish species that fish were caught in for a user
        Arguments:
            user_id(int): id of user
        Returns:
            Dict containing count of fish species in descending order
        """
        species_counts =db.session.query(FishSpecies.name, func.count(FishCatch.id).label('count')).join(FishCatch, FishSpecies.id==FishCatch.species_id).filter(FishCatch.user_id == user_id).group_by(FishSpecies.name).order_by(desc('count')).all()
        return species_counts

    @classmethod
    def popular_weather_conditions(cls, user_id):
        """
        Purpose:
            find the most popular weather conditions that fish were caught in for a user
        Arguments:
            user_id(int): id of user
        Returns:
            Dict containing count of weather conditions in descending order
        """
        weather_conditions =db.session.query(FishCatch.weather_conditions, func.count(FishCatch.id).label('count')).filter(FishCatch.user_id == user_id).group_by(FishCatch.weather_conditions).order_by(desc('count')).all()
        return weather_conditions

    @classmethod
    def popular_wind_direction(cls, user_id):
        """
        Purpose:
            find the most popular wind direction that fish were caught in for a user
        Arguments:
            user_id(int): id of user
        Returns:
            Dict containing count of wind direction in descending order
        """
        wind_conditions =db.session.query(FishCatch.wind_direction, func.count(FishCatch.id).label('count')).filter(FishCatch.user_id == user_id).group_by(FishCatch.wind_direction).order_by(desc('count')).all()
        return wind_conditions

    @classmethod
    def popular_barometric_pressure(cls, user_id):
        """
        Purpose:
            find the most popular barometric pressure that fish were caught in for a user
        Arguments:
            user_id(int): id of user
        Returns:
            Dict containing count of barometric pressure in descending order
        """
        high_pressure_range = (30.50, float('inf'))
        medium_pressure_range = (29.70, 30.40)
        low_pressure_range = (float('-inf'), 29.60)

        pressure_category = case(
            (FishCatch.barometric.between(*high_pressure_range), 'High ( >30.5 )'),
            (FishCatch.barometric.between(*medium_pressure_range), 'Medium ( 29.7 - 30.4 )'), else_='Low ( <29.6 )')
        barometric_conditions = db.session.query(pressure_category, func.count(FishCatch.id).label('count')).filter(FishCatch.user_id == user_id).group_by(pressure_category).order_by(func.count(FishCatch.id).desc()).all()
        return barometric_conditions
    
    species= db.relationship('FishSpecies', backref=db.backref('species_fish_catches'))
    user = db.relationship('User', backref=db.backref('user_fish_catches'))
    lake = db.relationship('Lake', backref=db.backref('lake_fish_catches'))
    lure = db.relationship('Lure', backref=db.backref('lure_fish_catches'))

class Lure(db.Model):
    """
    Model for a lure that a user used to catch a fish
    Attributes: 
        id, user_id, brand, name, color, size
    Relationships:
        user (User): The user who used the lure; `user_id` foreign key.
    Class Methods: None
    """
    
    __tablename__ = 'lures'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE')
    )

    brand = db.Column(
        db.Text,
        nullable=False
    )
    
    name = db.Column(
        db.Text,
        nullable=False
    )

    color = db.Column(
        db.Text,
        nullable=False
    )

    size= db.Column(
        db.Text,
        nullable=False
    )

    user = db.relationship('User', backref=db.backref('user_lure'))