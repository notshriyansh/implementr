from fastapi import APIRouter, Depends

from app.agents.autonomous_agent import (
    AutonomousResearchAgent,
)
from app.core.dependencies import (
    get_autonomous_agent,
)

router = APIRouter(
    prefix="/autonomous",
    tags=["autonomous"],
)


@router.post("/research")
async def autonomous_research(
    question: str,
    agent: AutonomousResearchAgent = Depends(
        get_autonomous_agent,
    ),
) -> dict:
    result = await agent.run(
        question=question,
    )

    return {
        "result": result,
    }