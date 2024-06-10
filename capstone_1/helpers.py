from functools import wraps
from flask import flash, g, redirect, url_for, session
from models import User, db

CURR_USER_KEY = "curr_user"


def add_user_to_session(user):
    """
    Purpose:
        - During login, adds user id to the session
    
    Arguments:
        - user: user dict containing user id
    
    Returns:
        - None
    """

    session[CURR_USER_KEY] = user.id

def remove_user_from_session():
    """
    Purpose:
        - During logut, removes user id from the session
    
    Arguments:
        - None
    
    Returns:
        - None
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def add_user_to_g_user():
    """
    Purpose:
        - If user has been added to session[CURR_USER_KEY], then add user_id to Flask global
    
    Arguments:
        - None
    
    Returns:
        - None    
    """

    if CURR_USER_KEY in session:
        g.user = db.session.get(User, session[CURR_USER_KEY])
    else:
        g.user = None

def login_required(f):
    """
    Purpose:
        - Checks if user_id is stored in g.user. If not, flashes unauthorized message, otherwise allows user access to page
    
    Arguments:
        - None
    
    Returns:
        - Function: The original function if the user is authenticated, otherwise redirects to the login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            flash("Access unauthorized. Please log in first", "danger")
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function
