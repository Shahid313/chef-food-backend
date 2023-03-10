"""migrations

Revision ID: 29e29f05baba
Revises: 
Create Date: 2023-02-07 00:33:24.011305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29e29f05baba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('customer_name', sa.String(length=100), nullable=True),
    sa.Column('ordered_recipe_name', sa.String(length=200), nullable=True),
    sa.Column('ordered_recipe_picture', sa.String(length=200), nullable=True),
    sa.Column('address', sa.String(length=300), nullable=True),
    sa.Column('order_quantity', sa.Integer(), nullable=True),
    sa.Column('total_price', sa.Integer(), nullable=True),
    sa.Column('delivery_price', sa.Integer(), nullable=True),
    sa.Column('recipe_ingredients', sa.String(length=300), nullable=True),
    sa.Column('chef_name', sa.String(length=300), nullable=True),
    sa.Column('time', sa.String(length=200), nullable=True),
    sa.Column('status', sa.String(length=300), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('role', sa.String(length=200), nullable=True),
    sa.Column('password', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('recipe',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('recipe_name', sa.String(length=300), nullable=True),
    sa.Column('recipe_picture', sa.String(length=300), nullable=True),
    sa.Column('recipe_description', sa.String(length=300), nullable=True),
    sa.Column('recipe_ingredients', sa.String(length=300), nullable=True),
    sa.Column('recipe_price', sa.Integer(), nullable=True),
    sa.Column('delivery_price', sa.Integer(), nullable=True),
    sa.Column('time', sa.String(length=300), nullable=True),
    sa.Column('chef_name', sa.String(length=300), nullable=True),
    sa.Column('added_by', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['added_by'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('recipe_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe')
    op.drop_table('user')
    op.drop_table('order')
    # ### end Alembic commands ###
