from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_benchmark_runner,
)
from app.evaluation.benchmark_runner import (
    BenchmarkRunner,
)

router = APIRouter(
    prefix="/evaluation",
    tags=["evaluation"],
)


@router.get("/benchmarks")
async def run_benchmarks(
    runner: BenchmarkRunner = Depends(
        get_benchmark_runner,
    ),
) -> dict:
    return await runner.run()