from pydantic import BaseModel


class ArchitectureInsight(
    BaseModel
):
    query: str

    summary: str

    relevant_files: list[str]

    relevant_symbols: list[str]

    execution_steps: list[str]

    engineering_notes: list[str]

    modification_points: list[str]

    entrypoints: list[str]

    execution_flow: list[str]

    affected_files: list[str]

    modification_order: list[str]

    confidence: float

    reasoning: str