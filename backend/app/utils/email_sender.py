# backend/app/utils/email_sender.py
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from app.core.config import settings

logger = logging.getLogger(__name__)


class SMTPClient:
    """
    Persistent SMTP connection manager.
    Allows reusing the same connection across multiple sends
    to drastically reduce connection overhead.
    """

    def __init__(self, smtp_config: dict):
        self.smtp_config = smtp_config
        self.server = None
        self.connected = False

    def connect(self):
        """Establish connection and authenticate."""
        if self.connected:
            return

        host = self.smtp_config.get("host") or settings.SMTP_HOST
        port = self.smtp_config.get("port") or settings.SMTP_PORT
        username = self.smtp_config.get("username") or settings.SMTP_USERNAME
        password = self.smtp_config.get("password") or settings.SMTP_PASSWORD
        use_tls = self.smtp_config.get("use_tls", port == 587)

        try:
            logger.info(f"Connecting to SMTP server {host}:{port} (TLS={use_tls}) as {username}")

            if port == 465:
                self.server = smtplib.SMTP_SSL(host, port, timeout=30)
            else:
                self.server = smtplib.SMTP(host, port, timeout=30)
                self.server.ehlo()
                if use_tls:
                    self.server.starttls()
                    self.server.ehlo()

            if username and password:
                self.server.login(username, password)

            self.connected = True
            logger.info("✅ SMTP connection established successfully")
        except Exception as e:
            self.connected = False
            logger.exception(f"❌ Failed to connect/login to SMTP {host}:{port}: {e}")
            raise

    def send_message(self, msg, from_email, to_address):
        """Send an already-built MIME message."""
        if not self.connected or not self.server:
            self.connect()
        try:
            self.server.sendmail(from_email, [to_address], msg.as_string())
        except Exception as e:
            logger.exception(f"❌ Failed to send email to {to_address}: {e}")
            raise

    def quit(self):
        """Close connection cleanly."""
        if self.server:
            try:
                self.server.quit()
            except Exception:
                logger.warning("SMTP quit() failed (already closed?)")
        self.connected = False
        self.server = None


def send_email(
    smtp_config: dict,
    to_address: str = None,
    subject: str = None,
    html_body: str = None,
    text_body: str = None,
    from_name: str = None,
    from_email: str = None,
    reply_to: str = None,
    test_mode: bool = False,
    smtp_client: SMTPClient = None,  # <-- allows reuse of persistent connection
):
    """
    Generic SMTP sender supporting SSL (465) and STARTTLS (587).
    If `test_mode=True`, only tests connection and login.
    If `smtp_client` is provided, reuses the persistent connection.
    """
    host = smtp_config.get("host") or settings.SMTP_HOST
    port = smtp_config.get("port") or settings.SMTP_PORT
    username = smtp_config.get("username") or settings.SMTP_USERNAME
    password = smtp_config.get("password") or settings.SMTP_PASSWORD
    use_tls = smtp_config.get("use_tls", port == 587)

    if test_mode:
        logger.info(f"Testing SMTP connection to {host}:{port} as {username}...")
        try:
            client = SMTPClient(smtp_config)
            client.connect()
            client.quit()
            logger.info("✅ SMTP credentials valid")
            return {"status": "ok"}
        except Exception:
            logger.exception("❌ SMTP test failed")
            raise

    # --- Build MIME message ---
    from_name = from_name or settings.FROM_NAME
    from_email = from_email or settings.FROM_EMAIL

    if html_body and not text_body:
        text_body = "This message contains HTML content. View in an HTML-capable client."

    if html_body:
        msg = MIMEMultipart("alternative")
        if text_body:
            msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))
    else:
        msg = MIMEText(text_body or "", "plain")

    if not to_address or not subject:
        raise ValueError("to_address and subject are required when not in test_mode")

    msg["Subject"] = subject
    msg["From"] = formataddr((from_name, from_email))
    msg["To"] = to_address
    if reply_to:
        msg["Reply-To"] = reply_to

    # --- Send Email ---
    try:
        # Reuse persistent client if available
        if smtp_client:
            smtp_client.send_message(msg, from_email, to_address)
        else:
            client = SMTPClient(smtp_config)
            client.connect()
            client.send_message(msg, from_email, to_address)
            client.quit()

        logger.info(f"✅ Email sent successfully to {to_address}")
        return {"status": "sent"}
    except Exception as e:
        logger.exception(f"❌ SMTP send_email() failed for {to_address}: {e}")
        return {"status": "failed", "error": str(e)}
