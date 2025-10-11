# backend/app/utils/campaign_helpers.py
from app.tasks.seedbox_tasks import send_seed_test_task
from app.core.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

def run_seed_test_before_batch(campaign_id: int, user_id: int, seedbox_id: int) -> dict:
    """
    Run a seed test synchronously or enqueue it; if test returns spam, it can pause the campaign.
    For MVP: enqueue and then read result (simple blocking might be used).
    """
    # Enqueue for now
    task = send_seed_test_task.delay(seedbox_id, user_id)
    logger.info("Queued seed test task %s for campaign %s", task.id, campaign_id)
    # For MVP return queued status
    return {"status": "queued", "task_id": task.id}
