"""empty message

Revision ID: 273854aed62c
Revises: 82cfc63e7b52
Create Date: 2022-07-05 12:08:23.134545

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '273854aed62c'
down_revision = '82cfc63e7b52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_users', sa.Column('requests', sa.Integer(), nullable=False))
    op.drop_column('tb_users', 'requests_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_users', sa.Column('requests_number', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('tb_users', 'requests')
    # ### end Alembic commands ###