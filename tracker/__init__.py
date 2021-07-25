from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from .model import db
from os import getenv
from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = 'f2a76a5a966c46d0b08f4965327a89d6'

    # Work around issue with Heroku Postgres and SQLAlchemy 1.4.x
    uri = getenv("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        # rest of connection code using the connection string `uri`

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app
