from fastapi import APIRouter, Depends

from app.code_ingestion.ingestion_service import (
    CodeIngestionService,
)
from app.core.dependencies import (
    get_code_ingestion_service,
)
from app.code_retrieval.code_retrieval_service import (
    CodeRetrievalService,
)
from app.core.dependencies import (
    get_code_retrieval_service,
)

router = APIRouter(
    prefix="/repository",
    tags=["repository"],
)


@router.post("/ingest")
async def ingest_repository(
    repo_path: str,
    ingestion_service: (
        CodeIngestionService
    ) = Depends(
        get_code_ingestion_service,
    ),
) -> dict:
    chunks = await ingestion_service.ingest_repository(
        repo_path
    )
    

    return {
        "total_chunks": len(chunks),
        "sample_chunk": (
            chunks[0]
            if chunks
            else None
        ),
    }

@router.get("/search")
async def search_repository(
    query: str,
    retrieval_service: (
        CodeRetrievalService
    ) = Depends(
        get_code_retrieval_service,
    ),
) -> dict:
    chunks = (
        await retrieval_service.retrieve(
            query=query,
            k=5,
        )
    )

    return {
        "results": chunks,
    }