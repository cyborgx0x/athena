"""empty message

Revision ID: a1e8d6f5f8ce
Revises: 
Create Date: 2023-02-24 14:17:04.152746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1e8d6f5f8ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=160), nullable=True),
    sa.Column('short_desc', sa.String(length=160), nullable=True),
    sa.Column('slug', sa.String(length=160), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
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
    op.create_table('collection',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Unicode(length=300), nullable=True),
    sa.Column('tag', sa.Unicode(length=300), nullable=True),
    sa.Column('status', sa.Unicode(length=300), nullable=True),
    sa.Column('short_desc', sa.String(length=160), nullable=True),
    sa.Column('desc', sa.JSON(), nullable=True),
    sa.Column('cover_data', sa.JSON(), nullable=True),
    sa.Column('cover', sa.Text(), nullable=True),
    sa.Column('download', sa.Unicode(length=500), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('view', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('media',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=160), nullable=True),
    sa.Column('short_desc', sa.String(length=160), nullable=True),
    sa.Column('content', sa.JSON(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('view', sa.Integer(), nullable=True),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['collection.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media')
    op.drop_table('collection')
    op.drop_table('user')
    op.drop_table('type')
    # ### end Alembic commands ###
