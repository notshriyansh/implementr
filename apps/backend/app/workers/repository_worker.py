from collections.abc import Callable

from sqlalchemy.orm import Session

from app.orchestration.dispatcher import JobDispatcher
from app.orchestration.service import JobService


class RepositoryWorker:
    
    def __init__(
        self,
        session_factory: Callable[[], Session],
        dispatcher: JobDispatcher,
    ) -> None:
        self.session_factory = session_factory
        self.dispatcher = dispatcher

    async def run_once(self) -> bool:

        db = self.session_factory()

        try:
            job_service = JobService(db)

            job = job_service.claim_next()

            if job is None:
                return False

            try:
                result = await self.dispatcher.dispatch(job)

                job_service.complete(
                    job.id,
                    result.result,
                )

            except Exception as exc:

                job_service.fail(
                    job.id,
                    str(exc),
                )

            return True

        finally:
            db.close()