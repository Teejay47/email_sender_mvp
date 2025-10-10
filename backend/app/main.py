from fastapi import FastAPI
from app.api.v1 import health

app = FastAPI(title="Email Sender MVP - API")

app.include_router(health.router, prefix="/api/v1")

@app.get("/health")
def root_health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Email Sender API!"}
