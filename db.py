from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import re

# Work around issue with Heroku Postgres and SQLAlchemy 1.4.x
uri = getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app.config["SQLALCHEMY_DATABASE_URI"] = uri
db = SQLAlchemy(app)