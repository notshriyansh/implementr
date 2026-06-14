from fastapi import APIRouter, Depends

from app.code_ingestion.ingestion_service import (
    CodeIngestionService,
)
from app.core.dependencies import (
    get_code_ingestion_service,
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
    chunks = (
        ingestion_service.ingest_repository(
            repo_path
        )
    )

    return {
        "total_chunks": len(chunks),
        "sample_chunk": (
            chunks[0]
            if chunks
            else None
        ),
    }