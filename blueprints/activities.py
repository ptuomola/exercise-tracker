from flask import Blueprint, render_template, redirect, url_for, abort, request
from flask_login import login_required, current_user
from wtforms.fields.core import SelectField
from model.activity import get_all_activities, insert_activity, get_activity_by_id, update_activity, get_subactivities_by_activity_id, insert_subactivity, update_subactivity, get_subactivity_by_id
from flask_wtf import FlaskForm
from wtforms.fields import TextField, SubmitField
from wtforms.validators import Required

activities = Blueprint('activities', __name__)
 
# list of supported activity types
activity_types = [(1, "Distance"), (2, "Stationary")]


@login_required
@activities.route('/activities')
def list():
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    return render_template('activities/list.html', activities = get_all_activities(), activity_types = dict(activity_types))


class CreateActivityForm(FlaskForm):
    description = TextField("Description", [Required()])
    activity_type = SelectField("Activity type", choices = activity_types)
    submit = SubmitField("Create activity")
    cancel = SubmitField(label='Cancel', render_kw={'formnovalidate': True})    


@login_required
@activities.route('/activity')
def activity():
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)
    
    form = CreateActivityForm()
    return render_template('activities/create.html', form = form)


@activities.route('/activity', methods=['POST'])
@login_required
def activity_post():
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = CreateActivityForm(request.form)

    if form.cancel.data:
        return redirect(url_for("activities.list",  activity_types = activity_types))

    if not form.validate():
        return render_template("activities/create.html", form = form)

    insert_activity(form.description.data, form.activity_type.data)

    return redirect(url_for("activities.list",  activity_types = activity_types))


@login_required
@activities.route("/activity/<int:activity_id>")
def detail(activity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)
    
    return render_template("activities/detail.html", 
                            activity = get_activity_by_id(activity_id), 
                            activity_types=dict(activity_types),
                            subactivities = get_subactivities_by_activity_id(activity_id))


class UpdateActivityForm(FlaskForm):
    description = TextField("Description", [Required()])
    submit = SubmitField("Update activity")
    cancel = SubmitField(label='Cancel', render_kw={'formnovalidate': True})    

@login_required
@activities.route('/activity/<int:activity_id>/edit')
def edit_activity(activity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = UpdateActivityForm()
    activity = get_activity_by_id(activity_id)

    form.description.data = activity["description"]

    return render_template('activities/edit.html', form = form, activity = activity, activity_types=dict(activity_types))


@activities.route('/activity/<int:activity_id>/edit', methods=['POST'])
@login_required
def edit_activity_post(activity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = UpdateActivityForm(request.form)

    if form.cancel.data:
        return redirect(url_for("activities.detail",  activity_id = activity_id, activity = activity))

    if not form.validate():
        return render_template("activities/edit.html", form = form, activity = get_activity_by_id(activity_id), activity_types=dict(activity_types))

    update_activity(activity_id,form.description.data)

    return redirect(url_for("activities.detail",  activity_id = activity_id, activity = activity))


### CONTROLLER FOR SUBACTIVITIES

class CreateSubactivityForm(FlaskForm):
    description = TextField("Description", [Required()])
    submit = SubmitField("Create subactivity")
    cancel = SubmitField(label='Cancel', render_kw={'formnovalidate': True})    



@login_required
@activities.route('/activity/<int:activity_id>/subactivity')
def subactivity(activity_id):
    # only superuser can view / modify subactivities
    if not current_user.superuser:
        abort(401)
    
    form = CreateSubactivityForm()
    return render_template('activities/create_subactivity.html', form = form)


@activities.route('/activity/<int:activity_id>/subactivity', methods=['POST'])
@login_required
def subactivity_post(activity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = CreateSubactivityForm(request.form)

    if form.cancel.data:
        return redirect(url_for("activities.detail",  activity_id = activity_id))

    if not form.validate():
        return render_template("activities/create_subactivity.html", form = form)

    insert_subactivity(activity_id, form.description.data)

    return redirect(url_for("activities.detail",  activity_id = activity_id))



class UpdateSubactivityForm(FlaskForm):
    description = TextField("Description", [Required()])
    submit = SubmitField("Update subactivity")
    cancel = SubmitField(label='Cancel', render_kw={'formnovalidate': True})    


@login_required
@activities.route('/activity/<int:activity_id>/subactivity/<int:subactivity_id>/edit')
def edit_subactivity(activity_id, subactivity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = UpdateSubactivityForm()
    subactivity = get_subactivity_by_id(subactivity_id)

    form.description.data = subactivity["description"]

    return render_template('activities/edit_subactivity.html', form = form, subactivity = subactivity, activity = get_activity_by_id(activity_id))


@activities.route('/activity/<int:activity_id>/subactivity/<int:subactivity_id>/edit', methods=['POST'])
@login_required
def edit_subactivity_post(activity_id, subactivity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = UpdateSubactivityForm(request.form)

    if form.cancel.data:
        return redirect(url_for("activities.detail",  activity_id = activity_id, activity = activity))
        

    if not form.validate():
        return render_template("activities/edit_subactivity.html", form = form, subactivity = get_subactivity_by_id(subactivity_id), activity = get_activity_by_id(activity_id))

    update_subactivity(subactivity_id,form.description.data)

    return redirect(url_for("activities.detail",  activity_id = activity_id, activity = activity))


