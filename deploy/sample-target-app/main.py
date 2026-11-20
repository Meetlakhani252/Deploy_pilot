from fastapi import FastAPI
import os

app = FastAPI(title="Sample Target App", version="1.0.0")

VERSION = os.getenv("APP_VERSION", "1.0.0")
HEALTH_STATUS = os.getenv("APP_HEALTH_STATUS", "healthy")


@app.get("/")
def read_root():
    return {
        "app": "sample-target-app",
        "version": VERSION,
        "status": HEALTH_STATUS,
    }


@app.get("/health")
def health():
    if HEALTH_STATUS != "healthy":
        return {"status": "unhealthy"}, 500
    return {"status": "healthy", "version": VERSION}
