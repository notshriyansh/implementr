from pydantic import BaseModel

from app.orchestration.enums import JobStatus


class RepositoryIngestionResponse(BaseModel):
    job_id: str
    status: JobStatus