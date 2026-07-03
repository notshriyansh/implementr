from sentence_transformers import (
    SentenceTransformer,
)

from app.schemas.concept import (
    Concept,
)

from app.schemas.concept_match import (
    ConceptMatch,
)


class ConceptMatcher:
    def __init__(
        self,
        model_name: str = (
            "all-MiniLM-L6-v2"
        ),
    ) -> None:

        self.model = (
            SentenceTransformer(
                model_name
            )
        )

    def match(
        self,
        paper_concepts: list[Concept],
        repo_concepts: list[Concept],
        threshold: float = 0.40,
    ) -> list[ConceptMatch]:

        if (
            not paper_concepts
            or not repo_concepts
        ):
            return []

        paper_names = [
            concept.name
            for concept in paper_concepts
        ]

        repo_names = [
            concept.name
            for concept in repo_concepts
        ]

        paper_embeddings = (
            self.model.encode(
                paper_names,
                normalize_embeddings=True,
            )
        )

        repo_embeddings = (
            self.model.encode(
                repo_names,
                normalize_embeddings=True,
            )
        )

        matches = []

        for i, paper_embedding in enumerate(
            paper_embeddings
        ):

            similarities = (
                repo_embeddings
                @ paper_embedding
            )

            best_idx = (
                similarities.argmax()
            )

            best_score = float(
                similarities[
                    best_idx
                ]
            )

            if (
                best_score
                >= threshold
            ):
                matches.append(
                    ConceptMatch(
                        paper_concept=(
                            paper_names[i]
                        ),
                        repository_concept=(
                            repo_names[
                                best_idx
                            ]
                        ),
                        similarity=(
                            round(
                                best_score,
                                3,
                            )
                        ),
                    )
                )

        return matches