"""Main FastAPI Application Entrypoint according to DeployPilot TSD."""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1 import api_v1_router
from app.api.v1.auth import router as auth_router
from app.core.config import settings
from app.core.exceptions import AppException

app = FastAPI(
    title="DeployPilot API",
    version="0.1.0",
    description="AI-Powered DevOps Automation Platform API",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler for custom AppException (code, message, details)
@app.exception_handler(AppException)
async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
        },
        headers=getattr(exc, "headers", None),
    )


# Exception handler for general Starlette / FastAPI HTTPException
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    code = "ERROR"
    if exc.status_code == 401:
        code = "UNAUTHORIZED"
    elif exc.status_code == 403:
        code = "FORBIDDEN"
    elif exc.status_code == 404:
        code = "NOT_FOUND"
    elif exc.status_code == 423:
        code = "LOCKED"

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": code,
            "message": str(exc.detail),
            "details": None,
        },
        headers=getattr(exc, "headers", None),
    )


# Exception handler for Pydantic RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"] if loc not in ("body",))
        errors.append({
            "field": field,
            "message": err["msg"],
            "type": err["type"],
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": "VALIDATION_ERROR",
            "message": "Invalid request parameters",
            "details": errors,
        },
    )


# Mount routers:
# Under /api/v1 (e.g. /api/v1/auth/signup) and direct /auth for convenience
app.include_router(api_v1_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix="/auth")


@app.get("/healthz")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
