"""fix -10

Revision ID: 4056d6652103
Revises: 12033bf1ee4c
Create Date: 2023-03-30 19:21:19.721518

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4056d6652103'
down_revision = '12033bf1ee4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('storage')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('storage',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('create_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='storage_pkey')
    )
    # ### end Alembic commands ###