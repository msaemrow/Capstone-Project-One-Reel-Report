from flask import Blueprint, render_template, redirect, url_for, g, request, flash, abort
from models import Lake, db
from forms import AddLakeForm, EditLakeForm
from helpers import login_required


lake_bp = Blueprint('lake', __name__)

#########################  Lake Routes #####################################
@lake_bp.route('/lake/view-all')
@login_required
def view_lakes():
    """
    Handles viewing all lakes.

    Authentication:
        - Requires user to be logged in (checked via @login_required)
    
    Arguments:
        - None
    
    GET:
        - Query database and get all lakes
        - Render template to display all lakes

    Forms:
        - None
    
    Returns:
        - Render template showing all lakes
    """
    lakes = db.session.query(Lake).order_by(Lake.state, Lake.name).all()
    if g.user.is_admin is True:
        return render_template('lake/view-all-admin.html', lakes=lakes)
    return render_template('lake/view-all.html', lakes=lakes)

@lake_bp.route('/lake/view/search', methods=['GET'])
@login_required
def search_lakes():
    """
    Handles viewing lakes that meet search criteria.

    Authentication:
        - Requires user to be logged in (checked via @login_required)
    
    Arguments:
        - None
        - Searches based on query string
    
    GET:
        - Get query string
        - Query database with search query string
        - Render template displaying lakes that match query string

    Returns:
        - Render template displaying lakes that match query string
    """
    search_query = request.args.get('search')
    matched_lakes=db.session.query(Lake).filter(Lake.name.ilike(f"%{search_query}%")).order_by(Lake.state, Lake.name).all()
    return render_template('lake/view-search-results.html', lakes=matched_lakes)

@lake_bp.route('/lake/edit/<int:lake_id>', methods=["GET", "POST"])
@login_required
def edit_lake(lake_id):
    """
    Handles editing a lake. Can edit the name, closest town and state

    Authentication:
        - Requires user to be logged in (checked via @login_required) and an admin user (check via g.user permissions)
    
    Arguments:
        - lake_id(int): id of lake to be edited
    
    GET:
        - Verify that g.user has admin permissions
        - If so, render edit lake form
        - If user does not have permissions, redirect to home page and flash unauhtorized message

    POST:
        - If form is valid, update lake information in database
        - Redirect to all lake
    
    Forms:
        - EditLakeForm
            - Existing data is prepopulated
    
    Returns:
        - Render prepopulated update lake form
        - On successful update, redirect to all lakes page
    """
    if g.user.is_admin is True:
        lake = db.session.get(Lake, lake_id)
        form = EditLakeForm(obj=lake)
        if form.validate_on_submit():
            lake.name = form.name.data
            lake.state = form.state.data
            lake.closest_town = form.closest_town.data
            db.session.add(lake)
            db.session.commit()
            return redirect(url_for('lake.view_lakes'))

        return render_template('lake/edit.html', form=form, lake=lake)
    flash("You are not authorized to complete that action", 'danger')
    return redirect(url_for('home.home'))

@lake_bp.route('/lake/delete/<int:lake_id>', methods=["POST"])
@login_required
def delete_lake(lake_id):
    """
    Handles deleting an existing lake.

    Authentication:
        - Requires user to be logged in (checked via @login_required) and an admin user (check via g.user permissions)
    
    Arguments:
        - lake_id(int): id of lake to be edited

    POST:
        - Verify g.user has admin permissions
            - Query database for lake_id
            - Delete lake
            - Redirect to lakes list
        - If g.user does not have admin permissions, redirect to home page and flash unauthorized message

    Returns:
        - On deletion, redirect to all lakes page
    """
    if g.user.is_admin is True:
        lake = db.session.get(Lake, lake_id)
        db.session.delete(lake)
        db.session.commit()
        return redirect(url_for('lake.view_lakes')) 
    flash("You are not authorized to complete that action", 'danger')
    return redirect(url_for('home.home'))

@lake_bp.route('/lake/add', methods=["GET", "POST"])
@login_required
def add_lake():
    """
    Handles adding a new lake.

    Authentication:
        - Requires user to be logged in (checked via @login_required) and an admin user (check via g.user permissions)
    
    GET:
        - Verify that g.user has admin permissions
        - If so, render add lake form
        - If user does not have permissions, redirect to home page and flash unauhtorized message

    POST:
        - If form is valid, 
            - Get latitude and longitude based on form data
            - Create a new lake in database
            - Redirect to all lakes
    
    Forms:
        - AddLakeForm

    Function:
        - Lake.get_lake_lat_long()
    
    Returns:
        - Render add lake form
        - On successful add, redirect to all lakes page
    """
    if g.user.is_admin is True:
        form=AddLakeForm()
        if form.validate_on_submit():
            try:
                lat_long = Lake.get_lake_lat_long(form.closest_town.data, form.state.data)
            except:
                print(f"Error getting lat_long data")
                return render_template('lake/add.html', form=form)
            new_lake = Lake(name=form.name.data,
                            state=form.state.data,
                            closest_town=form.closest_town.data,
                            latitude=lat_long['lat'],
                            longitude=lat_long['lon']
                            )
            db.session.add(new_lake)
            db.session.commit()
            return redirect(url_for('lake.view_lakes'))
        return render_template('lake/add.html', form=form)
    flash("You are not authorized to complete that action", 'danger')
    return redirect(url_for('home.home'))    

@lake_bp.route('/forecast/<int:lake_id>')
@login_required
def view_forecast(lake_id):
    """
    Handles adding a new lake.

    Authentication:
        - Requires user to be logged in (checked via @login_required) and an admin user (check via g.user permissions)
    
    Arguments:
        - lake_id(int): id of lake to get forecast for
    
    GET:
        - Query database for lake
        - Get forecast based on latitude and longitude of lake
        - Render forecast page

    Function:
        - Lake.get_forecast_data()
    
    Returns:
        - Render forecast template
    """
    lake = db.session.query(Lake).get(lake_id)

    lat = lake.latitude
    lon = lake.longitude
    forecast_data = Lake.get_forecast_data(lat, lon)

    return render_template('forecast.html', lake=lake, forecast_data=forecast_data)

