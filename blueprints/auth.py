from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms.fields import (BooleanField, PasswordField, StringField,
                            SubmitField)
from wtforms.validators import (Email, EqualTo, Length, Regexp, Required,
                                ValidationError)
from model.user import get_user_by_email, insert_user

auth = Blueprint("auth", __name__)


class LoginForm(FlaskForm):
    email = StringField("Email address", [Required()])
    password = PasswordField("Password", [Required()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


@auth.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@auth.route("/login", methods=["POST"])
def login_post():
    form = LoginForm(request.form)

    if not form.validate():
        return render_template("login.html", form=form)

    user = get_user_by_email(form.email.data)

    if not user or not check_password_hash(user.password, form.password.data):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("auth.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=form.remember.data)
    return redirect(url_for("exercises.list_exercises", user_id=current_user.id))


class RegistrationForm(FlaskForm):
    name = StringField("Name", [Required(), Length(min=4, max=40)])
    email = StringField("Email address", [Required(), Email()])
    password = PasswordField(
        "Password",
        [
            Required(),
            EqualTo("confirm", message="Passwords must match"),
            Length(min=8, message="Password be at least 8 characters"),
            Regexp("^(?=.*[a-z])", message="Password must have a lowercase character"),
            Regexp("^(?=.*[A-Z])", message="Password must have an uppercase character"),
            Regexp("^(?=.*\\d)", message="Password must contain a number"),
            Regexp(
                "(?=.*[@$!%*#?&])", message="Password must contain a special character"
            ),
        ],
    )
    confirm = PasswordField("Repeat password")
    submit = SubmitField("Signup")

    def validate_email(_form, field):
        if get_user_by_email(field.data):
            raise ValidationError("Email address already exists")


@auth.route("/signup")
def signup():
    form = RegistrationForm()
    return render_template("signup.html", form=form)


@auth.route("/signup", methods=["POST"])
def signup_post():
    form = RegistrationForm(request.form)

    if not form.validate():
        return render_template("signup.html", form=form)

    insert_user(
        form.email.data,
        form.name.data,
        generate_password_hash(form.password.data, method="sha256"),
    )

    flash("Thanks for registering! Please log in")
    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
