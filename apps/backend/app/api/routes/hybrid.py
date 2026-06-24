from fastapi import (
    APIRouter,
    Depends,
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
    agent: (
        HybridImplementationAgent
    ) = Depends(
        get_hybrid_agent,
    ),
) -> HybridAnalysisResponse:
    return await agent.analyze(
        question
    )