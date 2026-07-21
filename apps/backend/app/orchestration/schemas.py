from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict

from app.orchestration.enums import JobStatus
from app.orchestration.enums import JobType


class CreateJobRequest(BaseModel):

    job_type: JobType

    payload: dict[str, Any] = Field(
        default_factory=dict,
    )


class JobResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str

    job_type: JobType

    status: JobStatus

    payload: dict[str, Any]

    result: dict[str, Any] | None

    error: str | None

    created_at: datetime

    claimed_at: datetime | None

    started_at: datetime | None

    completed_at: datetime | None


class ClaimJobResponse(BaseModel):

    id: str

    job_type: JobType

    payload: dict[str, Any]


class CompleteJobRequest(BaseModel):

    result: dict[str, Any] = Field(
        default_factory=dict,
    )


class FailJobRequest(BaseModel):

    error: str