from app.concepts.concept_extractor import (
    ConceptExtractor,
)

from app.concepts.concept_matcher import (
    ConceptMatcher,
)


class ConceptService:
    def __init__(
        self,
        extractor: ConceptExtractor,
        matcher: ConceptMatcher,
    ) -> None:

        self.extractor = extractor

        self.matcher = matcher

    def build_concept_map(
        self,
        paper_text: str,
        code_text: str,
    ) -> list[dict]:

        paper_concepts = (
            self.extractor.extract(
                paper_text,
                source="paper",
            )
        )

        repo_concepts = (
            self.extractor.extract(
                code_text,
                source="repository",
            )
        )

        return self.matcher.match(
            paper_concepts,
            repo_concepts,
        )