import json
import os
import socket
import time
from contextlib import asynccontextmanager

import psycopg
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

APP_NAME = os.getenv("APP_NAME", "AI Infra Lab")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app@localhost:5432/appdb")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL = int(os.getenv("CACHE_TTL", "30"))
CACHE_KEY = "notes:all"

cache = redis.Redis.from_url(
    REDIS_URL, decode_responses=True, socket_timeout=1, socket_connect_timeout=1
)


def get_conn():
    return psycopg.connect(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    try:
        cache.ping()
        cache_status = "ok"
    except redis.RedisError:
        cache_status = "down"
    return {"status": "ok", "db": "ok", "cache": cache_status}


@app.post("/notes")
def add_note(note: Note):
    with get_conn() as conn:
        row = conn.execute(
            "INSERT INTO notes (text) VALUES (%s) RETURNING id", (note.text,)
        ).fetchone()
    try:
        cache.delete(CACHE_KEY)  # data changed, so the cached list is stale
    except redis.RedisError:
        pass
    return {"id": row[0], "text": note.text}


@app.get("/notes")
def list_notes():
    start = time.perf_counter()

    try:
        cached = cache.get(CACHE_KEY)
    except redis.RedisError:
        cached = None  # cache is down, so fall back to the database

    if cached:
        notes = json.loads(cached)
        source = "cache"
    else:
        with get_conn() as conn:
            conn.execute("SELECT pg_sleep(1)")  # pretend this is a slow query
            rows = conn.execute(
                "SELECT id, text, created_at FROM notes ORDER BY id"
            ).fetchall()
        notes = [
            {"id": r[0], "text": r[1], "created_at": r[2].isoformat()} for r in rows
        ]
        try:
            cache.setex(CACHE_KEY, CACHE_TTL, json.dumps(notes))
        except redis.RedisError:
            pass
        source = "database"

    elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
    return {"source": source, "ms": elapsed_ms, "host": socket.gethostname(), "notes": notes}


@app.get("/visits")
def visits():
    try:
        count = cache.incr("visits")  # atomic, shared by all API copies
    except redis.RedisError:
        raise HTTPException(status_code=503, detail="Visit counter unavailable: cache is down")
    return {"visits": count, "host": socket.gethostname()}