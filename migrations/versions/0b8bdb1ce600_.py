"""empty message

Revision ID: 0b8bdb1ce600
Revises: 9909d7ae85eb
Create Date: 2018-02-26 17:47:24.692236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b8bdb1ce600'
down_revision = '9909d7ae85eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('school_name', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'course', 'school', ['school_name'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_column('course', 'school_name')
    # ### end Alembic commands ###
