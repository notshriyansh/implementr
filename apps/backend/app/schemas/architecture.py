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

    confidence: float

    reasoning: str
