# check_smtp.py
import sys
from pathlib import Path
import smtplib
import ssl
import socket
import traceback

sys.path.append(str(Path(__file__).resolve().parent))  # add app/ to path

from core.database import get_db
from models.smtp_account import SMTPAccount
from core.security import fernet

db = next(get_db())

active_smtps = db.query(SMTPAccount).filter(SMTPAccount.is_active == True).all()

for smtp in active_smtps:
    server = None
    password = None
    try:
        # Try to decrypt password first
        if smtp.encrypted_password:
            try:
                password = fernet.decrypt(smtp.encrypted_password.encode()).decode()
            except Exception:
                print(f"[WARN] SMTP {smtp.id}: {smtp.username}@{smtp.host} -> InvalidToken, trying as plain text")
                password = smtp.encrypted_password
        else:
            password = None

        # Auto-detect SSL vs non-SSL
        if smtp.port == 465:
            # Implicit SSL
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(smtp.host, smtp.port, timeout=10, context=context)
        else:
            # Start unencrypted, upgrade to TLS if port 587
            server = smtplib.SMTP(smtp.host, smtp.port, timeout=10)
            if smtp.port == 587:
                server.starttls()

        # Login if credentials are provided
        if smtp.username and password:
            server.login(smtp.username, password)

        print(f"[OK] SMTP {smtp.id}: {smtp.username}@{smtp.host}")

    except smtplib.SMTPAuthenticationError as e:
        print(f"[FAIL] SMTP {smtp.id}: {smtp.username}@{smtp.host} -> Authentication failed: {repr(e)}")
    except smtplib.SMTPConnectError as e:
        print(f"[FAIL] SMTP {smtp.id}: {smtp.username}@{smtp.host} -> Connection failed: {repr(e)}")
    except smtplib.SMTPHeloError as e:
        print(f"[FAIL] SMTP {smtp.id}: {smtp.username}@{smtp.host} -> HELO error: {repr(e)}")
    except smtplib.SMTPServerDisconnected as e:
        print(f"[FAIL] SMTP {smtp.id}: {smtp.username}@{smtp.host} -> Server disconnected: {repr(e)}")
    except smtplib.SMTPException as e:
        print(f"[FAIL] SMTP {smtp.id}: {smtp.username}@{smtp.host} -> SMTP error: {repr(e)}")
    except socket.timeout:
        print(f"[FAIL] SMTP {smtp.id}: {smtp.username}@{smtp.host} -> Connection timed out")
    except socket.gaierror:
        print(f"[FAIL] SMTP {smtp.id}: {smtp.username}@{smtp.host} -> Hostname could not be resolved")
    except Exception as e:
        print(f"[FAIL] SMTP {smtp.id}: {smtp.username}@{smtp.host} -> Unexpected error: {repr(e)}")
        traceback.print_exc()
    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass
