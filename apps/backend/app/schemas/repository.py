from pydantic import BaseModel

from app.orchestration.enums import JobStatus
from app.sources.models import (
    LocalRepositoryModel,
    GithubRepositoryModel,
)


class RepositoryIngestionRequest(BaseModel):
    source: (
        LocalRepositoryModel
        | GithubRepositoryModel
    )


class RepositoryIngestionResponse(BaseModel):
    job_id: str
    status: JobStatus