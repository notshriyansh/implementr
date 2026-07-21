from app.orchestration.enums import JobType

from app.orchestration.handlers.base import (
    BaseJobHandler,
)


class HandlerRegistry:

    def __init__(self):
        self._handlers: dict[
            JobType,
            BaseJobHandler,
        ] = {}

    def register(
        self,
        job_type: JobType,
        handler: BaseJobHandler,
    ) -> None:
        self._handlers[job_type] = handler

    def get(
        self,
        job_type: JobType,
    ) -> BaseJobHandler | None:
        return self._handlers.get(job_type)