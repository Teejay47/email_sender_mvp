import imaplib
import email
import time
import logging
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)


def check_inbox_placement(imap_config: dict, subject_keyword: str, wait_seconds: int = 30) -> str:
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

    # Allow more delivery time
    logger.info(f"⏳ Waiting {wait_seconds}s before checking IMAP for {username}")
    time.sleep(wait_seconds)

    try:
        mail = imaplib.IMAP4_SSL(host, port) if use_ssl else imaplib.IMAP4(host, port)
        mail.login(username, password)

        # --- 1️⃣ Check Inbox ---
        logger.info(f"📥 Checking inbox folder '{inbox_folder}' for subject: {subject_keyword}")
        mail.select(inbox_folder)
        typ, data = mail.search(None, f'(TEXT "{subject_keyword}")')
        if typ == "OK" and data and data[0]:
            mail.logout()
            return "inbox"

        # --- 2️⃣ Check Spam ---
        logger.info(f"🗑️ Checking spam folder '{spam_folder}' for subject: {subject_keyword}")
        mail.select(spam_folder)
        typ, data = mail.search(None, f'(TEXT "{subject_keyword}")')
        if typ == "OK" and data and data[0]:
            mail.logout()
            return "spam"

        # --- 3️⃣ Not found anywhere ---
        logger.info("⚠️ Message not found in inbox or spam.")
        mail.logout()
        return "not_found"

    except Exception as e:
        logger.exception(f"❌ IMAP check failed for {username}: {e}")
        return "error"
