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

        for symbol in symbols:
            file_path = symbol.file_path

            visited_files.add(file_path)

            imports = (
                self.graph.get_related_files(
                    file_path
                )
            )

            expanded_context.append(
                {
                    "symbol": (
                        symbol.symbol_name
                    ),
                    "file": file_path,
                    "imports": imports,
                }
            )

        return {
            "symbols": expanded_context,
            "visited_files": list(
                visited_files
            ),
        }