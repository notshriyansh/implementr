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
                (
                    f"START | "
                    f"operation={name}"
                )
            )

            try:
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
                        f"SUCCESS | "
                        f"operation={name} | "
                        f"duration={duration:.2f}s"
                    )
                )

                return result

            except Exception as e:
                duration = (
                    time.perf_counter()
                    - start
                )

                logger.exception(
                    (
                        f"FAILURE | "
                        f"operation={name} | "
                        f"duration={duration:.2f}s | "
                        f"error={str(e)}"
                    )
                )

                raise

        return wrapper

    return decorator
