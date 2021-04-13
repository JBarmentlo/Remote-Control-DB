"""empty message

Revision ID: 11c6d12d6afd
Revises: acf105bd2d66
Create Date: 2021-04-13 12:00:13.515258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11c6d12d6afd'
down_revision = 'acf105bd2d66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('task', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'task')
    # ### end Alembic commands ###