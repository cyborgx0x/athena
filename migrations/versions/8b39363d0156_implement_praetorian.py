"""implement praetorian

Revision ID: 8b39363d0156
Revises: 1c020f300db3
Create Date: 2023-03-27 20:38:08.873726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b39363d0156'
down_revision = '1c020f300db3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('core_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True))
        batch_op.add_column(sa.Column('roles', sa.Text(), nullable=True))
        batch_op.drop_column('user_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('core_user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_name', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
        batch_op.drop_column('roles')
        batch_op.drop_column('is_active')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
