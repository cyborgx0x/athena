"""init

Revision ID: 1c020f300db3
Revises: 
Create Date: 2023-03-24 01:46:21.257215

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1c020f300db3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('core_user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('facebook', sa.String(length=50), nullable=True),
    sa.Column('name', sa.Unicode(length=256), nullable=True),
    sa.Column('user_name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('avatar', sa.String(length=200), nullable=True),
    sa.Column('about_me', sa.JSON(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fiction',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.Unicode(length=300), nullable=True),
    sa.Column('tag', sa.JSON(), nullable=True),
    sa.Column('status', sa.Unicode(length=125), nullable=True),
    sa.Column('short_desc', sa.String(length=160), nullable=True),
    sa.Column('desc', sa.JSON(), nullable=True),
    sa.Column('cover_data', sa.Unicode(length=300), nullable=True),
    sa.Column('cover', sa.Text(), nullable=True),
    sa.Column('download', sa.Unicode(length=500), nullable=True),
    sa.Column('view', sa.Integer(), nullable=True),
    sa.Column('created_by', postgresql.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['core_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chapter',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('short_desc', sa.String(length=160), nullable=True),
    sa.Column('content', sa.JSON(), nullable=True),
    sa.Column('fiction_id', postgresql.UUID(), nullable=True),
    sa.Column('created_by', postgresql.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['core_user.id'], ),
    sa.ForeignKeyConstraint(['fiction_id'], ['fiction.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chapter')
    op.drop_table('fiction')
    op.drop_table('core_user')
    # ### end Alembic commands ###
