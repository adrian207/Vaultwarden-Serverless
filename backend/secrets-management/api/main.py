"""
DevOps Secrets Management API

Author: Adrian Johnson <adrian207@gmail.com>
Date: 2025-11-05
Version: 1.0

FastAPI application for secrets management
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import structlog
import time
from typing import Callable

from api.routes import secrets, service_accounts, rotation, audit
from api.middleware.auth import AuthMiddleware
from api.middleware.rate_limit import RateLimitMiddleware
from api.middleware.logging import LoggingMiddleware
from config.settings import get_settings

# Initialize structured logger
logger = structlog.get_logger()

# Get application settings
settings = get_settings()

# ============================================================================
# APPLICATION INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Vaultwarden Secrets Management API",
    description="API-first secrets management for DevOps workflows",
    version="1.0.0",
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_DOCS else None,
    openapi_url="/openapi.json" if settings.ENABLE_DOCS else None,
)

# ============================================================================
# MIDDLEWARE
# ============================================================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthMiddleware)

# ============================================================================
# REQUEST TIMING MIDDLEWARE
# ============================================================================

@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable):
    """Add X-Process-Time header with request duration"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(
        "unhandled_exception",
        exc=str(exc),
        path=request.url.path,
        method=request.method,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "request_id": request.state.request_id if hasattr(request.state, "request_id") else None,
        },
    )

# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "service": "secrets-management-api",
        "version": "1.0.0",
    }

@app.get("/ready", tags=["Health"])
async def readiness_check():
    """
    Readiness check endpoint
    
    Returns:
        dict: Readiness status with dependencies
    """
    # TODO: Check database connectivity
    # TODO: Check Redis connectivity (if used)
    return {
        "status": "ready",
        "database": "connected",
        "cache": "connected",
    }

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    
    Returns:
        dict: API information
    """
    return {
        "name": "Vaultwarden Secrets Management API",
        "version": "1.0.0",
        "description": "API-first secrets management for DevOps workflows",
        "documentation": "/docs" if settings.ENABLE_DOCS else None,
        "health": "/health",
        "metrics": "/metrics",
    }

# ============================================================================
# API ROUTES
# ============================================================================

# Service Accounts
app.include_router(
    service_accounts.router,
    prefix="/api/v1/service-accounts",
    tags=["Service Accounts"],
)

# Secrets
app.include_router(
    secrets.router,
    prefix="/api/v1/secrets",
    tags=["Secrets"],
)

# Rotation
app.include_router(
    rotation.router,
    prefix="/api/v1/rotation-policies",
    tags=["Rotation"],
)

# Audit
app.include_router(
    audit.router,
    prefix="/api/v1/audit",
    tags=["Audit"],
)

# ============================================================================
# METRICS (Prometheus)
# ============================================================================

# Mount Prometheus metrics at /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(
        "application_startup",
        service="secrets-management-api",
        version="1.0.0",
        environment=settings.ENVIRONMENT,
    )
    
    # TODO: Initialize database connection pool
    # TODO: Initialize Redis connection (if used)
    # TODO: Load rotation policies into scheduler

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info(
        "application_shutdown",
        service="secrets-management-api",
    )
    
    # TODO: Close database connections
    # TODO: Close Redis connections
    # TODO: Stop rotation scheduler

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
    )

