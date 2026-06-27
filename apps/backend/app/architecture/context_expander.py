from app.architecture.repository_graph import (
    RepositoryGraph,
)


class ContextExpander:
    def __init__(
        self,
        graph: RepositoryGraph,
    ) -> None:
        self.graph = graph

    def expand_files(
        self,
        files: list[str],
    ) -> list[str]:

        expanded = set(files)

        for file in files:
            imports = (
                self.graph.get_related_files(
                    file
                )
            )

            expanded.update(imports)

        return list(expanded)