from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from app.agents.hybrid_implementation_agent import (
    HybridImplementationAgent,
)

from app.core.dependencies import (
    get_hybrid_agent,
)

from app.schemas.hybrid import (
    HybridAnalysisResponse,
)

router = APIRouter(
    prefix="/hybrid",
    tags=["hybrid"],
)


@router.post(
    "/analyze",
    response_model=HybridAnalysisResponse,
)
async def hybrid_analysis(
    question: str,
    repository_id: str | None = Query(default=None),
    paper_id: str | None = Query(default=None),
    agent: (
        HybridImplementationAgent
    ) = Depends(
        get_hybrid_agent,
    ),
) -> HybridAnalysisResponse:
    return await agent.analyze(
        question,
        repository_id=repository_id,
        paper_id=paper_id,
    )