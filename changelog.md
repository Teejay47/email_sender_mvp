# Changelog

## v0.2 – Base System Setup
- Added FastAPI backend, React frontend, Redis, Postgres, Celery, Flower.
- Created /health endpoint and confirmed frontend connection.
- Docker Compose orchestration working.

## v0.3 – Database Models Added
- Implemented SQLAlchemy models for User, SMTPAccount, Recipient, SeedBox, Campaign, Batch, EmailLog.
- Added Alembic migrations and confirmed successful DB creation.
- Created Pydantic schemas and DB health test endpoints.


## v0.4 – SMTP Manager Implemented
- Added SMTP CRUD endpoints and encryption layer.
- Introduced /smtp/test route for live credential validation.
- Built SMTP Manager frontend page with test button.


## v0.5 – Recipient Management Added
- Implemented CSV upload and email validation system.
- Added backend API endpoints for import/list/suppress.
- Created Recipient Manager frontend page with validation display.


## v0.6 – SeedBox Integration & Inbox Testing
- Added seed box management and inbox placement testing.
- Integrated Celery async tasks for seed tests.
- Frontend page for seed management and test results.
