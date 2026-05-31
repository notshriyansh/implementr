from fastapi import APIRouter, Depends

from app.core.dependencies import get_paper_service
from app.schemas.paper import PaperSearchResponse
from app.services.paper_service import PaperService

router = APIRouter(
    prefix="/papers",
    tags=["papers"],
)


@router.get(
    "/search",
    response_model=PaperSearchResponse,
)
async def search_papers(
    query: str,
    paper_service: PaperService = Depends(
        get_paper_service,
    ),
) -> PaperSearchResponse:
    papers = await paper_service.search_papers(
        query=query,
    )

    return PaperSearchResponse(
        papers=papers,
    )