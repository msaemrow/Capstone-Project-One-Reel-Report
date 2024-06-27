import os
import sys
import secrets
from flask import Flask, render_template
from models import db, connect_db
from routes import lure_routes, lake_routes, fish_species_routes, fish_catch_routes, user_routes, home_routes
from helpers import add_user_to_g_user
from sqlalchemy.orm import scoped_session, sessionmaker

CURR_USER_KEY = "curr_user"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

if os.environ.get('ENV')  == 'testing':
    app.config['SQLALCHEMY_DATABASE_URI']= (
        os.environ.get('DATABASE_URL', 'postgresql:///reel_report_test'))
    app.config['SECRET_KEY'] = 'test_secret_key'  
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vnjfdwfn:Ur9L_j2ppxvs0JjQQW6UnQ5iPM9wZmyT@raja.db.elephantsql.com/vnjfdwfn'
    app.config['SECRET_KEY'] = secrets.token_hex(16)

# app.config['SQLALCHEMY_DATABASE_URI']= (
#     os.environ.get('DATABASE_URL', 'postgresql:///reel_report_test'))
# app.config['SECRET_KEY'] = 'test_secret_key'  

connect_db(app)

Session = scoped_session(sessionmaker(bind=db.engine))

app.register_blueprint(lure_routes.lure_bp)
app.register_blueprint(lake_routes.lake_bp)
app.register_blueprint(fish_species_routes.species_bp)
app.register_blueprint(fish_catch_routes.catch_bp)
app.register_blueprint(user_routes.user_bp)
app.register_blueprint(home_routes.home_bp)

@app.before_request
def before_request():
    db.session = Session()
    add_user_to_g_user()

@app.teardown_request
def teardown_request(exception=None):
    if exception:
        db.session.rollback()
    db.session.remove()
#########################  Home Page and Error Pages #####################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_error.html'), 404

@app.errorhandler(401)
def not_authorized(e):
    return render_template('401_not_authorized.html'), 401
##############################################################################
# Turn off all caching in Flask
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req

if __name__ == '__main__':
    app.run()