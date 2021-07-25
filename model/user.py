from flask_login import UserMixin
from .db import db


class User(UserMixin):
    def __init__(self, id, email, name, password):
        self.id = id
        self.email = email
        self.name = name
        self.password = password


def insert_user(email, name, password):
    db.session.execute("INSERT INTO users (email, name, password) VALUES ( :email, :name, :password )", {
                       "email": email, "password": password, "name": name})
    db.session.commit()


def get_user_by_id(id):
    return get_user_from_query(db.session.execute("SELECT id, email, name, password FROM users WHERE id = :id", {"id": id}))


def get_user_by_email(email):
    return get_user_from_query(db.session.execute("SELECT id, email, name, password FROM users WHERE UPPER(email) = UPPER(:email)", {"email": email}))


def get_user_from_query(result):
    row = result.first()

    if row == None:
        return None

    return User(**row)
