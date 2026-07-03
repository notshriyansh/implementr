from collections import defaultdict

from app.schemas.concept import (
    Concept,
)


class ConceptIndex:
    def __init__(self) -> None:
        self.index = defaultdict(list)

    def add(
        self,
        concept: Concept,
    ) -> None:
        self.index[
            concept.name
        ].append(concept)

    def get(
        self,
        concept_name: str,
    ) -> list[Concept]:
        return self.index.get(
            concept_name.lower(),
            [],
        )

    def clear(
        self,
    ) -> None:
        self.index.clear()

    def all(
        self,
    ) -> dict:
        return dict(self.index)