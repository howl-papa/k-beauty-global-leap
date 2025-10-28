"""add instagram auth fields to user

Revision ID: 20251028_080000
Revises: 20251028_034256
Create Date: 2025-10-28 08:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20251028_080000'
down_revision: Union[str, None] = '20251028_034256'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add Instagram OAuth fields to users table"""
    # Add Instagram integration columns
    op.add_column('users', sa.Column('instagram_access_token', sa.String(), nullable=True))
    op.add_column('users', sa.Column('instagram_user_id', sa.String(), nullable=True))
    op.add_column('users', sa.Column('instagram_token_expires_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Remove Instagram OAuth fields from users table"""
    # Remove Instagram integration columns
    op.drop_column('users', 'instagram_token_expires_at')
    op.drop_column('users', 'instagram_user_id')
    op.drop_column('users', 'instagram_access_token')
