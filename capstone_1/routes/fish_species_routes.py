from flask import Blueprint, render_template, redirect, url_for, g, flash
from models import FishSpecies, User, db
from forms import AddFishSpeciesForm, UpdateFishSpeciesForm
from helpers import login_required


species_bp = Blueprint('species', __name__)

#########################  Fish Species Routes #####################################
@species_bp.route('/fishspecies/view-all')
@login_required
def view_fish_species():
    """
    Handles viewing all fish species

    Authentication:
        - Requires user to be logged; checked via @login_required
        - If admin user, will also see edit and delete options
    
    Arguments:
        - None
    
    GET:
        - If g.user doesn't have admin permissions, render template without edit/delete
        - Otherwise render template with edit/delete options
    
    Functions:
        - None
    
    Returns:
        - Template to view all fish species

    """
    species_list = db.session.query(FishSpecies).order_by(FishSpecies.name).all()
    if g.user.is_admin is False:
        return render_template('fish_species/view-all.html', species_list=species_list)

    return render_template('fish_species/view-all-admin.html', species_list=species_list)

@species_bp.route('/fishspecies/edit/<int:species_id>', methods=["GET", "POST"])
@login_required
def edit_fish_species(species_id):
    """
    Handles editing a fish species. Can edit the name of the fish and master angler length

    Authentication:
        - Requires user to be logged in (checked via @login_required) and an admin user (check via g.user permissions)
    
    Arguments:
        - species_id(int): id of fish species to be edited
    
    GET:
        - Verify that g.user has admin permissions
        - If so, render edit fish form
        - If user does not have permissions, redirect to home page and flash unauhtorized message

    POST:
        - If form is valid, update fish species information in database
        - Redirect to fish species list
    
    Forms:
        - UpdateFishSpeciesForm
            - Existing data is prepopulated
    
    Returns:
        - Render update fish species form
        - On successful update, redirect to all fish species page
    """
    if g.user.is_admin is True:
        species = db.session.get(FishSpecies, species_id)
        form = UpdateFishSpeciesForm(obj=species)

        if form.validate_on_submit():
            species.name = form.new_species_name.data
            species.master_angler_length=form.master_angler_length.data
            db.session.add(species)
            db.session.commit()
            return redirect(url_for('species.view_fish_species'))

        return render_template('fish_species/edit.html', form=form, species=species)
    flash("You are not authorized to complete that action", 'danger')
    return redirect(url_for('home.home'))

@species_bp.route('/fishspecies/delete/<int:species_id>', methods=["POST"])
@login_required
def delete_fish_species(species_id):
    """
    Handles deleting a fish species.

    Authentication:
        - Requires user to be logged in (checked via @login_required) and an admin user (check via g.user permissions)
    
    Arguments:
        - species_id(int): id of fish species to be deleted
    
    POST:
        - Verify g.user has admin permissions
        - Query database for fish
        - Delete fish from database
        - Redirect to fish species list
    
    Returns:
        - If g.user is not an admin, redirect to home page and flash unathorized message
        - On successful deletion, redirect to all fish species page
    """    
    if g.user.is_admin is True:
        species = db.session.get(FishSpecies, species_id)
        db.session.delete(species)
        db.session.commit()
        return redirect(url_for('species.view_fish_species'))
    flash("You are not authorized to complete that action", 'danger')
    return redirect(url_for('home.home'))

@species_bp.route('/fishspecies/add', methods=["GET", "POST"])
@login_required
def add_fish_species():
    """
    Handles adding a new fish species.

    Authentication:
        - Requires user to be logged in (checked via @login_required) and an admin user (check via g.user permissions)
    
    Arguments:
        - None
    
    GET:
        - Verify that g.user has admin permissions
        - If so, render add fish form
        - If user does not have permissions, redirect to home page and flash unauhtorized message

    POST:
        - If form is valid
            - Add fish species information in database
            - Redirect to fish species list
    
    Forms:
        - AddFishSpeciesForm
    
    Returns:
        - Render add fish species form
        - On successful add, redirect to all fish species page
    """
    if g.user.is_admin is True:
        form=AddFishSpeciesForm()
        if form.validate_on_submit():
            new_species = FishSpecies(name=form.species.data,
                                    master_angler_length=form.master_angler_length.data)
            db.session.add(new_species)
            db.session.commit()
            return redirect(url_for('species.view_fish_species'))
        return render_template('fish_species/add.html', form=form)
    flash("You are not authorized to complete that action", 'danger')
    return redirect(url_for('home.home'))  
