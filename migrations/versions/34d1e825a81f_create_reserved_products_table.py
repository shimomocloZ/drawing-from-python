"""create_reserved_products_table

Revision ID: 34d1e825a81f
Revises: 9d87421f5dd8
Create Date: 2021-12-02 10:37:27.065112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34d1e825a81f'
down_revision = '9d87421f5dd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reserved_products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=False),
    sa.Column('buyer_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reserved_products')
    # ### end Alembic commands ###
