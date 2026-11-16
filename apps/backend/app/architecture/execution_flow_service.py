from app.architecture.repository_graph_registry import (
    RepositoryGraphRegistry,
)

from app.code_retrieval.symbol_retrieval_service import (
    SymbolRetrievalService,
)


class ExecutionFlowService:
    def __init__(
        self,
        graph_registry: RepositoryGraphRegistry,
        symbol_service: SymbolRetrievalService,
    ) -> None:
        self.graph_registry = graph_registry
        self.symbol_service = symbol_service

    async def expand_query(
        self,
        query: str,
        repository_id: str | None = None,
    ) -> dict:
        symbols = await self.symbol_service.retrieve(
            query=query,
            k=5,
            repository_id=repository_id,
        )

        graph = (
            self.graph_registry.get(repository_id)
            if repository_id is not None
            else None
        )

        expanded_context = []
        visited_files = set()
        execution_paths = []

        for symbol in symbols:
            file_path = symbol.relative_path
            visited_files.add(file_path)

            imports = (
                graph.get_related_files(file_path)
                if graph is not None
                else []
            )

            call_chain = (
                graph.trace_execution_path(
                    symbol.symbol_name,
                    depth=2,
                )
                if graph is not None
                else []
            )

            execution_paths.extend(call_chain)

            expanded_context.append(
                {
                    "symbol": symbol.symbol_name,
                    "file": file_path,
                    "imports": imports,
                    "calls": (
                        graph.get_called_symbols(symbol.symbol_name)
                        if graph is not None
                        else []
                    ),
                    "called_by": (
                        graph.get_callers(symbol.symbol_name)
                        if graph is not None
                        else []
                    ),
                }
            )

        return {
            "symbols": expanded_context,
            "visited_files": sorted(visited_files),
            "execution_paths": execution_paths,
        }