"""Create User Table

Revision ID: febcf14d12a7
Revises: 
Create Date: 2020-07-09 12:48:39.347886

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'febcf14d12a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer, primary_key=True, index=True),
                    sa.Column('username', sa.String(16), index=True),
                    sa.Column('password', sa.String, index=True))


def downgrade():
    op.drop_table('users')
