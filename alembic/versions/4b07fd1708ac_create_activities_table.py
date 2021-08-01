"""create activities table

Revision ID: 4b07fd1708ac
Revises: 618fbbb28c7f
Create Date: 2021-08-01 09:24:32.922574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b07fd1708ac'
down_revision = '618fbbb28c7f'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("""CREATE TABLE activities (id SERIAL PRIMARY KEY, 
                                             description VARCHAR NOT NULL, 
                                             activity_type INT NOT NULL)""")
    conn.execute("""ALTER TABLE exercises 
                         ADD COLUMN activity_id INT NOT NULL,
                         ADD CONSTRAINT fk_activity_id 
                         FOREIGN KEY (activity_id)
                         REFERENCES activities (id)""")


def downgrade():
    conn = op.get_bind()
    conn.execute("ALTER TABLE exercises DROP CONSTRAINT fk_activity_id, DROP COLUMN activity_id")
    conn.execute("DROP TABLE activities")