from fastapi import APIRouter
from fastapi import Depends

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
    service: ResearchReproductionService = Depends(
        get_research_reproduction_service,
    ),
):
    return await service.generate(
        question
    )