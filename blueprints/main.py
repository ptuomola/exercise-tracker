from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from model.exercise import get_total_num_exercises, get_exercises_by_activity

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')

    tot_exercises = get_total_num_exercises(current_user.id)
    exercises_by_activity = get_exercises_by_activity(current_user.id)

    return render_template("overview.html", 
                            tot_exercises = tot_exercises, 
                            exercises_by_activity = exercises_by_activity,
                            user = current_user)