"""add default superuser account

Revision ID: c0c0d5686346
Revises: 0a44a3aa13b7
Create Date: 2021-07-31 08:25:39.119908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0c0d5686346'
down_revision = '0a44a3aa13b7'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("""INSERT INTO users (email, password, superuser) VALUES ('admin', 'sha256$9Bi9zH34tytRzkHr$7b507fbef13a79e9822202bd9451bb82bd4b9c56bc557fda671786edd33a60b4', TRUE)""")


def downgrade():
    conn = op.get_bind()
    conn.execute("DELETE FROM users WHERE email = 'admin'")
