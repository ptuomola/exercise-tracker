"""create exercise subactivities table

Revision ID: 61325410ab0a
Revises: a503fba6e8f4
Create Date: 2021-08-20 21:16:39.126459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61325410ab0a'
down_revision = 'a503fba6e8f4'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("""CREATE TABLE exercise_subactivities 
                                (id SERIAL PRIMARY KEY, 
                                 exercise_id INT REFERENCES exercises(id) ON DELETE CASCADE, 
                                 subactivity_id INT REFERENCES subactivities(id) ON DELETE CASCADE, 
                                 count INT)""")


def downgrade():
    conn = op.get_bind()
    conn.execute("DROP TABLE exercise_subactivities")
