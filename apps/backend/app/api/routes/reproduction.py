from fastapi import APIRouter, Depends, Query

from app.reproduction.research_reproduction_service import (
    ResearchReproductionService,
)
from app.core.dependencies import (
    get_research_reproduction_service,
)

router = APIRouter(
    prefix="/reproduction",
    tags=["reproduction"],
)


@router.post("/plan")
async def generate_plan(
    question: str,
    repository_id: str | None = Query(default=None),
    paper_id: str | None = Query(default=None),
    service: ResearchReproductionService = Depends(
        get_research_reproduction_service,
    ),
):
    return await service.generate(
        question,
        repository_id=repository_id,
        paper_id=paper_id,
    )
