from collections import defaultdict
from typing import DefaultDict

from app.schemas.concept import Concept


class ConceptIndex:
    def __init__(self) -> None:
        self.index: DefaultDict[str, list[Concept]] = defaultdict(list)

    def add(self, concept: Concept) -> None:
        self.index[concept.name].append(concept)

    def get(self, concept_name: str) -> list[Concept]:
        return self.index.get(concept_name.lower(), [])

    def clear(self) -> None:
        self.index.clear()

    def all(self) -> dict[str, list[Concept]]:
        return dict(self.index)

    def replace_repository(
        self,
        repository_id: str,
        concepts: list[Concept],
    ) -> None:
        if any(
            concept.repository_id != repository_id
            for concept in concepts
        ):
            raise ValueError(
                "All replacement concepts must belong to the specified repository."
            )

        updated_index: DefaultDict[str, list[Concept]] = defaultdict(list)

        for name, existing_concepts in self.index.items():
            preserved = [
                concept
                for concept in existing_concepts
                if concept.repository_id != repository_id
            ]

            if preserved:
                updated_index[name].extend(preserved)

        for concept in concepts:
            updated_index[concept.name].append(concept)

        self.index = updated_index
