from datetime import date, datetime
from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms.fields import SelectField, SubmitField, TextAreaField, TextField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import Optional, Required, ValidationError
from model.activity import (
    get_activity_by_id,
    get_all_activities_as_tuples,
    get_num_subactivities_by_activity_id,
    get_subactivities_by_activity_id,
)
from model.exercise import (
    delete_exercise_by_id,
    delete_exercise_subactivity_by_id,
    get_exercise_by_id,
    get_exercises_for_user,
    get_subactivities_for_exercise,
    get_subactivity_exercise_by_id,
    insert_exercise,
    insert_exercise_subactivity,
    update_exercise,
    update_exercise_subactivity,
)
from model.user import get_user_by_id

exercises = Blueprint("exercises", __name__)


@exercises.route("/exercises/<int:user_id>")
@login_required
def list_exercises(user_id):
    if not current_user.superuser and user_id != current_user.id:
        abort(401)

    return render_template(
        "exercises/list.html",
        user=get_user_by_id(user_id),
        exercises=get_exercises_for_user(user_id),
    )


class ExerciseForm(FlaskForm):
    activity_id = SelectField("Activity", coerce=int)
    start_date = DateField("Start date", validators=[Required()])
    start_time = TimeField("Start time", validators=[Optional()])
    end_date = DateField("End date", [Optional()])
    end_time = TimeField("End time", [Optional()])
    description = TextAreaField("Description")
    external_url = TextField("External URL link")
    submit = SubmitField("Record exercise")
    cancel = SubmitField(label="Cancel", render_kw={"formnovalidate": True})

    def validate_start_date(form, _field):
        if form.start_date.data > date.today():
            raise ValidationError("Start date cannot be in the future")

    def validate_end_date(form, _field):
        if form.end_date.data < form.start_date.data:
            raise ValidationError("End date cannot be before start date")

        if form.end_date.data > date.today():
            raise ValidationError("End date cannot be in the future")

    def validate_end_time(form, _field):
        if (form.end_date.data == form.start_date.data) and (
            form.end_time.data < form.start_time.data
        ):
            raise ValidationError("Exercise cannot end before it starts")


@exercises.route("/exercise")
@login_required
def exercise():
    form = ExerciseForm()
    form.activity_id.choices = get_all_activities_as_tuples()

    form.start_date.data = date.today()
    form.start_time.data = datetime.now()
    form.end_date.data = form.start_date.data

    return render_template("exercises/create.html", form=form)


@exercises.route("/exercise", methods=["POST"])
@login_required
def exercise_post():
    form = ExerciseForm(request.form)
    form.activity_id.choices = get_all_activities_as_tuples()

    if form.cancel.data:
        return redirect(url_for("exercises.list_exercises", user_id=current_user.id))

    if not form.validate():
        return render_template("exercises/create.html", form=form)

    exercise_id = insert_exercise(
        form.activity_id.data,
        form.start_date.data,
        form.start_time.data,
        form.end_date.data,
        form.end_time.data,
        form.description.data,
        form.external_url.data,
    )

    activity = get_activity_by_id(form.activity_id.data)

    if (
        activity.activity_type == 2
        and get_num_subactivities_by_activity_id(activity.id) != 0
    ):
        return redirect(url_for("exercises.subactivities", exercise_id=exercise_id))

    return redirect(url_for("exercises.list_exercises", user_id=current_user.id))


@exercises.route("/exercise/<int:exercise_id>")
@login_required
def detail(exercise_id):
    this_exercise = get_exercise_by_id(exercise_id)

    # only superuser can view exercises of others
    if not current_user.superuser and this_exercise.user_id != current_user.id:
        abort(401)

    return render_template(
        "exercises/detail.html",
        exercise=this_exercise,
        activity=get_activity_by_id(this_exercise.activity_id),
    )


@exercises.route("/exercise/<int:exercise_id>", methods=["DELETE"])
@login_required
def delete(exercise_id):
    this_exercise = get_exercise_by_id(exercise_id)

    # only superuser can delete other users' activities
    if not current_user.superuser and this_exercise.user_id != current_user.id:
        abort(401)

    delete_exercise_by_id(exercise_id)
    return "OK"


