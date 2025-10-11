# backend/app/utils/validators.py
import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


# A conservative RFC-like regex (not perfect but good enough for most)
EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

def is_valid_email(email: str) -> bool:
    if not email or "@" not in email:
        return False
    email = email.strip()
    # First try simple regex (fast)
    if not EMAIL_RE.match(email):
        return False
    # Try to use email_validator package for more thorough checks if available
    try:
        from email_validator import validate_email, EmailNotValidError
        try:
            v = validate_email(email, check_deliverability=False)
            # v['email'] is normalized form
            return True
        except EmailNotValidError as e:
            logger.debug("email_validator rejected %s: %s", email, e)
            return False
    except Exception:
        # email_validator not installed — rely on regex result
        return True


def check_mx_record(email: str) -> Optional[bool]:
    """
    Return True if MX records exist, False if none found, None if DNS lookup not possible.
    Requires dnspython (import dns.resolver) if available.
    """
    try:
        domain = email.split("@", 1)[1]
    except Exception:
        return False

    try:
        import dns.resolver  # from dnspython
    except Exception:
        logger.debug("dnspython not installed, skipping MX check")
        return None

    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=5.0)
        return len(answers) > 0
    except Exception as e:
        logger.debug("MX lookup failed for %s: %s", domain, e)
        return False
