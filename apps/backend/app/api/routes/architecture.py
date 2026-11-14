from fastapi import APIRouter, Depends, HTTPException, Query

from app.architecture.architecture_reasoning_service import (
    ArchitectureReasoningService,
)
from app.architecture.repository_graph_registry import (
    RepositoryGraphRegistry,
)

from app.core.dependencies import (
    get_architecture_reasoning_service,
    get_repository_graph_registry,
)

router = APIRouter(
    prefix="/architecture",
    tags=["architecture"],
)


@router.post("/analyze")
async def analyze_architecture(
    query: str,
    repository_id: str | None = Query(default=None),
    service: ArchitectureReasoningService = Depends(
        get_architecture_reasoning_service,
    ),
):
    try:
        return await service.analyze(
            query=query,
            repository_id=repository_id,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Architecture analysis is temporarily unavailable.",
        ) from exc


@router.get("/debug-flow")
async def debug_flow(
    symbol: str,
    repository_id: str,
    registry: RepositoryGraphRegistry = Depends(
        get_repository_graph_registry,
    ),
):
    graph = registry.get(repository_id)

    if graph is None:
        raise HTTPException(
            status_code=404,
            detail="Repository graph not found.",
        )

    return graph.trace_execution_path(symbol)


@router.get("/graph-stats")
async def graph_stats(
    repository_id: str,
    registry: RepositoryGraphRegistry = Depends(
        get_repository_graph_registry,
    ),
):
    graph = registry.get(repository_id)

    if graph is None:
        raise HTTPException(
            status_code=404,
            detail="Repository graph not found.",
        )

    return {
        "repository_id": repository_id,
        "symbols": len(graph.symbol_to_file),
        "callers": len(graph.call_graph),
        "files": len(graph.file_to_imports),
    }
