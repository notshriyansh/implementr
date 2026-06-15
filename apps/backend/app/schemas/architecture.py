from pydantic import BaseModel


class ArchitectureInsight(BaseModel):
    query: str

    summary: str

    relevant_files: list[str]

    relevant_symbols: list[str]

    reasoning: str