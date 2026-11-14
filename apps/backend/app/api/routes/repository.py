from fastapi import APIRouter, Depends, HTTPException

from app.code_ingestion.ingestion_service import CodeIngestionService
from app.code_ingestion.repository_analyzer import RepositoryAnalyzer
from app.code_ingestion.repository_scanner import (
    IGNORED_DIRECTORIES,
    SUPPORTED_EXTENSIONS,
)
from app.code_retrieval.code_retrieval_service import CodeRetrievalService
from app.core.dependencies import (
    get_code_ingestion_service,
    get_code_retrieval_service,
    get_repository_analyzer,
    get_repository_registry,
)
from app.repository_sources.repository_registry import RepositoryRegistry

router = APIRouter(
    prefix="/repository",
    tags=["repository"],
)


@router.post("/ingest")
async def ingest_repository(
    location: str,
    ingestion_service: CodeIngestionService = Depends(
        get_code_ingestion_service,
    ),
) -> dict:
    location = location.strip()

    try:
        chunks = await ingestion_service.ingest_repository(location)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch the GitHub repository.",
        ) from exc

    repository = ingestion_service.repository_info

    return {
        "repository": repository.repository_name if repository else None,
        "repository_id": repository.repository_id if repository else None,
        "repository_root": str(repository.repository_root) if repository else None,
        "source": repository.source if repository else None,
        "total_chunks": len(chunks),
        "sample_chunk": chunks[0] if chunks else None,
    }


@router.get("/search")
async def search_repository(
    query: str,
    repository_id: str | None = None,
    retrieval_service: CodeRetrievalService = Depends(
        get_code_retrieval_service,
    ),
) -> dict:
    chunks = await retrieval_service.retrieve(
        query=query,
        k=5,
        repository_id=repository_id,
    )

    return {"results": chunks}


@router.get("/structure")
async def analyze_repository(
    repository_id: str,
    analyzer: RepositoryAnalyzer = Depends(get_repository_analyzer),
    registry: RepositoryRegistry = Depends(get_repository_registry),
) -> dict:
    try:
        repository_root = registry.resolve_root(repository_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail="Repository not found. Please ingest it again.",
        ) from exc
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="Repository files are no longer available.",
        ) from exc

    result = analyzer.analyze(
        repo_path=str(repository_root),
        repository_id=repository_id,
    )

    return result.model_dump()


@router.get("/file")
async def get_file_content(
    repository_id: str,
    file_path: str,
    registry: RepositoryRegistry = Depends(get_repository_registry),
) -> dict:
    try:
        repository_root, target_file = registry.resolve_file_with_root(
            repository_id,
            file_path,
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail="Repository not found. Please ingest it again.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid file path",
        ) from exc
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        ) from exc

    relative_path = target_file.relative_to(repository_root)

    if any(part in IGNORED_DIRECTORIES for part in relative_path.parts):
        raise HTTPException(status_code=404, detail="File not found")

    if target_file.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        content = target_file.read_text(encoding="utf-8")
        size_bytes = target_file.stat().st_size
    except (OSError, UnicodeDecodeError) as exc:
        raise HTTPException(
            status_code=400,
            detail="Unable to read this source file",
        ) from exc

    language_map = {
        ".py": "python",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
        ".cpp": "cpp",
        ".c": "c",
    }

    return {
        "path": relative_path.as_posix(),
        "content": content,
        "language": language_map.get(target_file.suffix.lower(), "plaintext"),
        "size_bytes": size_bytes,
        "line_count": len(content.splitlines()),
    }
