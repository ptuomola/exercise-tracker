from flask import Blueprint, render_template, redirect, url_for, request, flash
from model.user import get_user_by_email, insert_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from flask_wtf import Form 
from wtforms.fields import SubmitField, StringField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = get_user_by_email(email)

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))

class RegistrationForm(Form):
    name = StringField('Name', [Required(), Length(min=4, max=40)])
    email = StringField('Email address', [Required(), Email()])
    password = PasswordField('Password', [
        Required(), 
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat password')
    submit = SubmitField('Signup')

@auth.route('/signup')
def signup():
    form = RegistrationForm()
    return render_template("signup.html", form=form)

@auth.route('/signup', methods=['POST'])
def signup_post():
    form = RegistrationForm(request.form)

    if not form.validate():
        return render_template("signup.html", form = form)

    if get_user_by_email(form.email.data): 
        flash("Email address already exists")
        return render_template("signup.html", form = form)

    insert_user(form.email.data, form.name.data, generate_password_hash(form.password.data, method='sha256'))

    flash("Thanks for registering! Please log in")
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

