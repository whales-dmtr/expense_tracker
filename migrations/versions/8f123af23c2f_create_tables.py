"""create tables

Revision ID: 8f123af23c2f
Revises:
Create Date: 2025-06-13 20:13:16.609463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '8f123af23c2f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(length=50),
                  unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False)
    )
    op.create_table(
        'expenses',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('time_created', sa.TIMESTAMP, nullable=False),
        sa.Column('category', sa.String, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(('user_id',), ['users.id'])
    )


def downgrade() -> None:
    op.drop_table('expenses')
    op.drop_table('users')
