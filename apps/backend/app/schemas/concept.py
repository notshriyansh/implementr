from pydantic import BaseModel


class Concept(BaseModel):
    name: str

    source: str

    description: str = ""

    occurrences: int = 1

    file_path: str | None = None

    symbol_name: str | None = None

    confidence: float = 1.0