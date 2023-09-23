"""updated new actions

Revision ID: f3b1124bdb7b
Revises: 614a4bfa8991
Create Date: 2023-09-23 16:38:10.029135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3b1124bdb7b'
down_revision = '614a4bfa8991'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurants', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_name_constraint', ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurants', schema=None) as batch_op:
        batch_op.drop_constraint('unique_name_constraint', type_='unique')

    # ### end Alembic commands ###
