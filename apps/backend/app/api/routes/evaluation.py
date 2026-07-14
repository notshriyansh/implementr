from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_benchmark_runner,
)
from app.evaluation.benchmark_runner import (
    BenchmarkRunner,
)

from app.evaluation.blueprint_eval import (
    BlueprintEvaluator,
)

from app.core.dependencies import (
    get_blueprint_evaluator,
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

@router.get("/blueprint")
async def evaluate_blueprint(
    question: str,
    evaluator: BlueprintEvaluator = Depends(
        get_blueprint_evaluator,
    ),
) -> dict:

    result = await (
        evaluator.evaluate(
            question=question,
            expected_files=[],
            expected_symbols=[],
            expected_gaps=[],
        )
    )

    return result.model_dump()