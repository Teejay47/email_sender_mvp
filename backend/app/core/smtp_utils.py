# backend/app/core/smtp_utils.py
from datetime import datetime, timedelta

def remaining_daily_quota(smtp) -> int:
    return max(0, smtp.daily_limit - (smtp.used_today or 0))

def should_pause_for_quota(smtp) -> bool:
    return remaining_daily_quota(smtp) <= 0

def reset_counters_if_needed(smtp):
    # placeholder: invoked by celery beat job at midnight
    if smtp.last_reset is None or smtp.last_reset.date() < datetime.utcnow().date():
        smtp.used_today = 0
        smtp.last_reset = datetime.utcnow()
