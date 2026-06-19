from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)

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
from app.api.routes.evaluation import (
    router as evaluation_router,
)
from app.api.routes.repository import (
    router as repository_router,
)
from app.api.routes.hybrid import (
    router as hybrid_router,
)
from app.api.routes.symbols import (
    router as symbols_router,
)
from app.api.routes.architecture import (
    router as architecture_router,
)

setup_logging()

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

app.include_router(
    evaluation_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    repository_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    hybrid_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    symbols_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    architecture_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

