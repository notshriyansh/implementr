class ConceptMapper:

    def build_mapping(
        self,
        paper_concepts: list[str],
        repo_concepts: list[str],
    ) -> list[dict]:

        mappings = []

        for paper_concept in (
            paper_concepts
        ):

            for repo_concept in (
                repo_concepts
            ):

                if (
                    paper_concept.lower()
                    in repo_concept.lower()
                    or
                    repo_concept.lower()
                    in paper_concept.lower()
                ):
                    mappings.append(
                        {
                            "paper": (
                                paper_concept
                            ),
                            "repo": (
                                repo_concept
                            ),
                        }
                    )

        return mappings