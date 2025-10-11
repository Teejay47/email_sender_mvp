from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import health
from app.api import smtp, recipients  # ✅ add recipients
from app.api import seedbox

app = FastAPI(title="Email Sender MVP - API")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(smtp.router, prefix="/api/v1")
app.include_router(recipients.router, prefix="/api/v1")  # ✅ add this line
app.include_router(seedbox.router, prefix="/api/v1")


@app.get("/health")
def root_health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Email Sender API!"}
