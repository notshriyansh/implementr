import time
from collections.abc import Callable
from functools import wraps

from app.observability.logger import (
    setup_logger,
)

logger = setup_logger(
    "implementr.tracing"
)


def trace_execution(
    name: str,
):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(
            *args,
            **kwargs,
        ):
            start = time.perf_counter()

            logger.info(
                f"START: {name}"
            )

            result = await func(
                *args,
                **kwargs,
            )

            duration = (
                time.perf_counter()
                - start
            )

            logger.info(
                (
                    f"END: {name} | "
                    f"{duration:.2f}s"
                )
            )

            return result

        return wrapper

    return decorator