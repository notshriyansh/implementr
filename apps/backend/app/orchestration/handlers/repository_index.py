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
from app.sources.factory import RepositorySourceFactory


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

        source_payload = payload.get("source")

        if source_payload is None:
            raise ValueError("Missing repository source.")

        source = RepositorySourceFactory.create_from_dict(
            source_payload
        )

        chunk_count = await self.ingestion_service.ingest_repository(
            source
        )

        return JobExecutionResult(
            result={
                "source": source_payload,
                "chunk_count": chunk_count,
            }
        )