from app.architecture.repository_graph import (
    RepositoryGraph,
)

from app.code_retrieval.symbol_retrieval_service import (
    SymbolRetrievalService,
)


class ExecutionFlowService:
    def __init__(
        self,
        graph: RepositoryGraph,
        symbol_service: (
            SymbolRetrievalService
        ),
    ) -> None:

        self.graph = graph

        self.symbol_service = (
            symbol_service
        )

    async def expand_query(
        self,
        query: str,
    ) -> dict:

        symbols = await (
            self.symbol_service.retrieve(
                query=query,
                k=5,
            )
        )

        expanded_context = []

        visited_files = set()

        execution_paths = []

        for symbol in symbols:

            file_path = symbol.file_path

            visited_files.add(
                file_path
            )

            imports = (
                self.graph.get_related_files(
                    file_path
                )
            )

            call_chain = (
                self.graph
                .trace_execution_path(
                    symbol.symbol_name,
                    depth=2,
                )
            )

            execution_paths.extend(
                call_chain
            )

            expanded_context.append(
                {
                    "symbol": (
                        symbol.symbol_name
                    ),
                    "file": file_path,
                    "imports": imports,
                    "calls": (
                        self.graph
                        .get_called_symbols(
                            symbol.symbol_name
                        )
                    ),
                    "called_by": (
                        self.graph
                        .get_callers(
                            symbol.symbol_name
                        )
                    ),
                }
            )

        return {
            "symbols": expanded_context,
            "visited_files": list(
                visited_files
            ),
            "execution_paths": (
                execution_paths
            ),
        }