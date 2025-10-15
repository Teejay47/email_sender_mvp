"""Add campaigns and batches tables

Revision ID: 7dfee23d6ea2
Revises: 2108834c7d11
Create Date: 2025-10-11 16:35:08.820018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dfee23d6ea2'
down_revision: Union[str, Sequence[str], None] = '2108834c7d11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
