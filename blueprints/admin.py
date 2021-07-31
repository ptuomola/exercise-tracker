from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from model.user import get_all_users

admin = Blueprint('admin', __name__)

@login_required
@admin.route('/users')
def list_users():
    if not current_user.superuser:
        abort(401)

    return render_template('admin/list_users.html', users=get_all_users())

