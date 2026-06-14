from fastapi import (
    APIRouter,
    Depends,
)

from app.code_retrieval.symbol_retrieval_service import (
    SymbolRetrievalService,
)

from app.core.dependencies import (
    get_symbol_retrieval_service,
)

router = APIRouter(
    prefix="/symbols",
    tags=["symbols"],
)


@router.get("/search")
async def search_symbols(
    query: str,
    retrieval_service: (
        SymbolRetrievalService
    ) = Depends(
        get_symbol_retrieval_service
    ),
):
    results = await (
        retrieval_service.retrieve(
            query=query,
            k=5,
        )
    )

    return {
        "results": results
    }