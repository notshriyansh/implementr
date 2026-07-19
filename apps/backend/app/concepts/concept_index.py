from collections import defaultdict
from typing import DefaultDict

from app.schemas.concept import (
    Concept,
)


class ConceptIndex:
    def __init__(self) -> None:
        self.index: DefaultDict[str, list[Concept]] = defaultdict(list)

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
    ) -> dict[str, list[Concept]]:
        return dict(self.index)