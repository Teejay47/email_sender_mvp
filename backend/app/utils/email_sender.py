import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def send_email(
    smtp_config: dict,
    to_address: str,
    subject: str,
    body: str,
    from_name: str = None,
    from_email: str = None,
    reply_to: str = None,
):
    """
    Generic SMTP sender supporting both SSL (465) and STARTTLS (587).
    """

    host = smtp_config.get("host") or settings.SMTP_HOST
    port = smtp_config.get("port") or settings.SMTP_PORT
    username = smtp_config.get("username") or settings.SMTP_USERNAME
    password = smtp_config.get("password") or settings.SMTP_PASSWORD
    use_tls = smtp_config.get("use_tls", port == 587)

    from_name = from_name or settings.FROM_NAME
    from_email = from_email or settings.FROM_EMAIL

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = formataddr((from_name, from_email))
    msg["To"] = to_address
    if reply_to:
        msg["Reply-To"] = reply_to

    logger.info(f"Connecting to SMTP server {host}:{port} (TLS={use_tls}) as {username}")

    try:
        # 🔹 Automatically choose the right protocol
        if port == 465:
            logger.info("Using SSL connection...")
            server = smtplib.SMTP_SSL(host, port, timeout=20)
        else:
            server = smtplib.SMTP(host, port, timeout=20)
            server.ehlo()
            if use_tls:
                logger.info("Starting TLS session...")
                server.starttls()
                server.ehlo()

        if username and password:
            logger.info(f"Logging in as {username}")
            server.login(username, password)

        logger.info(f"Sending email to {to_address}")
        server.sendmail(from_email, [to_address], msg.as_string())
        server.quit()
        logger.info("✅ Email sent successfully")

    except Exception as e:
        logger.exception("❌ SMTP send_email() failed")
        raise
