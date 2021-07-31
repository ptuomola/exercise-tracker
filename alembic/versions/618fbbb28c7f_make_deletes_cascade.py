"""make deletes cascade

Revision ID: 618fbbb28c7f
Revises: c0c0d5686346
Create Date: 2021-07-31 13:15:04.352594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '618fbbb28c7f'
down_revision = 'c0c0d5686346'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("""ALTER TABLE exercises 
                    DROP CONSTRAINT fk_user_id,
                    ADD CONSTRAINT fk_user_id 
                    FOREIGN KEY (user_id) 
                    REFERENCES users (id) 
                    ON DELETE CASCADE""")

def downgrade():
    pass
