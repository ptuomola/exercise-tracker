from flask import Blueprint, render_template, request
from flask_login import current_user
from model.exercise import (
    get_duration_of_exercise,
    get_total_num_exercises,
    get_exercises_by_activity,
    get_subactivities_by_exercise,
)

main = Blueprint("main", __name__)


@main.route("/")
def index():
    if not current_user.is_authenticated:
        return render_template("index.html")

    if "days" in request.args:
        days = request.args["days"]
        period = "last " + days + " days"
    else:
        days = None
        period = "all time"

    return render_template(
        "overview.html",
        tot_exercises=get_total_num_exercises(current_user.id, days),
        exercises_by_activity=get_exercises_by_activity(current_user.id, days),
        user=current_user,
        tot_duration=get_duration_of_exercise(current_user.id, days),
        subactivities=get_subactivities_by_exercise(current_user.id, days),
        period=period,
    )
