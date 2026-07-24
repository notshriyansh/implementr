import asyncio

from app.workers.bootstrap import (
    create_repository_worker,
)

from app.core.config import get_settings

settings = get_settings()


class WorkerRunner:

    def __init__(
        self,
        *workers,
        poll_interval: float = settings.worker_poll_interval,
    ):
        self.workers = workers
        self.poll_interval = poll_interval

    async def run(self):

        while True:

            processed = False

            for worker in self.workers:

                if await worker.run_once():
                    processed = True

            if not processed:
                await asyncio.sleep(
                    self.poll_interval
                )


async def main():

    runner = WorkerRunner(
        create_repository_worker(),
    )

    await runner.run()


if __name__ == "__main__":
    asyncio.run(main())