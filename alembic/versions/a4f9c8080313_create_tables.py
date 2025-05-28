"""Create tables

Revision ID: a4f9c8080313
Revises: 
Create Date: 2025-05-28 04:56:19.875550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4f9c8080313'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.create_table(
        'cvs',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('cv', sa.Text, nullable=False),
        sa.Column('job_desc', sa.Text, nullable=False),
    )


def downgrade():
    op.drop_table('cvs')
