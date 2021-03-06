"""create_table

Revision ID: 9d87421f5dd8
Revises:
Create Date: 2021-11-30 01:04:10.564048

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '9d87421f5dd8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('wishlists',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('priority', sa.String(
                        length=1000), nullable=False),
                    sa.Column('number_of_buy', sa.String(
                        length=1000), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('buyers',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('wishlist_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['wishlist_id'], ['wishlists.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('buyers')
    op.drop_table('wishlists')
    op.drop_table('products')
    # ### end Alembic commands ###
