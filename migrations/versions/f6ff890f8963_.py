"""empty message

Revision ID: f6ff890f8963
Revises: 
Create Date: 2021-04-13 12:36:34.342567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6ff890f8963'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('task', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('task_id')
    )
    op.create_table('users',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('pas', sa.String(), nullable=True),
    sa.Column('mail', sa.String(), nullable=True),
    sa.Column('authenticated', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('tasks')
    # ### end Alembic commands ###
