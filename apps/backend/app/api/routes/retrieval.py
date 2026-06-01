from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_retrieval_service,
)
from app.retrieval.retrieval_service import (
    RetrievalService,
)

router = APIRouter(
    prefix="/retrieval",
    tags=["retrieval"],
)


@router.get("/search")
async def search_chunks(
    query: str,
    retrieval_service: RetrievalService = Depends(
        get_retrieval_service,
    ),
) -> dict:
    results = await retrieval_service.retrieve(
        query=query,
        k=5,
    )

    return {
        "query": query,
        "results": results,
    }