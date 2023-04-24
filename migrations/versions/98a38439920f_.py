"""empty message

Revision ID: 98a38439920f
Revises: c2721afa9a34
Create Date: 2023-04-22 13:23:53.509538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98a38439920f'
down_revision = 'c2721afa9a34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'create')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('create', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
