"""make campaign name nullable

Revision ID: a3974eb19130
Revises: 1fedc35b6348
Create Date: 2025-10-15 01:15:56.108577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a3974eb19130'
down_revision: Union[str, Sequence[str], None] = '1fedc35b6348'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('campaigns', 'name',
               existing_type=sa.String(),
               nullable=True)


def downgrade():
    op.alter_column('campaigns', 'name',
               existing_type=sa.String(),
               nullable=False)
