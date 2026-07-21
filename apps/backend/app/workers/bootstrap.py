from app.core.dependencies import (
    get_code_ingestion_service,
)

from app.db.session import SessionLocal

from app.orchestration.dispatcher import (
    JobDispatcher,
)

from app.orchestration.handlers.registry import (
    HandlerRegistry,
)

from app.orchestration.handlers.repository_index import (
    RepositoryIndexHandler,
)

from app.orchestration.enums import (
    JobType,
)


from app.workers.repository_worker import (
    RepositoryWorker,
)


def create_repository_worker() -> RepositoryWorker:


    ingestion_service = (
        get_code_ingestion_service()
    )

    handler_registry = HandlerRegistry()

    handler_registry.register(
        JobType.REPOSITORY_INDEX,
        RepositoryIndexHandler(
            ingestion_service,
        ),
    )

    dispatcher = JobDispatcher(
        handler_registry,
    )

    return RepositoryWorker(
        session_factory=SessionLocal,
        dispatcher=dispatcher,
    )