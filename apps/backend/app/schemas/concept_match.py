from pydantic import BaseModel


class ConceptMatch(BaseModel):
    paper_concept: str

    repository_concept: str

    similarity: float