from pydantic import BaseModel


class Concept(
    BaseModel,
):
    name: str

    source: str

    description: str

    occurrences: int = 1