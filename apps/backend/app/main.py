import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("Starting route imports...", flush=True)

from app.api.routes import agents
print(" agents", flush=True)

from app.api.routes import architecture
print(" architecture", flush=True)

from app.api.routes import autonomous
print(" autonomous", flush=True)

from app.api.routes import blueprints
print("  blueprints", flush=True)

from app.api.routes import chat
print("  chat", flush=True)

from app.api.routes import concepts
print("  concepts", flush=True)

from app.api.routes import evaluation
print("  evaluation", flush=True)

from app.api.routes import hybrid
print("  hybrid", flush=True)

from app.api.routes import ingestion
print("  ingestion", flush=True)

from app.api.routes import papers
print("  papers", flush=True)

from app.api.routes import repository
print("  repository", flush=True)

from app.api.routes import reproduction
print("  reproduction", flush=True)

from app.api.routes import research
print("  research", flush=True)

from app.api.routes import retrieval
print("  retrieval", flush=True)

from app.api.routes import symbols
print("  symbols", flush=True)

from app.api.routes import workspace_outputs
print("  workspace_outputs", flush=True)

from app.api.routes import workspaces
print("  workspaces", flush=True)

from app.core.config import get_settings
print("  config", flush=True)

from app.core.logging import setup_logging
print("  logging", flush=True)

setup_logging()

logger = logging.getLogger(__name__)
logger.info("main.py imported successfully")

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)

agents_router = agents.router
architecture_router = architecture.router
autonomous_router = autonomous.router
blueprints_router = blueprints.router
chat_router = chat.router
concepts_router = concepts.router
evaluation_router = evaluation.router
hybrid_router = hybrid.router
ingestion_router = ingestion.router
papers_router = papers.router
repository_router = repository.router
reproduction_router = reproduction.router
research_router = research.router
retrieval_router = retrieval.router
symbols_router = symbols.router
workspace_outputs_router = workspace_outputs.router
workspaces_router = workspaces.router


@app.on_event("startup")
async def startup_log():
    logger.info("====================================")
    logger.info("FastAPI startup event reached")
    logger.info("Application has finished importing.")
    logger.info("====================================")


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

app.include_router(
    concepts_router,
    prefix="/api/v1",
)

app.include_router(
    reproduction_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    blueprints_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    workspaces_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    workspace_outputs_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}