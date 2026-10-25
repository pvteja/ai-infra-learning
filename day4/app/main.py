import os
import socket
from pathlib import Path
from fastapi import FastAPI

APP_NAME = os.getenv("APP_NAME", "AI Infra Lab")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))
VISITS_FILE = DATA_DIR / "visits.txt"

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": f"Hello from {APP_NAME}",
        "environment": ENVIRONMENT,
        "host": socket.gethostname(),
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/visits")
def visits():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    count = int(VISITS_FILE.read_text()) if VISITS_FILE.exists() else 0
    count += 1
    VISITS_FILE.write_text(str(count))
    return {"visits": count}