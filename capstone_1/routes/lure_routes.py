from flask import Blueprint, render_template, redirect, url_for, g
from models import Lure, User, db
from forms import LureForm
from helpers import login_required


lure_bp = Blueprint('lure', __name__)


@lure_bp.route('/tackle-box/view-all/<int:user_id>')
@login_required
def view_tackle_box(user_id):
    """
    Handles viewing all lures in a tackle box for a single user. Only can view lures for same user

    Authentication:
        - Requires user to be logged in (checked via @login_required)
    
    Arguments:
        - user_id(int): Id of user to get tackle box for
    
    GET:
        - Query database and get all lures for a single user
        - Render template to display all lures
    
    Returns:
        - Render template showing all lures in tackle box
    """
    lures = Lure.query.filter_by(user_id=user_id).order_by(Lure.brand.asc()).all()
    user = db.session.get(User, user_id)
    return render_template('/tackle_box/view-all-lures.html', lures=lures, user=user)

@lure_bp.route('/tackle-box/add', methods=["GET", "POST"])
@login_required
def add_lure():
    """
    Handles viewing adding a new lure in a tackle box for a single user. Only can add lures for same users tackle box

    Authentication:
        - Requires user to be logged in (checked via @login_required)
    
    Arguments:
        - None
    
    GET:
        - Render LureForm
    
    POST: 
        - If for is valid
            - Create new lure in database using g.user.id as the user_id
            - Redirect to view all lures
    
    Returns:
        - Render template showing all lures in tackle box
    """
    form = LureForm()
    if form.validate_on_submit():
        new_lure=Lure(user_id=g.user.id,
                      name=form.name.data,
                      brand=form.brand.data,
                      color=form.color.data,
                      size=form.size.data)
        db.session.add(new_lure)
        db.session.commit()
        return redirect(url_for('lure.view_tackle_box', user_id=g.user.id))
    return render_template('tackle_box/add-lure.html', form=form)


@lure_bp.route('/tackle-box/update', methods=["GET"])
@login_required
def update_lure():
    """
    UNFINISHED ROUTE
    
    Handles editing a new lure in a tackle box for a single user. Can update lure name, brand and size

    Authentication:
        - Requires user to be logged in (checked via @login_required) and to be the same user
    
    Arguments:
        - lure_id(int): lure to be updated
    
    GET:
        - Render LureForm
    
    POST: 
        - If for is valid
            - Update lure in database
            - Redirect to view all lures
    
    Returns:
        - Render template showing all lures in tackle box
    """
    return render_template('tackle_box/test.html')