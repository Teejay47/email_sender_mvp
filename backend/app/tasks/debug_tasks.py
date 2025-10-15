from app.celery_worker import celery

@celery.task(name="debug.ping")
def ping():
    return "pong"
