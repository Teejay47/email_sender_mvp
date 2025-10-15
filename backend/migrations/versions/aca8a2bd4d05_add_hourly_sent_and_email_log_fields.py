"""Add hourly_sent and email_log fields (idempotent safe operations)

Revision ID: aca8a2bd4d05
Revises: 7dfee23d6ea2
Create Date: 2025-10-11
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'aca8a2bd4d05'
down_revision: Union[str, Sequence[str], None] = '7dfee23d6ea2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema with idempotent SQL operations."""
    conn = op.get_bind()

    # 1) Ensure seedboxstatus enum exists (safe if already present)
    op.execute("""
    DO $$
    BEGIN
      IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'seedboxstatus') THEN
        CREATE TYPE seedboxstatus AS ENUM ('unknown','inbox','spam','error');
      END IF;
    END
    $$;
    """)

    # 2) Ensure email_logs has smtp_account_id, attempts, error_message columns (use IF NOT EXISTS)
    op.execute("""
    ALTER TABLE email_logs
      ADD COLUMN IF NOT EXISTS smtp_account_id INTEGER,
      ADD COLUMN IF NOT EXISTS attempts INTEGER DEFAULT 1 NOT NULL,
      ADD COLUMN IF NOT EXISTS error_message TEXT;
    """)

    # 2b) Create index on smtp_account_id if not exists
    op.execute("""
    DO $$
    BEGIN
      IF NOT EXISTS (
        SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE c.relname = 'ix_email_logs_smtp_account_id'
      ) THEN
        CREATE INDEX ix_email_logs_smtp_account_id ON email_logs (smtp_account_id);
      END IF;
    END
    $$;
    """)

    # 2c) Create foreign key constraint if not exists (named fk_email_logs_smtp_account_id_smtp_accounts)
    op.execute("""
    DO $$
    BEGIN
      IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints tc
        WHERE tc.constraint_name = 'fk_email_logs_smtp_account_id_smtp_accounts'
          AND tc.table_name = 'email_logs'
      ) THEN
        ALTER TABLE email_logs
          ADD CONSTRAINT fk_email_logs_smtp_account_id_smtp_accounts
          FOREIGN KEY (smtp_account_id) REFERENCES smtp_accounts(id) ON DELETE SET NULL;
      END IF;
    END
    $$;
    """)

    # 3) Add hourly_sent to smtp_accounts safely (if missing)
    op.execute("""
    DO $$
    BEGIN
      IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='smtp_accounts' AND column_name='hourly_sent'
      ) THEN
        ALTER TABLE smtp_accounts ADD COLUMN hourly_sent INTEGER DEFAULT 0 NOT NULL;
        -- set existing NULLs to 0 just in case
        UPDATE smtp_accounts SET hourly_sent = 0 WHERE hourly_sent IS NULL;
        -- drop the server default so inserts don't rely on DB default unless desired
        ALTER TABLE smtp_accounts ALTER COLUMN hourly_sent DROP DEFAULT;
      END IF;
    END
    $$;
    """)

    # 4) If batches.seedbox_status is textual and not the enum, attempt to convert safely.
    #    We only run conversion if column is not already of enum type.
    op.execute("""
    DO $$
    DECLARE
      coltype TEXT;
    BEGIN
      SELECT pg_catalog.format_type(a.atttypid, a.atttypmod) INTO coltype
      FROM pg_attribute a
      JOIN pg_class c ON a.attrelid = c.oid
      WHERE c.relname = 'batches' AND a.attname = 'seedbox_status' AND a.attnum > 0;
      IF coltype IS NOT NULL AND coltype NOT LIKE 'seedboxstatus%' THEN
        -- safe casting with mapping unknown values to 'unknown'
        ALTER TABLE batches
          ALTER COLUMN seedbox_status
          TYPE seedboxstatus
          USING (
            CASE
              WHEN seedbox_status IN ('unknown','inbox','spam','error') THEN seedbox_status::seedboxstatus
              ELSE 'unknown'::seedboxstatus
            END
          );
      END IF;
    EXCEPTION WHEN others THEN
      -- if any problem, skip conversion (leave existing value)
      RAISE NOTICE 'Skipping seedbox_status conversion: %', SQLERRM;
    END
    $$;
    """)


def downgrade() -> None:
    """Downgrade: remove the columns we added if they exist."""
    # Remove hourly_sent if exists
    op.execute("""
    DO $$
    BEGIN
      IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='smtp_accounts' AND column_name='hourly_sent'
      ) THEN
        ALTER TABLE smtp_accounts DROP COLUMN hourly_sent;
      END IF;
    END
    $$;
    """)

    # Remove added email_logs columns if present
    op.execute("""
    DO $$
    BEGIN
      IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='email_logs' AND column_name='error_message') THEN
        ALTER TABLE email_logs DROP COLUMN error_message;
      END IF;
      IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='email_logs' AND column_name='attempts') THEN
        ALTER TABLE email_logs DROP COLUMN attempts;
      END IF;
      IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='email_logs' AND column_name='smtp_account_id') THEN
        -- drop constraint if exists
        IF EXISTS (
          SELECT 1 FROM information_schema.table_constraints tc
          WHERE tc.constraint_name = 'fk_email_logs_smtp_account_id_smtp_accounts'
            AND tc.table_name = 'email_logs'
        ) THEN
          ALTER TABLE email_logs DROP CONSTRAINT fk_email_logs_smtp_account_id_smtp_accounts;
        END IF;
        ALTER TABLE email_logs DROP COLUMN smtp_account_id;
      END IF;
    END
    $$;
    """)

