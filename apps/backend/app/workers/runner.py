import asyncio
import logging

from app.core.config import get_settings
from app.workers.bootstrap import (
    create_repository_worker,
)

settings = get_settings()

logger = logging.getLogger(__name__)


class WorkerRunner:

    def __init__(
        self,
        *workers,
        poll_interval: float = settings.worker_poll_interval,
    ):
        self.workers = workers
        self.poll_interval = poll_interval
        self.running = True

    async def stop(self) -> None:
        logger.info("Stopping worker...")
        self.running = False

    async def run(self):

        logger.info("Worker started.")

        try:
            while self.running:

                processed = False

                for worker in self.workers:

                    if await worker.run_once():
                        processed = True

                if not processed:
                    await asyncio.sleep(
                        self.poll_interval
                    )

        except asyncio.CancelledError:
            logger.info("Worker cancelled.")

        finally:
            logger.info("Worker stopped.")


async def main():

    runner = WorkerRunner(
        create_repository_worker(),
    )

    try:
        await runner.run()

    except KeyboardInterrupt:
        await runner.stop()


if __name__ == "__main__":
    asyncio.run(main())