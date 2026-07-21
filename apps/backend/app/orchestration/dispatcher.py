from app.db.models import Job

from app.orchestration.handlers.registry import (
    HandlerRegistry,
)

from app.orchestration.models import (
    JobExecutionResult,
)


class JobDispatcher:

    def __init__(
        self,
        registry: HandlerRegistry,
    ):
        self.registry = registry

    async def dispatch(
        self,
        job: Job,
    ) -> JobExecutionResult:

        handler = self.registry.get(
            job.job_type
        )

        if handler is None:
            raise ValueError(
                f"No handler registered for {job.job_type}"
            )

        return await handler.handle(job)