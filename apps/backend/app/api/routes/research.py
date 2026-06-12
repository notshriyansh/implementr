from fastapi import APIRouter, Depends

from app.agents.research_graph import (
    ResearchGraph,
)
from app.core.dependencies import (
    get_research_graph,
)

router = APIRouter(
    prefix="/research",
    tags=["research"],
)


@router.post("/analyze")
async def analyze_research(
    question: str,
    graph: ResearchGraph = Depends(
        get_research_graph,
    ),
) -> dict:
    result = await graph.run(
        question=question,
    )

    return {
        "analysis": result,
    }