from os import getenv

from flask import Flask
from flask_bs4 import Bootstrap
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_nav import register_renderer

from blueprints.activities import activities as activities_blueprint
from blueprints.auth import auth as auth_blueprint
from blueprints.exercises import exercises as exercises_blueprint
from blueprints.main import main as main_blueprint
from blueprints.nav import MyBootstrapRenderer, nav
from blueprints.users import users as users_blueprint
from model.db import db
from model.user import get_user_by_id


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = getenv("SECRET_KEY")

    # Work around issue with Heroku Postgres and SQLAlchemy 1.4.x
    uri = getenv("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        # rest of connection code using the connection string `uri`

    # initialise SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # initialise blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(exercises_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(activities_blueprint)

    # initialise flask-login
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        return get_user_by_id(int(userid))

    # initialise CSRF protection
    CSRFProtect(app)

    # initialise Flask-bootstrap
    Bootstrap(app)

    # initialise Navigation
    nav.init_app(app)
    register_renderer(app, "my_bootstrap_renderer", MyBootstrapRenderer)

    return app
