class GapAnalyzer:

    def analyze(
        self,
        paper_concepts: list[str],
        repo_concepts: list[str],
    ) -> list[str]:

        repo_set = {
            concept.lower()
            for concept
            in repo_concepts
        }

        gaps = []

        for concept in (
            paper_concepts
        ):

            if (
                concept.lower()
                not in repo_set
            ):
                gaps.append(
                    concept
                )

        return gaps