"""add batch_number to campaign_batch

Revision ID: a5fc6488ce19
Revises: 061c18855fea
Create Date: 2025-10-12 01:26:50.345016
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5fc6488ce19'
down_revision: Union[str, Sequence[str], None] = '061c18855fea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('campaign_batches', sa.Column('recipients_count', sa.Integer(), nullable=True))
    op.add_column('campaign_batches', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))

def downgrade():
    op.drop_column('campaign_batches', 'recipients_count')
    op.drop_column('campaign_batches', 'created_at')
