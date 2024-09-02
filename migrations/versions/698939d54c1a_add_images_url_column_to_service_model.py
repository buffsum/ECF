"""Add images_url column to Service model

Revision ID: 698939d54c1a
Revises: d20a5cfcbc0d
Create Date: 2024-09-02 14:02:55.381402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '698939d54c1a'
down_revision = 'd20a5cfcbc0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.add_column(sa.Column('images_url', sa.PickleType(), nullable=True))
        batch_op.drop_column('images')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.add_column(sa.Column('images', sa.BLOB(), nullable=True))
        batch_op.drop_column('images_url')

    # ### end Alembic commands ###
