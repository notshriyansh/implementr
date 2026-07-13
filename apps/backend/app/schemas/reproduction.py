from pydantic import BaseModel


class ResearchReproductionPlan(
    BaseModel,
):
    paper_summary: str

    repository_targets: list[str]

    required_changes: list[str]

    training_changes: list[str]

    evaluation_changes: list[str]

    benchmark_tasks: list[str]

    success_criteria: list[str]

    risks: list[str]

    confidence: float

    concept_mappings: list[str]

    architecture_gaps: list[str]

    implementation_steps: list[str]

    modification_targets: list[str]

    gap_to_symbol_mapping: list[str]