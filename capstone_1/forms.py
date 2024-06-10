from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField, TimeField, DateField
from wtforms.validators import InputRequired, Email, Length, NumberRange, Optional

STATE_CHOICES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),('WI', 'Wisconsin'), ('WY', 'Wyoming')
    ]

##########  USER FORMS #######################
class AddUserForm(FlaskForm):
    """
    Form:
        - Creates a new user
    
    Fields:
        - username(StringField)
        - email(StringField)
        - password(PasswordField)
        - password2(PasswordField)
    """
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[Length(min=6)])

class UpdateUserForm(FlaskForm):
    """
    Form:
        - Update an existing user
    
    Fields:
        - username(StringField)
        - email(StringField)
        - password(PasswordField)
    """
    username = StringField('Update Username', validators=[InputRequired()])
    email = StringField('Update Email', validators=[InputRequired(), Email()])
    password = PasswordField('Enter password to update information', validators=[Length(min=6)])

class SignInForm(FlaskForm):
    """
    Form:
        - Sign in an existing user
    
    Fields:
        - username(StringField)
        - password(PasswordField)
    """
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


########## FISH CATCH FORMS #######################
class NewFishCatch(FlaskForm):
    """
    Form:
        - Add a fish catch
    
    Fields:
        - species(SelectField)
        - lake(SelectField)
        - lenght(FloatField)
        - weight(FloatField)
        - date(DateField)
        - time(TimeField)
        - lure(SelectField)
        - fish_image(StringField)    
    """
    species = SelectField('Fish Species', validators=[InputRequired()])
    lake = SelectField('Lake', validators=[InputRequired()])
    length = FloatField('Fish Length (inches)', validators=[NumberRange(min=0.0, max=60.0), Optional()] )
    weight = FloatField('Fish Weight (lbs)', validators=[NumberRange(min=0.0, max=60.0), Optional()] )
    date = DateField('Timestamp', validators=[InputRequired()])
    time = TimeField('Timestamp', validators=[InputRequired()])
    lure = SelectField('Lure', validators=[Optional()])
    fish_image = StringField('Fish Image URL', validators=[Optional()])

class UpdateFishCatch(FlaskForm):
    """
    Form:
        - Update an existing fish catch
    
    Fields:
        - species(SelectField)
        - lake(SelectField)
        - lenght(FloatField)
        - weight(FloatField)
        - fish_image(StringField)    
    """  
    species = SelectField('Fish Species', validators=[InputRequired()])
    lake = SelectField('Lake', validators=[InputRequired()])
    length = FloatField('Fish Length (inches)', validators=[NumberRange(min=0.0, max=60.0), Optional()] )
    weight = FloatField('Fish Weight (lbs)', validators=[NumberRange(min=0.0, max=60.0), Optional()] )
    fish_image = StringField('Fish Image URL', validators=[Optional()])
########## LAKE FORMS #######################
class AddLakeForm(FlaskForm):
    """
    Form:
        - Add or update an existing lake.
    
    Fields:
        - name(StringField
        - state(SelectField)
        - closest_town(StringField)
    """
    name = StringField('Lake Name', validators=[InputRequired()])
    state = SelectField('State', choices=STATE_CHOICES, validators=[InputRequired()])
    closest_town = StringField('Enter Closest Town (for weather data)', validators=[InputRequired()])

class EditLakeForm(FlaskForm):
    """
    Form
        - Update an existing lake.
    
    Fields:
        - name(StringField),
        - state(StringField),
        - closest_town(StringField)
    """
    name = StringField('Lake Name', validators=[InputRequired()])
    state = StringField('State (Use 2 character abbreviation)', validators=[InputRequired()])
    closest_town = StringField('Enter Closest Town (for weather data)', validators=[InputRequired()])
########## FISH SPECIES FORMS #######################
class AddFishSpeciesForm(FlaskForm):
    """
    Form
        - Add a new fish speices. 
    
    Fields:
        - species(StringField)
        - master_angler_length(FloatField)
    """
    species = StringField('Fish Species Name', validators=[InputRequired()])
    master_angler_length = FloatField('Minimum length to be considered master angler', validators=[InputRequired()])

class UpdateFishSpeciesForm(FlaskForm):
    """
    Form
        - Update an existing fish speices.
    
    Fields:
        - new_species_name(StringField)
        - master_angler_length(FloatField)
        """
    new_species_name = StringField('Fish Species Name', validators=[InputRequired(), Length(min=3)])
    master_angler_length = FloatField('Minimum length to be considered master angler', validators=[InputRequired()])

########## LURE FORMS #######################
class LureForm(FlaskForm):
    """
    Form
        - Add or update an existing lure.
    
    Fields:
        - name(StringField)
        - brand(StringField)
        - color(StringField)
        - size(StringField)
    """

    name = StringField('Name', validators=[InputRequired()])
    brand = StringField('Brand', validators=[InputRequired()])
    color = StringField('Color', validators=[Optional()])
    size = StringField('Size', validators=[Optional()])