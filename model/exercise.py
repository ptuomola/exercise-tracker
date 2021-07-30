from .db import db
from flask_login import current_user

def insert_exercise(start_date, start_time, end_date, end_time, description, external_url ):
    db.session.execute("""INSERT INTO exercises (user_id, start_date, start_time, end_date, end_time, description, external_url ) 
                                         VALUES (:user_id, :start_date, :start_time, :end_date, :end_time, :description, :external_url )"""
                    , {"user_id": current_user.id, "start_date" : start_date, "start_time": start_time, "end_date": end_date, 
                       "end_time": end_time, "description": description, "external_url": external_url})
    db.session.commit()

def get_exercises_for_user(user_id):
    return db.session.execute("SELECT * FROM exercises WHERE user_id = :user_id ORDER BY start_date DESC, start_time DESC", {"user_id": user_id})