from fastapi import APIRouter
from fastapi import Depends

from app.architecture.architecture_reasoning_service import (
    ArchitectureReasoningService,
)

from app.core.dependencies import (
    get_architecture_reasoning_service,
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