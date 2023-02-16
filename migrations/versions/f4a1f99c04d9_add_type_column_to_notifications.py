"""add type column to notifications

Revision ID: f4a1f99c04d9
Revises: d86e7c845c96
Create Date: 2023-02-02 13:17:31.849162

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f4a1f99c04d9'
down_revision = 'd86e7c845c96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=100), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('user_type',
               existing_type=postgresql.ENUM('PATIENT', 'CAREGIVER', name='eusertype'),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('user_type',
               existing_type=postgresql.ENUM('PATIENT', 'CAREGIVER', name='eusertype'),
               nullable=True)

    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.drop_column('type')

    # ### end Alembic commands ###
