from fastapi import APIRouter, Depends, Query

from app.core.dependencies import (
    get_implementation_blueprint_service,
)

router = APIRouter(
    prefix="/blueprints",
    tags=["blueprints"],
)


@router.get("/generate")
async def generate_blueprint(
    question: str,
    repository_id: str | None = Query(default=None),
    service=Depends(get_implementation_blueprint_service),
):
    return await service.generate(
        question,
        repository_id=repository_id,
    )
