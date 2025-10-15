#backend/app/utils/imap_checker.py
import imaplib
import email
import time
import logging
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)


def check_inbox_placement(imap_config: dict, subject_keyword: str, wait_seconds: int = 45) -> str:
    """
    Check where an email landed (inbox/spam/unknown) by searching IMAP folders.
    - Waits longer for delayed delivery.
    - Distinguishes between "spam", "not_found", and "error".
    """
    host = imap_config["host"]
    port = imap_config.get("port", 993)
    username = imap_config["username"]
    password = imap_config["password"]
    use_ssl = imap_config.get("use_ssl", True)

    inbox_folder = imap_config.get("inbox_folder", "INBOX")
    spam_folder = imap_config.get("spam_folder", "[Gmail]/Spam")

    logger.info(f"⏳ Waiting {wait_seconds}s before checking IMAP for {username}")
    time.sleep(wait_seconds)

    mail = None
    try:
        mail = imaplib.IMAP4_SSL(host, port) if use_ssl else imaplib.IMAP4(host, port)
        mail.login(username, password)

        # Helper to safely select folder and search
        def search_folder(folder_name: str) -> bool:
            typ, _ = mail.select(folder_name)
            if typ != "OK":
                logger.warning(f"⚠️ Cannot select folder '{folder_name}' for {username}")
                return False
            typ, data = mail.search(None, f'(TEXT "{subject_keyword}")')
            return typ == "OK" and data and data[0]

        # 1️⃣ Check inbox
        logger.info(f"📥 Checking inbox folder '{inbox_folder}' for subject: {subject_keyword}")
        if search_folder(inbox_folder):
            return "inbox"

        # 2️⃣ Check spam
        logger.info(f"🗑️ Checking spam folder '{spam_folder}' for subject: {subject_keyword}")
        if search_folder(spam_folder):
            return "spam"

        # 3️⃣ Not found
        logger.info("⚠️ Message not found in inbox or spam.")
        return "not_found"

    except Exception as e:
        logger.exception(f"❌ IMAP check failed for {username}: {e}")
        return "error"
    finally:
        if mail:
            try:
                mail.logout()
            except Exception:
                pass
