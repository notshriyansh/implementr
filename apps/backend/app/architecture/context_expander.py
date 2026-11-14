from app.architecture.repository_graph_registry import (
    RepositoryGraphRegistry,
)


class ContextExpander:
    def __init__(
        self,
        graph_registry: RepositoryGraphRegistry,
    ) -> None:
        self.graph_registry = graph_registry

    def expand(
        self,
        files: list[str],
        repository_id: str | None = None,
    ) -> list[str]:
        graph = (
            self.graph_registry.get(repository_id)
            if repository_id is not None
            else None
        )

        if graph is None:
            return list(dict.fromkeys(files))

        expanded = set(files)

        for file in files:
            imports = graph.get_related_files(file)
            expanded.update(imports)

        return sorted(expanded)
