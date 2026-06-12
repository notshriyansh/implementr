from fastapi import FastAPI

from app.api.routes.papers import router as papers_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.api.routes.ingestion import (
    router as ingestion_router,
)
from app.api.routes.retrieval import (
    router as retrieval_router,
)
from app.api.routes.chat import (
    router as chat_router,
)
from app.api.routes.agents import (
    router as agents_router,
)
from app.api.routes.research import (
    router as research_router,
)
from app.api.routes.autonomous import (
    router as autonomous_router,
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

app.include_router(
    retrieval_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    chat_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    agents_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    research_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    autonomous_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

