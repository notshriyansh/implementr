import numpy as np

from app.embeddings.base import BaseEmbeddingModel

from app.schemas.concept import Concept
from app.schemas.concept_match import ConceptMatch


class ConceptMatcher:
    def __init__(
        self,
        embedding_model: BaseEmbeddingModel,
    ) -> None:
        self.embedding_model = embedding_model

    async def match(
        self,
        paper_concepts: list[Concept],
        repo_concepts: list[Concept],
        threshold: float = 0.40,
    ) -> list[ConceptMatch]:

        if not paper_concepts or not repo_concepts:
            return []

        paper_names = [
            c.name
            for c in paper_concepts
        ]

        repo_names = [
            c.name
            for c in repo_concepts
        ]

        paper_embeddings = (
            await self.embedding_model.embed_texts(
                paper_names
            )
        )

        repo_embeddings = (
            await self.embedding_model.embed_texts(
                repo_names
            )
        )

        paper_embeddings = paper_embeddings / np.linalg.norm(
            paper_embeddings,
            axis=1,
            keepdims=True,
        )

        repo_embeddings = repo_embeddings / np.linalg.norm(
            repo_embeddings,
            axis=1,
            keepdims=True,
        )

        matches: list[ConceptMatch] = []

        for i, paper_embedding in enumerate(
            paper_embeddings
        ):

            similarities = (
                repo_embeddings @ paper_embedding
            )

            best_idx = int(
                similarities.argmax()
            )

            best_score = float(
                similarities[best_idx]
            )

            if best_score >= threshold:

                matches.append(
                    ConceptMatch(
                        paper_concept=paper_names[i],
                        repository_concept=repo_names[
                            best_idx
                        ],
                        similarity=round(
                            best_score,
                            3,
                        ),
                    )
                )

        return matches