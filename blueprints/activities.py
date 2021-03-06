from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, TextField
from wtforms.fields.core import SelectField
from wtforms.fields.simple import HiddenField
from wtforms.validators import Required, ValidationError
from model.activity import (
    get_activity_by_description,
    get_activity_by_id,
    get_all_activities,
    get_subactivities_by_activity_id,
    get_subactivity_by_id,
    insert_activity,
    insert_subactivity,
    update_activity,
    update_subactivity,
)

activities = Blueprint("activities", __name__)

# list of supported activity types
activity_types = [(1, "Distance"), (2, "Stationary")]



@activities.route("/activities")
@login_required
def list_activities():
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    return render_template(
        "activities/list.html",
        activities=get_all_activities(),
        activity_types=dict(activity_types),
    )


class CreateActivityForm(FlaskForm):
    description = TextField("Description", [Required()])
    activity_type = SelectField("Activity type", choices=activity_types)
    submit = SubmitField("Create activity")
    cancel = SubmitField(label="Cancel", render_kw={"formnovalidate": True})

    def validate_description(_form, field):
        if get_activity_by_description(field.data):
            raise ValidationError("Activity already exists")



@activities.route("/activity")
@login_required
def activity():
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = CreateActivityForm()
    return render_template("activities/create.html", form=form)


@activities.route("/activity", methods=["POST"])
@login_required
def activity_post():
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = CreateActivityForm(request.form)

    if form.cancel.data:
        return redirect(
            url_for("activities.list_activities", activity_types=activity_types)
        )

    if not form.validate():
        return render_template("activities/create.html", form=form)

    insert_activity(form.description.data, form.activity_type.data)

    return redirect(
        url_for("activities.list_activities", activity_types=activity_types)
    )



@activities.route("/activity/<int:activity_id>")
@login_required
def detail(activity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    return render_template(
        "activities/detail.html",
        activity=get_activity_by_id(activity_id),
        activity_types=dict(activity_types),
        subactivities=get_subactivities_by_activity_id(activity_id),
    )


class UpdateActivityForm(FlaskForm):
    activity_id = HiddenField("Activity ID")
    description = TextField("Description", [Required()])
    submit = SubmitField("Update activity")
    cancel = SubmitField(label="Cancel", render_kw={"formnovalidate": True})

    def validate_description(form, field):
        other_activity = get_activity_by_description(field.data)
        if other_activity and form.activity_id.data != str(other_activity.id):
            raise ValidationError("Activity already exists")



@activities.route("/activity/<int:activity_id>/edit")
@login_required
def edit_activity(activity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = UpdateActivityForm()
    this_activity = get_activity_by_id(activity_id)

    form.activity_id.data = activity_id
    form.description.data = this_activity["description"]

    return render_template(
        "activities/edit.html",
        form=form,
        activity=this_activity,
        activity_types=dict(activity_types),
    )


@activities.route("/activity/<int:activity_id>/edit", methods=["POST"])
@login_required
def edit_activity_post(activity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = UpdateActivityForm(request.form)

    if form.cancel.data:
        return redirect(
            url_for(
                "activities.detail",
                activity_id=activity_id,
                activity=get_activity_by_id(activity_id),
            )
        )

    if not form.validate():
        return render_template(
            "activities/edit.html",
            form=form,
            activity=get_activity_by_id(activity_id),
            activity_types=dict(activity_types),
        )

    update_activity(activity_id, form.description.data)

    return redirect(
        url_for(
            "activities.detail",
            activity_id=activity_id,
            activity=get_activity_by_id(activity_id),
        )
    )


# CONTROLLER FOR SUBACTIVITIES


class CreateSubactivityForm(FlaskForm):
    description = TextField("Description", [Required()])
    submit = SubmitField("Create subactivity")
    cancel = SubmitField(label="Cancel", render_kw={"formnovalidate": True})



@activities.route("/activity/<int:_activity_id>/subactivity")
@login_required
def subactivity(_activity_id):
    # only superuser can view / modify subactivities
    if not current_user.superuser:
        abort(401)

    form = CreateSubactivityForm()
    return render_template("activities/create_subactivity.html", form=form)


@activities.route("/activity/<int:activity_id>/subactivity", methods=["POST"])
@login_required
def subactivity_post(activity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = CreateSubactivityForm(request.form)

    if form.cancel.data:
        return redirect(url_for("activities.detail", activity_id=activity_id))

    if not form.validate():
        return render_template("activities/create_subactivity.html", form=form)

    insert_subactivity(activity_id, form.description.data)

    return redirect(url_for("activities.detail", activity_id=activity_id))


class UpdateSubactivityForm(FlaskForm):
    description = TextField("Description", [Required()])
    submit = SubmitField("Update subactivity")
    cancel = SubmitField(label="Cancel", render_kw={"formnovalidate": True})



@activities.route("/activity/<int:activity_id>/subactivity/<int:subactivity_id>/edit")
@login_required
def edit_subactivity(activity_id, subactivity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = UpdateSubactivityForm()
    this_subactivity = get_subactivity_by_id(subactivity_id)

    form.description.data = this_subactivity["description"]

    return render_template(
        "activities/edit_subactivity.html",
        form=form,
        subactivity=this_subactivity,
        activity=get_activity_by_id(activity_id),
    )


@activities.route(
    "/activity/<int:activity_id>/subactivity/<int:subactivity_id>/edit",
    methods=["POST"],
)
@login_required
def edit_subactivity_post(activity_id, subactivity_id):
    # only superuser can view / modify activities
    if not current_user.superuser:
        abort(401)

    form = UpdateSubactivityForm(request.form)

    if form.cancel.data:
        return redirect(
            url_for("activities.detail", activity_id=activity_id, activity=activity)
        )

    if not form.validate():
        return render_template(
            "activities/edit_subactivity.html",
            form=form,
            subactivity=get_subactivity_by_id(subactivity_id),
            activity=get_activity_by_id(activity_id),
        )

    update_subactivity(subactivity_id, form.description.data)

    return redirect(
        url_for("activities.detail", activity_id=activity_id, activity=activity)
    )
