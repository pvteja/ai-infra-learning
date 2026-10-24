from fastapi import FastAPI
import socket

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from AI Infra Lab2", "host": socket.gethostname()}

@app.get("/health")
def health():
    return {"status": "ok"}