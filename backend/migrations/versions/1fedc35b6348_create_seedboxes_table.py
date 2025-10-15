"""create seedboxes table

Revision ID: 1fedc35b6348
Revises: dfe3e349c6fe
Create Date: 2025-10-14 21:40:47.017539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1fedc35b6348'
down_revision: Union[str, Sequence[str], None] = 'dfe3e349c6fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'seedboxes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('email_address', sa.String(length=320), nullable=False),
        sa.Column('imap_host', sa.String(length=255), nullable=True),
        sa.Column('imap_port', sa.Integer(), nullable=True),
        sa.Column('imap_username', sa.String(length=320), nullable=True),
        sa.Column('imap_encrypted_password', sa.String(length=255), nullable=True),
        sa.Column('imap_use_ssl', sa.Boolean(), nullable=True, default=True),
        sa.Column('imap_inbox_folder', sa.String(length=255), nullable=True, default="INBOX"),
        sa.Column('imap_spam_folder', sa.String(length=255), nullable=True, default="[Gmail]/Spam"),
        sa.Column('last_status', sa.String(length=255), nullable=True),
        sa.Column('last_checked', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    op.create_index('ix_seedboxes_email_address', 'seedboxes', ['email_address'], unique=False)
    op.create_index('ix_seedboxes_id', 'seedboxes', ['id'], unique=False)
    op.create_index('ix_seedboxes_user_id', 'seedboxes', ['user_id'], unique=False)



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_seedboxes_user_id', table_name='seedboxes')
    op.drop_index('ix_seedboxes_id', table_name='seedboxes')
    op.drop_index('ix_seedboxes_email_address', table_name='seedboxes')
    op.drop_table('seedboxes')
