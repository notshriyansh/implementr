import re

from app.schemas.concept import (
    Concept,
)

from app.concepts.concept_keywords import (
    CONCEPT_KEYWORDS,
)


class ConceptExtractor:
    def extract(
        self,
        text: str,
        source: str,
    ) -> list[Concept]:

        text = text.lower()

        concepts: dict[str, int] = {}

        for keyword in CONCEPT_KEYWORDS:

            matches = re.findall(
                rf"\b{re.escape(keyword)}\w*\b",
                text,
            )

            if matches:
                concepts[keyword] = len(
                    matches
                )

        return [
            Concept(
                name=name,
                source=source,
                occurrences=count,
            )
            for name, count in concepts.items()
        ]