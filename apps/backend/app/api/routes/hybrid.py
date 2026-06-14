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

router = APIRouter(
    prefix="/hybrid",
    tags=["hybrid"],
)


@router.post("/analyze")
async def hybrid_analysis(
    question: str,
    agent: (
        HybridImplementationAgent
    ) = Depends(
        get_hybrid_agent,
    ),
) -> dict:
    result = await agent.analyze(
        question
    )

    return {
        "result": result,
    }