"""create user table

Revision ID: 669909b506d1
Revises: 
Create Date: 2021-07-25 17:20:50.143738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '669909b506d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("create table users (id SERIAL PRIMARY KEY, email VARCHAR NOT NULL, password VARCHAR NOT NULL, name VARCHAR)")


def downgrade():
    conn = op.get_bind()
    conn.execute("DROP TABLE users")
