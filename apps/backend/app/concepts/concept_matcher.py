from app.concepts.concept import (
    Concept,
)


class ConceptMatcher:
    def match(
        self,
        paper_concepts: list[Concept],
        repo_concepts: list[Concept],
    ) -> list[dict]:

        matches = []

        repo_lookup = {
            concept.name.lower(): concept
            for concept in repo_concepts
        }

        for paper_concept in (
            paper_concepts
        ):

            paper_name = (
                paper_concept.name.lower()
            )

            for (
                repo_key,
                repo_concept,
            ) in repo_lookup.items():

                if (
                    paper_name in repo_key
                    or repo_key in paper_name
                ):
                    matches.append(
                        {
                            "paper_concept":
                                paper_concept.name,
                            "repository_concept":
                                repo_concept.name,
                        }
                    )

        return matches