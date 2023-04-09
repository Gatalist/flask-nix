"""fix -31

Revision ID: a9f1dd4f804c
Revises: 6ed90d89392f
Create Date: 2023-04-05 19:35:28.353016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9f1dd4f804c'
down_revision = '6ed90d89392f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movies', 'reliases')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('reliases', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
