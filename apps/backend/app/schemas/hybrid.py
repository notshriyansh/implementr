from pydantic import BaseModel


class HybridAnalysisResponse(
    BaseModel
):
    summary: str

    relevant_files: list[str]

    relevant_symbols: list[str]

    implementation_steps: list[str]

    risks: list[str]

    confidence: float

    reasoning: str