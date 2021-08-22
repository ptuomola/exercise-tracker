from flask import Blueprint, render_template, request
from flask_login import current_user
from model.exercise import get_total_num_exercises, get_exercises_by_activity, get_total_num_exercises_in_days, get_exercises_by_activity_in_days

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')

    if "days" in request.args:
        days = request.args["days"]
        tot_exercises = get_total_num_exercises_in_days(current_user.id, days)
        exercises_by_activity = get_exercises_by_activity_in_days(current_user.id, days)
        period = "last " + days + " days"
    else:
        tot_exercises = get_total_num_exercises(current_user.id)
        exercises_by_activity = get_exercises_by_activity(current_user.id)
        period = "all time"

    return render_template("overview.html", 
                            tot_exercises = tot_exercises, 
                            exercises_by_activity = exercises_by_activity,
                            user = current_user, 
                            period = period
                            )