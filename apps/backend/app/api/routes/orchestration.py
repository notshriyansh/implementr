from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.core.dependencies import get_job_service

from app.orchestration.service import JobService

from app.orchestration.schemas import (
    ClaimJobResponse,
    CompleteJobRequest,
    CreateJobRequest,
    FailJobRequest,
    JobResponse,
)

router = APIRouter(
    prefix="/orchestration",
    tags=["Orchestration"],
)

@router.post(
    "/jobs",
    response_model=JobResponse,
)
def create_job(
    request: CreateJobRequest,
    service: JobService = Depends(
        get_job_service,
    ),
):

    job = service.create(
        job_type=request.job_type,
        payload=request.payload,
    )

    return JobResponse.model_validate(job)

@router.get(
    "/jobs/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: str,
    service: JobService = Depends(
        get_job_service,
    ),
):

    job = service.get(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return JobResponse.model_validate(job)

@router.get(
    "/jobs",
    response_model=list[JobResponse],
)
def list_jobs(
    service: JobService = Depends(
        get_job_service,
    ),
):

    return [
        JobResponse.model_validate(job)
        for job in service.list()
    ]


@router.post(
    "/jobs/claim",
    response_model=ClaimJobResponse | None,
)
def claim_job(
    service: JobService = Depends(
        get_job_service,
    ),
):

    job = service.claim_next()

    if job is None:
        return None

    return ClaimJobResponse(
        id=job.id,
        job_type=job.job_type,
        payload=job.payload,
    )



@router.post(
    "/jobs/{job_id}/complete",
    response_model=JobResponse,
)
def complete_job(
    job_id: str,
    request: CompleteJobRequest,
    service: JobService = Depends(get_job_service),
):
    try:
        job = service.complete(
            job_id,
            request.result,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return JobResponse.model_validate(job)


@router.post(
    "/jobs/{job_id}/fail",
    response_model=JobResponse,
)
def fail_job(
    job_id: str,
    request: FailJobRequest,
    service: JobService = Depends(
        get_job_service,
    ),
):

    try:
        job = service.fail(
            job_id,
            request.error,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return JobResponse.model_validate(job)


