# =========================
# Backend Dockerfile
# =========================
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# 🧠 Install only what we actually need — PostgreSQL client for pg_isready
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app with hot reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
