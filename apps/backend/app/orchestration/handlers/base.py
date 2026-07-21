from abc import ABC, abstractmethod

from app.db.models import Job

from app.orchestration.models import (
    JobExecutionResult,
)


class BaseJobHandler(ABC):

    @abstractmethod
    async def handle(
        self,
        job: Job,
    ) -> JobExecutionResult:
        
        raise NotImplementedError