class UpdateExerciseForm(FlaskForm):
    start_date = DateField("Start date", validators=[Required()])
    start_time = TimeField("Start time", validators=[Optional()])
    end_date = DateField("End date", [Optional()])
    end_time = TimeField("End time", [Optional()])
    description = TextAreaField("Description")
    external_url = TextField("External URL link")
    submit = SubmitField("Update exercise")
    cancel = SubmitField(label="Cancel", render_kw={"formnovalidate": True})

    def validate_start_date(form, _field):
        if form.start_date.data > date.today():
            raise ValidationError("Start date cannot be in the future")

    def validate_end_date(form, _field):
        if form.end_date.data < form.start_date.data:
            raise ValidationError("End date cannot be before start date")

        if form.end_date.data > date.today():
            raise ValidationError("End date cannot be in the future")

    def validate_end_time(form, _field):
        if (form.end_date.data == form.start_date.data) and (
            form.end_time.data < form.start_time.data
        ):
            raise ValidationError("Exercise cannot end before it starts")


@exercises.route("/exercise/<int:exercise_id>/edit")
@login_required
def edit_exercise(exercise_id):
    this_exercise = get_exercise_by_id(exercise_id)
    form = UpdateExerciseForm()

    # only superuser can view / modify exercises of other users
    if not current_user.superuser and this_exercise.user_id != current_user.id:
        abort(401)

    form.start_date.data = this_exercise.start_date
    form.start_time.data = this_exercise.start_time
    form.end_date.data = this_exercise.end_date
    form.end_time.data = this_exercise.end_time
    form.description.data = this_exercise.description
    form.external_url.data = this_exercise.external_url

    return render_template(
        "exercises/edit.html",
        form=form,
        exercise=this_exercise,
        activity=get_activity_by_id(this_exercise.activity_id),
    )



@exercises.route("/exercise/<int:exercise_id>/edit", methods=["POST"])
@login_required
def edit_exercise_post(exercise_id):
    form = UpdateExerciseForm(request.form)

    if form.cancel.data:
        return redirect(url_for("exercises.detail", exercise_id=exercise_id))

    this_exercise = get_exercise_by_id(exercise_id)

    if not form.validate():
        return render_template(
            "exercises/edit.html",
            form=form,
            exercise=this_exercise,
            activity=get_activity_by_id(this_exercise.activity_id),
        )

    # only superuser can view / modify activities
    if not current_user.superuser and this_exercise.user_id != current_user.id:
        abort(401)

    update_exercise(
        exercise_id,
        form.start_date.data,
        form.start_time.data,
        form.end_date.data,
        form.end_time.data,
        form.description.data,
        form.external_url.data,
    )

    return redirect(url_for("exercises.detail", exercise_id=exercise_id))



@exercises.route("/exercise/<int:exercise_id>/subactivities")
@login_required
def subactivities(exercise_id):
    this_exercise = get_exercise_by_id(exercise_id)

    # only superuser can view / modify exercises of other users
    if not current_user.superuser and this_exercise.user_id != current_user.id:
        abort(401)

    return render_template(
        "exercises/subactivities.html",
        subactivities=get_subactivities_for_exercise(exercise_id),
        subactivity_types=list(
            get_subactivities_by_activity_id(this_exercise.activity_id)
        ),
        exercise=this_exercise,
        current_user=current_user,
    )



@exercises.route("/exercise/<int:exercise_id>/subactivity", methods=["POST"])
@login_required
def post_subactivity(exercise_id):
    this_exercise = get_exercise_by_id(exercise_id)

    # only superuser can view / modify exercises of other users
    if not current_user.superuser and this_exercise.user_id != current_user.id:
        abort(401)

    return str(
        insert_exercise_subactivity(
            this_exercise.id, request.form["id"], request.form["amount"]
        )
    )



@exercises.route(
    "/exercise/<int:exercise_id>/subactivity/<int:subactivity_id>", methods=["DELETE"]
)
@login_required
def delete_subactivity(exercise_id, subactivity_id):
    this_exercise = get_exercise_by_id(exercise_id)

    # only superuser can view / modify exercises of other users
    if not current_user.superuser and this_exercise.user_id != current_user.id:
        abort(401)

    # check that the subactivity belongs to this exercise
    subactivity = get_subactivity_exercise_by_id(subactivity_id)

    if subactivity.exercise_id != exercise_id:
        abort(404)

    delete_exercise_subactivity_by_id(subactivity_id)
    return "OK"



@exercises.route(
    "/exercise/<int:exercise_id>/subactivity/<int:subactivity_id>", methods=["PUT"]
)
@login_required
def update_subactivity(exercise_id, subactivity_id):
    this_exercise = get_exercise_by_id(exercise_id)

    # only superuser can view / modify exercises of other users
    if not current_user.superuser and this_exercise.user_id != current_user.id:
        abort(401)

    # check that the subactivity belongs to this exercise
    subactivity = get_subactivity_exercise_by_id(subactivity_id)

    if subactivity.exercise_id != exercise_id:
        abort(404)

    update_exercise_subactivity(
        subactivity_id, request.form["id"], request.form["amount"]
    )
    return "OK"
