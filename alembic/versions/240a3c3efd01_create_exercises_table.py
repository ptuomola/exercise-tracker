"""create exercises table

Revision ID: 240a3c3efd01
Revises: 669909b506d1
Create Date: 2021-07-30 06:56:28.449189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '240a3c3efd01'
down_revision = '669909b506d1'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("""CREATE TABLE exercises (id SERIAL PRIMARY KEY, 
                                            user_id INTEGER NOT NULL, 
                                            start_date DATE NOT NULL,
                                            start_time TIME, 
                                            end_date DATE,
                                            end_time TIME,  
                                            description VARCHAR, 
                                            external_url VARCHAR, 
                                            CONSTRAINT fk_user_id
                                                FOREIGN KEY(user_id)
                                                    REFERENCES users(id))""")


def downgrade():
    conn = op.get_bind()
    conn.execute("DROP TABLE exercises")
