from .db import db
from flask_login import current_user

def get_all_activities():
    return db.session.execute("SELECT * FROM activities ORDER BY id ASC")

def get_activity_by_id(activity_id):
    return db.session.execute("SELECT * FROM activities WHERE id = :activity_id", {"activity_id":activity_id}).first()

def insert_activity(description, activity_type):
    db.session.execute("""INSERT INTO activities (description, activity_type ) 
                                         VALUES (:description, :activity_type)"""
                    , {"description": description, "activity_type" : activity_type})
    db.session.commit()    

def update_activity(activity_id, description):
    db.session.execute("UPDATE activities SET description = :description WHERE id = :activity_id", {"description": description, "activity_id": activity_id})
    db.session.commit()

