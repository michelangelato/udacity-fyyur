"""change Venue website to website_link

Revision ID: 2d88b075cef0
Revises: 4d8478f31d89
Create Date: 2023-11-26 12:06:33.967552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d88b075cef0'
down_revision = '4d8478f31d89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website_link', sa.String(length=120), nullable=True))
        batch_op.drop_column('website')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
        batch_op.drop_column('website_link')

    # ### end Alembic commands ###