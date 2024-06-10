from flask import Blueprint, render_template


home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    """
    Homepage for Reel Report. Has buttons for users to login and sign up

    Authentication
        - None (anyone can view)
    """
    return render_template('home.html')

@home_bp.route('/features')
def features():
    """
    Page the shows the features of Reel Report

    Authentication
        - None (anyone can view)
    """
    return render_template('features.html')


