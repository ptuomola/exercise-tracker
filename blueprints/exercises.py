from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from sqlalchemy.sql.operators import notbetween_op
from wtforms.fields.html5 import DateField, TimeField
from wtforms.fields import TextAreaField, TextField, SubmitField, SelectField
from wtforms.validators import Required, Optional, ValidationError
from model.activity import get_activity_by_id, get_all_activities_as_tuples, get_num_subactivities_by_activity_id, get_subactivities_by_activity_id, get_subactivity_by_id
from model.exercise import delete_exercise_by_id, delete_exercise_subactivity_by_id, get_subactivity_exercise_by_id, insert_exercise, get_exercises_for_user, get_exercise_by_id, update_exercise, get_subactivities_for_exercise, insert_exercise_subactivity, update_exercise_subactivity
from model.user import get_user_by_id
from blueprints.activities import activity_types
from datetime import date, datetime

exercises = Blueprint('exercises', __name__)

@exercises.route('/exercises/<int:user_id>')
@login_required
def list_exercises(user_id):
    if not current_user.superuser and user_id != current_user.id: 
        abort(401)

    return render_template("exercises/list.html", user = get_user_by_id(user_id), exercises = get_exercises_for_user(user_id))

class ExerciseForm(FlaskForm):
    activity_id = SelectField("Activity", coerce=int)
    start_date = DateField("Start date", validators=[Required()])
    start_time = TimeField("Start time", validators=[Optional()])
    end_date = DateField("End date", [Optional()])
    end_time = TimeField("End time", [Optional()])
    description = TextAreaField("Description")
    external_url = TextField("External URL link")
    submit = SubmitField("Record exercise")
    cancel = SubmitField(label='Cancel', render_kw={'formnovalidate': True})    

    def validate_end_date(form, field):
        if form.end_date.data < form.start_date.data:
            raise ValidationError("End date cannot be before start date")


    def validate_end_time(form, field):
        if (form.end_date.data == form.start_date.data) and (form.end_time.data < form.start_time.data):
            raise ValidationError("Exercise cannot end before it starts")


@exercises.route('/exercise')
def exercise():
    form = ExerciseForm()
    form.activity_id.choices = get_all_activities_as_tuples()

    form.start_date.data = date.today()
    form.start_time.data = datetime.now()
    form.end_date.data = form.start_date.data

    return render_template('exercises/create.html', form = form)

@exercises.route('/exercise', methods=['POST'])
def exercise_post():
    form = ExerciseForm(request.form)
    form.activity_id.choices = get_all_activities_as_tuples()

    if form.cancel.data:
        return redirect(url_for("exercises.list_exercises", user_id = current_user.id))

    if not form.validate():
        return render_template("exercises/create.html", form = form)

    exercise_id = insert_exercise(form.activity_id.data, form.start_date.data, form.start_time.data, form.end_date.data, form.end_time.data, form.description.data, form.external_url.data)

    activity = get_activity_by_id(form.activity_id.data)

    if activity.activity_type == 2 and get_num_subactivities_by_activity_id(activity.id) != 0: 
        return redirect(url_for("exercises.subactivities", exercise_id = exercise_id))

    return redirect(url_for("exercises.list_exercises", user_id = current_user.id))


@login_required
@exercises.route("/exercise/<int:exercise_id>")
def detail(exercise_id):
    exercise = get_exercise_by_id(exercise_id)

    # only superuser can view exercises of others
    if not current_user.superuser and exercise.user_id != current_user.id: 
        abort(401)
    
    return render_template("exercises/detail.html", 
                            exercise = exercise, 
                            activity = get_activity_by_id(exercise.activity_id))

@login_required
@exercises.route("/exercise/<int:exercise_id>", methods = ["DELETE"])
def delete(exercise_id):
    exercise = get_exercise_by_id(exercise_id)

    # only superuser can delete other users' activities
    if not current_user.superuser and exercise.user_id != current_user.id:
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
    cancel = SubmitField(label='Cancel', render_kw={'formnovalidate': True})    

    def validate_end_date(form, field):
        if form.end_date.data < form.start_date.data:
            raise ValidationError("End date cannot be before start date")


    def validate_end_time(form, field):
        if (form.end_date.data == form.start_date.data) and (form.end_time.data < form.start_time.data):
            raise ValidationError("Exercise cannot end before it starts")


