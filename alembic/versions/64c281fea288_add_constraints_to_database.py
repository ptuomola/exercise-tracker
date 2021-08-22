"""Add constraints to database

Revision ID: 64c281fea288
Revises: 61325410ab0a
Create Date: 2021-08-22 20:45:39.315317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64c281fea288'
down_revision = '61325410ab0a'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("""ALTER TABLE exercise_subactivities
                    ALTER COLUMN exercise_id SET NOT NULL, ALTER COLUMN subactivity_id SET NOT NULL""")



def downgrade():
    pass
