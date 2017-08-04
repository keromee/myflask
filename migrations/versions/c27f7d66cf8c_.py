"""empty message

Revision ID: c27f7d66cf8c
Revises: 
Create Date: 2017-08-04 11:33:39.992535

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c27f7d66cf8c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lottery', sa.Column('dates', sa.DateTime(), nullable=True))
    op.add_column('lottery', sa.Column('times', sa.String(length=80), nullable=False))
    op.drop_column('lottery', 'time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lottery', sa.Column('time', mysql.DATETIME(), nullable=False))
    op.drop_column('lottery', 'times')
    op.drop_column('lottery', 'dates')
    # ### end Alembic commands ###