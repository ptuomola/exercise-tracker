"""create subactivity table

Revision ID: a503fba6e8f4
Revises: 4b07fd1708ac
Create Date: 2021-08-18 05:27:32.072803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a503fba6e8f4'
down_revision = '4b07fd1708ac'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("""CREATE TABLE subactivities (id SERIAL PRIMARY KEY, 
                                                activity_id INT NOT NULL REFERENCES activities ON DELETE CASCADE,
                                                description VARCHAR NOT NULL,
                                                CONSTRAINT fk_activity_id
                                                FOREIGN KEY (activity_id) 
                                                REFERENCES activities (id) 
                                                ON DELETE CASCADE)""")


def downgrade():
    conn = op.get_bind()
    conn.execute("DROP TABLE subactivities")