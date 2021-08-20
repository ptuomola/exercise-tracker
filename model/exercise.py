from .db import db
from flask_login import current_user

def insert_exercise(activity_id, start_date, start_time, end_date, end_time, description, external_url ):
    retval = db.session.execute("""INSERT INTO exercises (activity_id, user_id, start_date, start_time, end_date, end_time, description, external_url ) 
                                         VALUES (:activity_id, :user_id, :start_date, :start_time, :end_date, :end_time, :description, :external_url )
                                         RETURNING id"""
                    , {"activity_id": activity_id, "user_id": current_user.id, "start_date" : start_date, "start_time": start_time, "end_date": end_date, 
                       "end_time": end_time, "description": description, "external_url": external_url})
    db.session.commit()
    return retval.first()[0]

def get_exercises_for_user(user_id):
    return db.session.execute("""SELECT e.*, a.description AS activity_description, a.activity_type AS activity_type
                                 FROM exercises e, activities a 
                                 WHERE user_id = :user_id AND e.activity_id = a.id
                                 ORDER BY start_date DESC, start_time DESC""", {"user_id": user_id})

def get_total_num_exercises(user_id):
    return db.session.execute("SELECT COUNT(1) FROM exercises WHERE user_id = :user_id", {"user_id": user_id}).first()[0]

def get_exercises_by_activity(user_id):
    return db.session.execute("""SELECT a.description, COUNT(1)
                                 FROM activities a, exercises e
                                 WHERE e.activity_id = a.id AND e.user_id = :user_id
                                 GROUP BY a.description""", {"user_id": user_id })

def get_exercise_by_id(exercise_id):
    return db.session.execute("SELECT * FROM exercises WHERE id = :exercise_id", {"exercise_id":exercise_id}).first()

def delete_exercise_by_id(exercise_id):
    db.session.execute("DELETE FROM exercises WHERE id = :exercise_id", {"exercise_id":exercise_id})
    db.session.commit()

def update_exercise(exercise_id, start_date, start_time, end_date, end_time, description, external_url):
    db.session.execute("""UPDATE exercises 
                          SET start_date = :start_date,
                              end_date = :end_date,
                              start_time = :start_time,
                              end_time = :end_time,
                              description = :description,
                              external_url = :external_url
                          WHERE id = :exercise_id""", 
                          {"exercise_id":exercise_id, "start_date":start_date, "start_time":start_time,
                           "end_date":end_date, "end_time":end_time, "description":description, 
                           "external_url":external_url})
    db.session.commit()

def get_subactivities_for_exercise(exercise_id):
    db.session.execute("SELECT * FROM EXERCISE_SUBACTIVITIES WHERE exercise_id = :exercise_id", {"exercise_id": exercise_id})