"""Initial migration.

Revision ID: d86e7c845c96
Revises: 
Create Date: 2023-01-30 16:39:47.717302

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd86e7c845c96'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('firstname', sa.String(length=100), nullable=False),
    sa.Column('lastname', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('photo_path', sa.Text(), nullable=True),
    sa.Column('user_type', sa.Enum('PATIENT', 'CAREGIVER', name='eusertype'), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('agenda',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('calendar',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('additional_info', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('long', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('location_name', sa.String(), nullable=True),
    sa.Column('additional_info', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('body', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('relation', sa.Enum('First', 'Second', name='erelationlevel'), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userfaces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('face_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('bio', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['face_id'], ['faces.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userfaces')
    op.drop_table('user_contacts')
    op.drop_table('notifications')
    op.drop_table('locations')
    op.drop_table('calendar')
    op.drop_table('agenda')
    op.drop_table('user')
    op.drop_table('faces')
    # ### end Alembic commands ###