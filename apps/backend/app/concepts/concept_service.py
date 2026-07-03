import re

from app.schemas.concept import (
    Concept,
)

from app.concepts.concept_extractor import (
    ConceptExtractor,
)

from app.concepts.concept_matcher import (
    ConceptMatcher,
)

from app.schemas.code_symbol import (
    CodeSymbol,
)

from app.concepts.constants import (
    IGNORED_CONCEPTS,
)


class ConceptService:
    def __init__(
        self,
        extractor: ConceptExtractor,
        matcher: ConceptMatcher,
    ) -> None:

        self.extractor = extractor

        self.matcher = matcher

    def symbol_to_concepts(
        self,
        symbol: CodeSymbol,
    ) -> list[Concept]:

        parts = re.findall(
            r"[A-Z]?[a-z]+",
            symbol.symbol_name,
        )

        concepts = []

        for part in parts:
            if (
                len(part) < 3
                or part.lower() in IGNORED_CONCEPTS
            ):
                continue

            concepts.append(
                Concept(
                    name=part.lower(),
                    source="repository",
                    file_path=(
                        symbol.file_path
                    ),
                    symbol_name=(
                        symbol.symbol_name
                    ),
                )
            )

        return concepts

    def build_concept_map(
        self,
        paper_text: str,
        symbols: list[CodeSymbol],
    ) -> dict:

        paper_concepts = (
            self.extractor.extract(
                paper_text,
                source="paper",
            )
        )

        repository_concepts = []

        for symbol in symbols:

            repository_concepts.extend(
                self.symbol_to_concepts(
                    symbol
                )
            )

        matches = (
            self.matcher.match(
                paper_concepts,
                repository_concepts,
            )
        )

        return {
            "paper_concepts":
                paper_concepts,
            "repository_concepts":
                repository_concepts,
            "matches":
                matches,
        }