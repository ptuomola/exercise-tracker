from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user, logout_user
from model.user import get_all_users, get_user_by_id, delete_user_by_id

users = Blueprint("users", __name__)


@users.route("/users")
@login_required
def list_users():
    # only superuser can list all users
    if not current_user.superuser:
        abort(401)

    return render_template("users/list.html", users=get_all_users())


@users.route("/user/<int:user_id>")
@login_required
def detail(user_id):
    # only superuser can view other users
    if not current_user.superuser and user_id != current_user.id:
        abort(401)

    return render_template(
        "users/detail.html", current_user=current_user, user=get_user_by_id(user_id)
    )

@users.route("/user/<int:user_id>", methods=["DELETE"])
@login_required
def delete(user_id):
    # only superuser can delete other users
    if not current_user.superuser and user_id != current_user.id:
        abort(401)

    delete_user_by_id(user_id)

    if user_id == current_user.id:
        logout_user()

    return "OK"
