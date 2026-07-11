from fastapi import APIRouter
from fastapi import Depends

from app.architecture.architecture_reasoning_service import (
    ArchitectureReasoningService,
)

from app.architecture.repository_graph import (
    RepositoryGraph,
)

from app.core.dependencies import (
    get_architecture_reasoning_service,
    get_repository_graph,
)

router = APIRouter(
    prefix="/architecture",
    tags=["architecture"],
)


@router.post("/analyze")
async def analyze_architecture(
    query: str,
    service: ArchitectureReasoningService = Depends(
        get_architecture_reasoning_service,
    ),
):
    return await service.analyze(
        query=query
    )


@router.get("/debug-flow")
async def debug_flow(
    symbol: str,
    graph: RepositoryGraph = Depends(
        get_repository_graph,
    ),
):
    return graph.trace_execution_path(
        symbol
    )

@router.get("/graph-stats")
async def graph_stats(
    graph: RepositoryGraph = Depends(
        get_repository_graph,
    ),
):
    return {
        "symbols": len(
            graph.symbol_to_file
        ),
        "callers": len(
            graph.call_graph
        ),
        "files": len(
            graph.file_to_imports
        ),
    }