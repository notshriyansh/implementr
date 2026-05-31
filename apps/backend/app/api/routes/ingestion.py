from fastapi import APIRouter, Depends

from app.core.dependencies import get_ingestion_service
from app.services.ingestion_service import IngestionService

router = APIRouter(
    prefix="/ingestion",
    tags=["ingestion"],
)


@router.post("/download")
async def download_paper(
    pdf_url: str,
    paper_id: str,
    ingestion_service: IngestionService = Depends(
        get_ingestion_service,
    ),
) -> dict[str, str]:
    saved_path = await ingestion_service.ingest_paper(
        pdf_url=pdf_url,
        user_id="local_user",
        paper_id=paper_id,
    )

    return {
        "saved_path": saved_path,
    }