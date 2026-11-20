"""Main FastAPI Application Entrypoint."""
from fastapi import FastAPI

app = FastAPI(
    title="DeployPilot API",
    version="0.1.0",
    description="AI-Powered DevOps Automation Platform API",
)


@app.get("/healthz")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
