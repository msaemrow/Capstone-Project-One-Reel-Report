from flask import Blueprint, render_template, redirect, url_for, g, request, flash
from models import FishCatch, User, db, FishSpecies, Lake, Lure
from forms import NewFishCatch, UpdateFishCatch
from helpers import login_required
from sqlalchemy.exc import IntegrityError



catch_bp = Blueprint('catch', __name__)

#########################  Fish Catch Routes #####################################
@catch_bp.route('/fishcatch/add', methods=["GET", "POST"])
@login_required
def add_fish_catch():
    """
    Handle adding a new fish catch.

    Authentication:
        - Requires user to be logged; checked via @login_required
    
    Arguments:
        - None
    
    GET:
        - Render NewFishCatch Form with species, lake, and lure choices popualate
    
    POST:
        - Validate the form.
        - Create a new fish catch entry in the database.
        - Increment the user's catch total.
        - Handle any integrity errors during the database transaction.
    
    Forms:
        - NewFishCatch
    
    Functions:
        - FishCatch.new_fish_catch(), User.increment_user_catch_total()
    
    Returns:
        - Renders template with NewFishCatch form
        - On successful form submission, redirect to user profile page
        - On failed form submission, re-render NewFishCatch form with error message.

    """
    form = NewFishCatch()
    lakes = Lake.query.all()
    all_species = db.session.query(FishSpecies).order_by(FishSpecies.name).all()
    lures = Lure.query.filter_by(user_id=g.user.id).all()
    form.species.choices = [(str(species.id), species.name) for species in all_species]
    form.lake.choices = [(str(lake.id), str(lake.name + ' - ' +lake.closest_town)) for lake in lakes]
    form.lure.choices = [(str(lure.id), str(lure.size + ' ' + lure.name + ' -- ' + lure.color)) for lure in lures]

    if form.validate_on_submit():
        try:
            new_catch = FishCatch.new_fish_catch(form.species.data,
                                g.user.id,
                                form.lake.data,
                                form.length.data,
                                form.weight.data,
                                form.date.data,
                                form.time.data,
                                form.lure.data,
                                form.fish_image.data)     
            db.session.commit()
            
        except IntegrityError as e:
            flash(f"Error adding catch. Please try again Error: {e}", 'danger')
            return render_template('/fish_catch/new-catch.html', form=form)
        
        User.increment_user_catch_total(g.user.id)
        flash(f"Successfully added {new_catch.species.name}", 'success')
        return redirect(url_for('user.view_user', user_id=g.user.id))
        
    else:
        return render_template('/fish_catch/new-catch.html', form=form)

@catch_bp.route('/fishcatch/view/<int:user_id>')
@login_required
def view_fish_catches(user_id):
    """
    Handle all fish catches for a logged in user.

    Authentication:
        - Requires user to be logged; checked via @login_required
    
    Arguments:
        - user_id(int): The id of the user whose fish catches are to be viewed
   
    GET:
        - Retrieve all fish catches for the specified user, ordered by catch date in descending order.
        - Render the template to display all fish catches for the user.
    
    Returns:
        - Renders template for viewing all fish catches for one user
    """
    user_catches = FishCatch.query.filter_by(user_id=user_id).order_by(FishCatch.catch_date.desc()).all()
    user = db.session.get(User, user_id)
    return render_template('/fish_catch/view-all.html', user_catches=user_catches, user=user)

@catch_bp.route('/fishcatch/view/<int:user_id>/<int:catch_id>')
@login_required
def view_single_fish_catch(user_id, catch_id):
    """
    Handle viewing a single fish catch.

    Authentication:
        - Requires user to be logged; checked via @login_required

    Arguments:
        - catch_id(int): id of the fish catch to be viewed

    GET:
        - Retrieve all information for fish catch.
        - Render the template to display fish catch.

    Returns:
        - Renders template for viewing fish catch
        
    """
    catch = db.session.get(FishCatch, catch_id)
    user = db.session.get(User, user_id)
    return render_template('/fish_catch/view-one.html', catch=catch, user=user)

@catch_bp.route('/fishcatch/edit/<int:catch_id>', methods=["GET", "POST"])
@login_required
def edit_fish_catch(catch_id):
    """
    Handle editing a new fish catch.
    Can edit species_id, lake_id, length, weight, and fish_image

    Authentication:
        - Requires user to be logged; checked via @login_required
    
    Arguments:
        - catch_id(int): id of fish catch to be edited
    
    GET:
        - Render UpdateFishCatch Form with existing data for catch
    
    POST:
        - Validate the form.
        - Update catch information in database
        - Render template for single fish catch
    
    Forms:
        - UpdateFishCatch
    
    Returns:
        - Renders template with UpdateFishCatch form
        - On successful form submission, redirect to fish catch page
    
    """
    catch = db.session.get(FishCatch, catch_id)
    form = UpdateFishCatch(obj=catch)
    lakes = Lake.query.all()
    all_species = db.session.query(FishSpecies).order_by(FishSpecies.name).all()
    form.species.choices = [(str(species.id), species.name) for species in all_species]
    form.lake.choices = [(str(lake.id), str(lake.name + ' - ' +lake.closest_town)) for lake in lakes]

    if form.validate_on_submit():
        catch.species_id=form.species.data        
        catch.lake_id=form.lake.data
        catch.length=form.length.data
        catch.weight=form.weight.data
        catch.fish_image=form.fish_image.data
        db.session.add(catch)
        db.session.commit()
        return redirect(url_for('catch.view_single_fish_catch', catch_id=catch.id))
    form.species.process_data(str(catch.species_id))
    form.lake.process_data(str(catch.lake_id))
    return render_template('/fish_catch/edit-catch.html', form=form, fish_catch=catch)

@catch_bp.route('/fishcatch/delete/<int:catch_id>', methods=["POST"])
@login_required
def delete_fish_catch(catch_id):
    """
    Handles deleting a single fish catch

    Authentication:
        - Requires user to be logged; checked via @login_required
    
    Arguments:
        - catch_id(int): id of fish catch to be deleted
    
    POST:
        - Query database for fish catch.
        - Delete fish catch from database.
        - Reduce the fish catch total for the user by 1
        - Render template for view all fish catches
    
    Functions:
        - User.decrement_user_catch_total()
    
    Returns:
        - On deletion, redirect to all fish catches page or the previous url

    """
    catch = db.session.get(FishCatch, catch_id) 
    db.session.delete(catch)
    db.session.commit()
    User.decrement_user_catch_total(g.user.id)
    prev_URL = request.referrer
    if prev_URL and prev_URL != request.url:
            return redirect(prev_URL)
    return redirect(url_for('catch.view_fish_catches', user_id=g.user.id))
