from pydantic import BaseModel


class BlueprintEvaluationResult(
    BaseModel,
):
    target_file_score: float

    target_symbol_score: float

    gap_coverage_score: float

    implementation_score: float

    risk_score: float

    overall_score: float