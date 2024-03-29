"""init

Revision ID: dd7424f2e9cf
Revises: 
Create Date: 2023-02-19 00:21:28.280783

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import geoalchemy2
# revision identifiers, used by Alembic.
revision = 'dd7424f2e9cf'
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
    sa.Column('user_type', sa.Enum('PATIENT', 'CAREGIVER', name='eusertype'), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('location', geoalchemy2.types.Geometry(geometry_type='POINT', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # with op.batch_alter_table('user', schema=None) as batch_op:
        # batch_op.create_index('idx_user_location', ['location'], unique=False, postgresql_using='gist')

    op.create_table('agenda',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('repeat_interval', sa.Interval(), nullable=True),
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
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('body', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userLocations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POINT', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('location_name', sa.String(), nullable=True),
    sa.Column('additional_info', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # with op.batch_alter_table('userLocations', schema=None) as batch_op:
        # batch_op.create_index('idx_userLocations_geom', ['geom'], unique=False, postgresql_using='gist')

    op.create_table('user_contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('relation', sa.Enum('basic', 'close', name='erelationlevel'), nullable=True),
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('memory_picture')
    op.drop_table('caregiverMemory')
    op.drop_table('userfaces')
    op.drop_table('user_contacts')
    with op.batch_alter_table('userLocations', schema=None) as batch_op:
        batch_op.drop_index('idx_userLocations_geom', postgresql_using='gist')

    op.drop_table('userLocations')
    op.drop_table('notifications')
    op.drop_table('memory')
    op.drop_table('calendar')
    op.drop_table('agenda')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('idx_user_location', postgresql_using='gist')

    op.drop_table('user')
    op.drop_table('faces')
    # ### end Alembic commands ###
