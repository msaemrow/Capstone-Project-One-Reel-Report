from flask import Blueprint, render_template, redirect, url_for, g, flash, abort
from models import FishCatch, User, db
from forms import AddUserForm, UpdateUserForm, SignInForm
from helpers import login_required, add_user_to_session, remove_user_from_session
from sqlalchemy.exc import IntegrityError


user_bp = Blueprint('user', __name__)

@user_bp.route('/signup', methods=["GET", "POST"])
def signup():
    """
    Handle the user signup process

    GET:
        Render the signup form
    POST:
        If the form is valid and passwords match:
            -Create new user in DB
            -add user to the session
            -Redirect to the user.view_user route
        If the username is already taken:
            -Flash message to user and re-load form
            -Re-render the sign up form
    Forms:
        AddUserForm
    Functions:
        User.passwordsmatch, User.signup(), User.check_username_error(), add_user_to_session()
    Returns:
        - Rendered signup template if GET request or form validation fails.
        - Redirect to user home page if signup is successful.
    """
    form = AddUserForm()

    if form.validate_on_submit() and User.passwords_match(form.password.data, form.password2.data):
        try:
            user=User.signup(username=form.username.data,
                        password=form.password.data,
                        email=form.email.data)
            db.session.commit()

        except IntegrityError  as e:
            User.check_username_error(e)
            return render_template('user/signup.html', form=form)
        add_user_to_session(user)
        return redirect(url_for('user.view_user', user_id=user.id))
    else:
        return render_template('user/signup.html', form=form)

@user_bp.route('/login', methods=["GET", "POST"])
def login():
    """
    Handle existing user login process

    GET:
        Render login form
    POST:
        If form is valid:
            -Authenticate user credentials
            -If credentials are valid:
                -Add user to session
                -Flash welcome message
                -Redirect to user.view_user route
            -If invalid credentials
                -Flash message
                -Re-render login form
    Forms:
        SignInForm
    Functions:
        User.authenticate(), add_user_to_session()
    Returns:
        - Rendered login template if GET request or form validation fails.
        - Redirect to user home page if signup is successful.
    """
    form = SignInForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        
        if user:
            add_user_to_session(user)
            flash(f"Welcome back {user.username}!", "success")
            return redirect(url_for('user.view_user', user_id=user.id))
        
        flash("Password did not match. Please try again", 'danger')

    return render_template('user/login.html', form=form)

@user_bp.route('/logout')
def logout():
    """
    Handle the user logout process

    Actions:
        -Remove user from session
        -Flash success message
        -Redirect to login page
    Functions:
        remove_user_from_session()
    Returns:
        -Redirect to the login page after logout
    """
    remove_user_from_session()
    flash("Successful logout. Goodbye.", 'success')
    return redirect(url_for('user.login'))

@user_bp.route('/user/view/<int:user_id>')
@login_required
def view_user(user_id):
    """
    View the profile of a single user.

    Only the user themselves or an admin can view the profile. Relevant information on the profile is recent fish catches, master angler catches, and various fishing statistics.
    
    Authentication:
        Requires user to be logged; checked via @login_required
    Arguments:
        user_id(int): Id of the user being viewed
    Functions:
        FishCatch.most_caught_species(), FishCatch.popular_weather_conditions(),FishCatch.popular_wind_direction(),FishCatch.popular_barometric_pressure()
    Returns:
        -Renders user profile template with passed in user's catch information
    Raises:
        -404: If no user is found
        -401: If the logged in user is not authorized to view the user's profile
    """
    user = db.session.get(User, user_id)
    if not user:
        abort(404, "User not found")
    if g.user.is_admin == True or g.user.id == user.id:
        user_catches = FishCatch.query.filter_by(user_id=user_id).order_by(FishCatch.catch_date.desc()).limit(8)
        master_angler_catches=  FishCatch.query.filter_by(user_id=user_id, is_master_angler=True).order_by(FishCatch.catch_date.desc()).all()
        most_caught = FishCatch.most_caught_species(user_id)
        popular_weather = FishCatch.popular_weather_conditions(user_id)
        popular_wind = FishCatch.popular_wind_direction(user_id)
        barometric_conditions = FishCatch.popular_barometric_pressure(user_id)
        return render_template('/user/view-user.html', user=user, user_catches=user_catches, master_angler_catches=master_angler_catches,  most_caught=most_caught, popular_weather=popular_weather, popular_wind=popular_wind, barometric_conditions=barometric_conditions)
    abort(401, "Not authorized to view user")

@user_bp.route('/user/edit', methods=["GET", "POST"])
@login_required
def edit_user():
    """
    Handle editing user information.
    Information that can be edited is username and email. 
    User must enter correct password to update user information.

    Authentication:
        Requires user to be logged; checked via @login_required
    GET:
        Render UpdateUserForm
    POST:
        If form is valid:
            -If password is correct:
                -Update the user's username and email
                -Save changes to the database
                -Redirect the the users profile page
            -If the password is incorrect:
                -Display an error message on the formd
    Forms:
        -UpdateUserForm
    Functions:
        -User.authenticate()
    Returns:
        -Rendered template for the edit user form
        -Redirect to the user's profile upon successful update
    """
    form=UpdateUserForm(obj=g.user)

    if form.validate_on_submit():
        if User.authenticate(g.user.username, form.password.data):
            g.user.username = form.username.data
            g.user.email = form.email.data
            db.session.add(g.user)
            db.session.commit()
            return redirect(url_for('view_user', user_id=g.user.id))
        else:
            form.password.errors=['Incorrect Password Entered']

    return render_template('user/edit-user.html', form=form, user=g.user)

@user_bp.route('/user/delete/<int:user_id>', methods=["POST"])
@login_required
def delete_user(user_id):
    """
    Handle deleting user process.
    Allows the logged-in user to delete their own account.

    Authentication:
        - Requires user to be logged; checked via @login_required

    Arguments:
        - user_id(int): Id of the user being viewed

    Actions:
        - Query database to find user
        - Delete user user from database
        - Remove user from session
        - If user does not have permission to delete the account:
            - Flash warning message to user
            - Redirect user to home page

    Functions:
        - remove_user_from_session()
        
    Returns:
        - Redirects to the home page after successful deletion 
    """
    if g.user.id == user_id:
        user = db.session.get(User, user_id)
        db.session.delete(user)
        db.session.commit()
        remove_user_from_session
        return redirect(url_for('home.home'))
    else:
        flash("You don't have permission to delete that account")
        return redirect(url_for('home.home'))
