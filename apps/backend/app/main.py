from fastapi import FastAPI

from app.api.routes.papers import router as papers_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.api.routes.ingestion import (
    router as ingestion_router,
)

setup_logging()

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)

app.include_router(
    papers_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    ingestion_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

