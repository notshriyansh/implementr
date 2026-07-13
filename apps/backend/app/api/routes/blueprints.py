from fastapi import APIRouter
from fastapi import Depends

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
    service=Depends(
        get_implementation_blueprint_service
    ),
):
    return await service.generate(
        question
    )