from app.architecture.repository_graph import (
    RepositoryGraph,
)


class RepositoryReasoner:
    def __init__(
        self,
        graph: RepositoryGraph,
    ):
        self.graph = graph

    def trace(
        self,
        file_path: str,
    ) -> dict:

        imports = (
            self.graph.get_related_files(
                file_path
            )
        )

        return {
            "entry_file": file_path,
            "imports": imports,
        }