@login_required
@exercises.route('/exercise/<int:exercise_id>/edit')
def edit_exercise(exercise_id):
    exercise = get_exercise_by_id(exercise_id)
    form = UpdateExerciseForm()

    # only superuser can view / modify exercises of other users
    if not current_user.superuser and exercise.user_id != current_user.id:
        abort(401)

    form.start_date.data = exercise.start_date
    form.start_time.data = exercise.start_time
    form.end_date.data = exercise.end_date
    form.end_time.data = exercise.end_time
    form.description.data = exercise.description
    form.external_url.data = exercise.external_url

    return render_template('exercises/edit.html', form = form, exercise = exercise, activity = get_activity_by_id(exercise.activity_id))


@login_required
@exercises.route('/exercise/<int:exercise_id>/edit', methods = ['POST'])
def edit_exercise_post(exercise_id):
    form = UpdateExerciseForm(request.form)

    if form.cancel.data:
        return redirect(url_for("exercises.detail",  exercise_id = exercise_id))

    exercise = get_exercise_by_id(exercise_id)

    if not form.validate():
        return render_template('exercises/edit.html', form = form, exercise = exercise, activity = get_activity_by_id(exercise.activity_id))

    # only superuser can view / modify activities
    if not current_user.superuser and exercise.user_id != current_user.id:
        abort(401)

    update_exercise(exercise_id, form.start_date.data, form.start_time.data, form.end_date.data, form.end_time.data, form.description.data, form.external_url.data)

    return redirect(url_for("exercises.detail",  exercise_id = exercise_id))


@login_required
@exercises.route('/exercise/<int:exercise_id>/subactivities')
def subactivities(exercise_id):
    exercise = get_exercise_by_id(exercise_id)

    # only superuser can view / modify exercises of other users
    print(current_user.id)
    print(exercise.user_id)
    if not current_user.superuser and exercise.user_id != current_user.id:
        abort(401)

    return render_template('exercises/subactivities.html', 
                            subactivities = get_subactivities_for_exercise(exercise_id), 
                            subactivity_types = list(get_subactivities_by_activity_id(exercise.activity_id)),
                            exercise = exercise,
                            current_user = current_user)

@login_required
@exercises.route('/exercise/<int:exercise_id>/subactivity', methods=["POST"])
def post_subactivity(exercise_id):
    exercise = get_exercise_by_id(exercise_id)

    # only superuser can view / modify exercises of other users
    if not current_user.superuser and exercise.user_id != current_user.id:
        abort(401)

    return str(insert_exercise_subactivity(exercise.id, request.form["id"], request.form["amount"]))

@login_required
@exercises.route('/exercise/<int:exercise_id>/subactivity/<int:subactivity_id>', methods=["DELETE"])
def delete_subactivity(exercise_id, subactivity_id):
    exercise = get_exercise_by_id(exercise_id)

    # only superuser can view / modify exercises of other users
    if not current_user.superuser and exercise.user_id != current_user.id:
        abort(401)

    # check that the subactivity belongs to this exercise
    subactivity = get_subactivity_exercise_by_id(subactivity_id)

    if subactivity.exercise_id != exercise_id:
        abort(404)
    
    delete_exercise_subactivity_by_id(subactivity_id)
    return "OK"

@login_required
@exercises.route('/exercise/<int:exercise_id>/subactivity/<int:subactivity_id>', methods=["PUT"])
def update_subactivity(exercise_id, subactivity_id):
    exercise = get_exercise_by_id(exercise_id)

    # only superuser can view / modify exercises of other users
    if not current_user.superuser and exercise.user_id != current_user.id:
        abort(401)

    # check that the subactivity belongs to this exercise
    subactivity = get_subactivity_exercise_by_id(subactivity_id)

    if subactivity.exercise_id != exercise_id:
        abort(404)
    
    update_exercise_subactivity(subactivity_id, request.form["id"], request.form["amount"])
    return "OK"