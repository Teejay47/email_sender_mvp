# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings


# Optimized PostgreSQL connection pool for high-concurrency workloads
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # validate connections before using them
    pool_size=20,            # persistent connections in pool
    max_overflow=40,         # temporary connections allowed during spikes
    pool_timeout=30,         # wait time before raising "no connection" error
    pool_recycle=1800,       # recycle connections every 30 mins (prevent stale)
    pool_use_lifo=True,      # (optional) speeds up under heavy parallelism
    echo_pool=False,         # set True only for debugging pool behavior
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,  # avoids stale object errors in Celery workers
)


# Dependency for FastAPI routes
def get_db():
    """
    Dependency that provides a clean SQLAlchemy session
    for FastAPI route handlers.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
