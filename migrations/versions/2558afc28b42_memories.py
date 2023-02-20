"""Memories

Revision ID: 2558afc28b42
Revises: a164cc77ceee
Create Date: 2023-02-16 23:57:27.762827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2558afc28b42'
down_revision = 'a164cc77ceee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('memory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('memo_body', sa.String(), nullable=True),
    sa.Column('memo_date', sa.Date(), nullable=True),
    sa.Column('thumbnail', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('caregiverMemory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('memory_id', sa.Integer(), nullable=True),
    sa.Column('caregiver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caregiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['memory_id'], ['memory.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('memory_picture',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('memory_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['memory_id'], ['memory.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # op.drop_table('spatial_ref_sys')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('spatial_ref_sys',
    # sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    # sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    # sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    # sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    # sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    # sa.CheckConstraint('srid > 0 AND srid <= 998999', name='spatial_ref_sys_srid_check'),
    # sa.PrimaryKeyConstraint('srid', name='spatial_ref_sys_pkey')
    # )
    op.drop_table('memory_picture')
    op.drop_table('caregiverMemory')
    op.drop_table('memory')
    # ### end Alembic commands ###
