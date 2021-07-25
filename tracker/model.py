from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import getenv

db = SQLAlchemy()
# migrate = Migrate(app, db)
