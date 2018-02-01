"""empty message

Revision ID: 76461081b9ca
Revises: 
Create Date: 2018-02-01 11:40:23.196902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76461081b9ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('add_time', sa.DATETIME(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=512), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id')
    )
    op.create_table('goods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('good_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=512), nullable=True),
    sa.Column('good_tag', sa.String(length=128), nullable=True),
    sa.Column('chap_num', sa.Integer(), nullable=True),
    sa.Column('price', sa.String(length=512), nullable=True),
    sa.Column('old_price', sa.String(length=512), nullable=True),
    sa.Column('start', sa.Integer(), nullable=True),
    sa.Column('discount', sa.String(length=4), nullable=True),
    sa.Column('ad_time', sa.DATETIME(), nullable=True),
    sa.Column('view_num', sa.Integer(), nullable=True),
    sa.Column('comment_num', sa.Integer(), nullable=True),
    sa.Column('course_info', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['good_tag'], ['tag.name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('good_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('buycar',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('add_time', sa.DATETIME(), nullable=True),
    sa.Column('goods', sa.String(length=512), nullable=True),
    sa.Column('goods_id', sa.Integer(), nullable=True),
    sa.Column('users', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['goods'], ['goods.name'], ),
    sa.ForeignKeyConstraint(['goods_id'], ['goods.good_id'], ),
    sa.ForeignKeyConstraint(['users'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collect',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('add_time', sa.DATETIME(), nullable=True),
    sa.Column('goods', sa.String(length=512), nullable=True),
    sa.Column('good_id', sa.Integer(), nullable=True),
    sa.Column('users', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['good_id'], ['goods.good_id'], ),
    sa.ForeignKeyConstraint(['goods'], ['goods.name'], ),
    sa.ForeignKeyConstraint(['users'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('add_time', sa.DATETIME(), nullable=True),
    sa.Column('fab', sa.Integer(), nullable=True),
    sa.Column('replay', sa.Text(), nullable=True),
    sa.Column('comment_good_id', sa.Integer(), nullable=True),
    sa.Column('users', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['comment_good_id'], ['goods.good_id'], ),
    sa.ForeignKeyConstraint(['users'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('add_time', sa.DATETIME(), nullable=True),
    sa.Column('goods_id', sa.Integer(), nullable=True),
    sa.Column('goods_name', sa.String(length=512), nullable=True),
    sa.Column('num', sa.Integer(), nullable=True),
    sa.Column('orderId', sa.Integer(), nullable=True),
    sa.Column('user', sa.String(length=128), nullable=True),
    sa.Column('price', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['goods_id'], ['goods.good_id'], ),
    sa.ForeignKeyConstraint(['goods_name'], ['goods.name'], ),
    sa.ForeignKeyConstraint(['orderId'], ['orders.order_id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('detail')
    op.drop_table('comment')
    op.drop_table('collect')
    op.drop_table('buycar')
    op.drop_table('goods')
    op.drop_table('orders')
    # ### end Alembic commands ###
