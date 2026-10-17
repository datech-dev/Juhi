from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.errors import JuhiAPIException


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    yield
    # Shutdown actions


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-grade backend for Juhi AI Companion",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(o) for o in settings.ALLOWED_ORIGINS] if isinstance(settings.ALLOWED_ORIGINS, list) else [str(settings.ALLOWED_ORIGINS)],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(JuhiAPIException)
async def juhi_api_exception_handler(request: Request, exc: JuhiAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details or {},
            }
        },
    )


# Mount API V1
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    return {
        "product": "Juhi AI Companion",
        "status": "operational",
        "api_docs": "/docs" if settings.DEBUG else "hidden_in_production",
    }
