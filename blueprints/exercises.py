from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField, TimeField
from wtforms.fields import TextAreaField, TextField, SubmitField
from wtforms.validators import Required, Optional, ValidationError
from model.exercise import insert_exercise, get_exercises_for_user
from model.user import get_user_by_id
exercises = Blueprint('exercises', __name__)

@exercises.route('/exercises/<int:user_id>')
@login_required
def list(user_id):
    if not current_user.superuser and user_id != current_user.id: 
        abort(401)

    return render_template("exercises/list.html", user = get_user_by_id(user_id), exercises = get_exercises_for_user(user_id))

class ExerciseForm(FlaskForm):
    start_date = DateField("Start date", [Required()])
    start_time = TimeField("Start time", [Optional()])
    end_date = DateField("End date", [Optional(), ])
    end_time = TimeField("End time", [Optional()])
    desription = TextAreaField("Description")
    external_url = TextField("External URL link")
    submit = SubmitField("Record exercise")

    def validate_end_date(form, field):
        print("in validator")

        if form.end_date.data < form.start_date.data:
            raise ValidationError("End date cannot be before start date")


    def validate_end_time(form, field):
        if (form.end_date.data == form.start_date.data) and (form.end_time.data < form.start_time.data):
            raise ValidationError("Exercise cannot end before it starts")


@exercises.route('/exercise')
def exercise():
    form = ExerciseForm()
    return render_template('exercises/create.html', form = form)

@exercises.route('/exercise', methods=['POST'])
def exercise_post():
    form = ExerciseForm(request.form)

    if not form.validate():
        return render_template("exercises/create.html", form = form)

    insert_exercise(form.start_date.data, form.start_time.data, form.end_date.data, form.end_time.data, form.desription.data, form.external_url.data)

    return redirect(url_for("exercises.list"))


