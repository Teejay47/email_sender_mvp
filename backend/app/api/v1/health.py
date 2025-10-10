from fastapi import APIRouter, Depends
from ...core.database import get_db
from ...core.redis_client import redis_client

router = APIRouter()


@router.get("/health")
def health(db=Depends(get_db)):
    # Perform minimal checks
    try:
        redis_client.ping()
        redis_ok = True
    except Exception:
        redis_ok = False

    return {"status": "ok", "redis": redis_ok}
