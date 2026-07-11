from app.architecture.repository_graph import (
    RepositoryGraph,
)


class RepositoryReasoner:
    def __init__(
        self,
        graph: RepositoryGraph,
    ):
        self.graph = graph

    def trace_symbol(
        self,
        symbol_name: str,
    ) -> dict:

        return {
            "symbol": symbol_name,
            "file": (
                self.graph.get_symbol_file(
                    symbol_name
                )
            ),
            "calls": (
                self.graph.get_called_symbols(
                    symbol_name
                )
            ),
            "called_by": (
                self.graph.get_callers(
                    symbol_name
                )
            ),
            "execution_path": (
                self.graph.trace_execution_path(
                    symbol_name,
                    depth=3,
                )
            ),
        }