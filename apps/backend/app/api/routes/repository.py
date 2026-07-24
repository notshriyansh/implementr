from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from app.code_retrieval.code_retrieval_service import (
    CodeRetrievalService,
)
from app.core.dependencies import (
    get_code_retrieval_service,
)
from app.code_ingestion.repository_analyzer import (
    RepositoryAnalyzer,
)
from app.core.dependencies import (
    get_repository_analyzer,
)
from app.orchestration.service import JobService
from app.core.dependencies import get_job_service

from app.orchestration.enums import JobType
from app.sources.models import LocalRepositoryModel

from app.schemas.repository import (
    RepositoryIngestionResponse,
)

router = APIRouter(
    prefix="/repository",
    tags=["repository"],
)


@router.post(
    "/ingest",
    response_model=RepositoryIngestionResponse,
)
async def ingest_repository(
    repo_path: str,
    job_service: JobService = Depends(
        get_job_service,
    ),
):

    job = job_service.create(
        job_type=JobType.REPOSITORY_INDEX,
        payload={
            "source": LocalRepositoryModel(
                path=repo_path,
            ).model_dump()
        },
    )

    return {
        "job_id": job.id,
        "status": job.status,
    }


@router.get("/search")
async def search_repository(
    query: str,
    retrieval_service: CodeRetrievalService = Depends(
        get_code_retrieval_service,
    ),
) -> dict:
    chunks = await retrieval_service.retrieve(
        query=query,
        k=5,
    )

    return {
        "results": chunks,
    }


@router.get("/structure")
async def analyze_repository(
    repo_path: str,
    analyzer: RepositoryAnalyzer = Depends(
        get_repository_analyzer,
    ),
) -> dict:
    result = analyzer.analyze(
        repo_path
    )

    return result.model_dump()


@router.get("/file")
async def get_file_content(
    repo_path: str,
    file_path: str,
) -> dict:
    try:
        base_dir = Path(repo_path).resolve()
        target_file = (base_dir / file_path).resolve()

        try:
            target_file.relative_to(base_dir)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid file path",
            )

        if not target_file.is_file():
            raise HTTPException(
                status_code=404,
                detail="File not found",
            )

        content = target_file.read_text(
            encoding="utf-8"
        )

        size_bytes = target_file.stat().st_size
        line_count = len(
            content.splitlines()
        )

        ext = target_file.suffix.lower()

        language_map = {
            ".py": "python",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".js": "javascript",
            ".jsx": "javascript",
            ".json": "json",
            ".md": "markdown",
            ".html": "html",
            ".css": "css",
            ".rs": "rust",
            ".go": "go",
        }

        language = language_map.get(
            ext,
            "plaintext",
        )

        return {
            "path": file_path,
            "content": content,
            "language": language,
            "size_bytes": size_bytes,
            "line_count": line_count,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )