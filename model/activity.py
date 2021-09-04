from .db import db
from flask_login import current_user


def get_all_activities():
    return db.session.execute("SELECT * FROM activities ORDER BY id ASC")


def get_all_activities_as_tuples():
    return [(act.id, act.description) for act in get_all_activities()]


def get_activity_by_id(activity_id):
    return db.session.execute(
        "SELECT * FROM activities WHERE id = :activity_id", {"activity_id": activity_id}
    ).first()


def insert_activity(description, activity_type):
    db.session.execute(
        """INSERT INTO activities (description, activity_type)
                           VALUES (:description, :activity_type)""",
        {"description": description, "activity_type": activity_type},
    )
    db.session.commit()


def update_activity(activity_id, description):
    db.session.execute(
        "UPDATE activities SET description = :description WHERE id = :activity_id",
        {"description": description, "activity_id": activity_id},
    )
    db.session.commit()


def get_subactivities_by_activity_id(activity_id):
    return db.session.execute(
        "SELECT * FROM subactivities WHERE activity_id = :activity_id",
        {"activity_id": activity_id},
    )


def get_num_subactivities_by_activity_id(activity_id):
    return db.session.execute(
        "SELECT COUNT(1) FROM subactivities WHERE activity_id = :activity_id",
        {"activity_id": activity_id},
    ).first()[0]


def insert_subactivity(activity_id, description):
    db.session.execute(
        """INSERT INTO subactivities (activity_id, description)
                              VALUES (:activity_id, :description)""",
        {"activity_id": activity_id, "description": description},
    )
    db.session.commit()


def update_subactivity(subactivity_id, description):
    db.session.execute(
        "UPDATE subactivities SET description = :description WHERE id = :subactivity_id",
        {"description": description, "subactivity_id": subactivity_id},
    )
    db.session.commit()


def get_subactivity_by_id(subactivity_id):
    return db.session.execute(
        "SELECT * FROM subactivities WHERE id = :subactivity_id",
        {"subactivity_id": subactivity_id},
    ).first()
