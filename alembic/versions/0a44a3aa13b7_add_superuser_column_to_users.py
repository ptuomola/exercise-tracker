"""add superuser column to users

Revision ID: 0a44a3aa13b7
Revises: 240a3c3efd01
Create Date: 2021-07-31 08:21:42.350652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a44a3aa13b7'
down_revision = '240a3c3efd01'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("""ALTER TABLE users ADD COLUMN superuser boolean DEFAULT FALSE""")


def downgrade():
    conn = op.get_bind()
    conn.execute("ALTER TABLE users DROP COLUMN superuser")
