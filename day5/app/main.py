import os
import socket
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

APP_NAME = os.getenv("APP_NAME", "AI Infra Lab")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app@localhost:5432/appdb")


def get_conn():
    return psycopg.connect(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once at startup: create the table if it doesn't exist
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT now()
            )
        """)
    yield


app = FastAPI(lifespan=lifespan)


class Note(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": f"Hello from {APP_NAME}", "host": socket.gethostname()}


@app.get("/health")
def health():
    with get_conn() as conn:
        conn.execute("SELECT 1")
    return {"status": "ok", "db": "ok"}


@app.post("/notes")
def add_note(note: Note):
    with get_conn() as conn:
        row = conn.execute(
            "INSERT INTO notes (text) VALUES (%s) RETURNING id", (note.text,)
        ).fetchone()
    return {"id": row[0], "text": note.text}


@app.get("/notes")
def list_notes():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, text, created_at FROM notes ORDER BY id"
        ).fetchall()
    return [{"id": r[0], "text": r[1], "created_at": r[2]} for r in rows]