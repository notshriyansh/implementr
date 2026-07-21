from datetime import datetime

from sqlalchemy.orm import Session

from typing import Any

from app.db.models import Job
from app.orchestration.enums import JobStatus
from app.orchestration.enums import JobType


class JobService:

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def _ensure_status(
        self,
        job: Job,
        expected: JobStatus,
    ) -> None:

        if job.status != expected:
            raise ValueError(
                f"Expected {expected}, got {job.status}"
            )

    def create(
        self,
        job_type: JobType,
        payload: dict[str, Any],
    ) -> Job:
        job = Job(
            job_type=job_type,
            payload=payload,
            status=JobStatus.QUEUED,
        )

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job

    def get(
        self,
        job_id: str,
    ) -> Job | None:
        return (
            self.db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )

    def list(
        self,
    ) -> list[Job]:
        return (
            self.db.query(Job)
            .order_by(Job.created_at.desc())
            .all()
        )

    def claim_next(
        self,
    ) -> Job | None:

        job = (
            self.db.query(Job)
            .filter(Job.status == JobStatus.QUEUED)
            .order_by(Job.created_at)
            .first()
        )

        if job is None:
            return None

        now = datetime.utcnow()

        job.status = JobStatus.RUNNING
        job.claimed_at = now
        job.started_at = now

        self.db.commit()
        self.db.refresh(job)

        return job

    def complete(
        self,
        job_id: str,
        result: dict[str, Any],
    ) -> Job | None:

        job = self.get(job_id)

        if job is None:
            return None
        
        self._ensure_status(
            job,
            JobStatus.RUNNING,
        )

        job.status = JobStatus.COMPLETED
        job.result = result
        job.completed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(job)

        return job

    def fail(
        self,
        job_id: str,
        error: str,
    ) -> Job | None:

        job = self.get(job_id)

        if job is None:
            return None

        if job.status not in (
            JobStatus.CLAIMED,
            JobStatus.RUNNING,
        ):
            raise ValueError(
                f"Cannot fail job in state {job.status}"
            )

        job.status = JobStatus.FAILED
        job.error = error
        job.completed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(job)

        return job