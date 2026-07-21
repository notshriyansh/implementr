from app.code_ingestion.ingestion_service import (
    CodeIngestionService,
)

from app.db.models import Job

from app.orchestration.handlers.base import (
    BaseJobHandler,
)

from app.orchestration.models import (
    JobExecutionResult,
)


class RepositoryIndexHandler(
    BaseJobHandler,
):
    def __init__(
        self,
        ingestion_service: CodeIngestionService,
    ):
        self.ingestion_service = ingestion_service

    async def handle(
        self,
        job: Job,
    ) -> JobExecutionResult:

        payload = job.payload or {}

        repo_path = payload.get(
            "repo_path"
        )

        if not repo_path:
            raise ValueError(
                "Repository job missing repo_path."
            )

        chunk_count = (
            await self.ingestion_service.ingest_repository(
                repo_path
            )
        )

        return JobExecutionResult(
            result={
                "repo_path": repo_path,
                "chunk_count": chunk_count,
            }
        )