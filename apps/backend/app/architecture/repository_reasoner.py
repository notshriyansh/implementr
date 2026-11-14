from app.architecture.repository_graph_registry import (
    RepositoryGraphRegistry,
)


class RepositoryReasoner:
    def __init__(
        self,
        graph_registry: RepositoryGraphRegistry,
    ):
        self.graph_registry = graph_registry

    def trace_symbol(
        self,
        symbol_name: str,
        repository_id: str,
    ) -> dict:
        graph = self.graph_registry.get(repository_id)

        if graph is None:
            return {
                "symbol": symbol_name,
                "file": None,
                "calls": [],
                "called_by": [],
                "execution_path": [],
            }

        return {
            "symbol": symbol_name,
            "file": graph.get_symbol_file(symbol_name),
            "calls": graph.get_called_symbols(symbol_name),
            "called_by": graph.get_callers(symbol_name),
            "execution_path": graph.trace_execution_path(
                symbol_name,
                depth=3,
            ),
        }