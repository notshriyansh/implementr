import re

from app.concepts.concept import (
    Concept,
)


class ConceptExtractor:
    def extract(
        self,
        text: str,
        source: str,
    ) -> list[Concept]:

        matches = re.findall(
            r"\b[A-Z][A-Za-z0-9_]+\b",
            text,
        )

        concepts = {}

        for match in matches:

            if match not in concepts:
                concepts[match] = 0

            concepts[match] += 1

        return [
            Concept(
                name=name,
                source=source,
                description="",
                occurrences=count,
            )
            for name, count in concepts.items()
        ]