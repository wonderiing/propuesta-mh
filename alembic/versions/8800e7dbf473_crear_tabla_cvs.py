"""Crear tabla CVs

Revision ID: 8800e7dbf473
Revises: 102b0d455728
Create Date: 2025-02-25 17:41:37.021926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8800e7dbf473'
down_revision: Union[str, None] = '102b0d455728'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'cvs',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('cv', sa.Text(), nullable=True),
        sa.Column('job_dexc', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:
    op.drop_table('cvs')

