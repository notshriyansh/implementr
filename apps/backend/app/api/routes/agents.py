from fastapi import APIRouter, Depends

from app.agents.implementation_agent import (
    ImplementationAgent,
)
from app.core.dependencies import (
    get_implementation_agent,
)

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)


@router.post("/implementation-plan")
async def implementation_plan(
    question: str,
    agent: ImplementationAgent = Depends(
        get_implementation_agent,
    ),
) -> dict:
    plan = await agent.generate_plan(
        question=question,
    )

    return {
        "plan": plan,
    }