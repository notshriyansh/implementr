from fastapi import (
    APIRouter,
    Depends,
)

from app.concepts.concept_service import (
    ConceptService,
)

from app.concepts.concept_index import ConceptIndex

from app.code_retrieval.symbol_retrieval_service import (
    SymbolRetrievalService,
)

from app.core.dependencies import (
    get_concept_index,
    get_concept_service,
    get_symbol_retrieval_service,
)

router = APIRouter(
    prefix="/concepts",
    tags=["concepts"],
)


@router.get("/debug")
async def debug_concepts(
    query: str,
    concept_service: (
        ConceptService
    ) = Depends(
        get_concept_service
    ),
    symbol_service: (
        SymbolRetrievalService
    ) = Depends(
        get_symbol_retrieval_service
    ),
):

    symbols = await (
        symbol_service.retrieve(
            query=query,
            k=20,
        )
    )

    return (
        concept_service
        .build_concept_map(
            paper_text=query,
            symbols=symbols,
        )
    )

@router.get("/index")
async def concept_index_debug(
    concept_index: ConceptIndex = Depends(get_concept_index),
):

    concepts = (
        concept_index.all()
    )

    return {
        "total_concepts": len(
            concepts
        ),
        "concepts": concepts,
    }
