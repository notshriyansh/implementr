from collections import defaultdict
from typing import DefaultDict


class RepositoryGraph:
    def __init__(self) -> None:

        self.file_to_imports: DefaultDict[str, list[str]] = defaultdict(list)

        self.symbol_to_file: dict[str, str] = {}

        self.call_graph: DefaultDict[str, set[str]] = defaultdict(set)

        self.reverse_call_graph: DefaultDict[str, set[str]] = defaultdict(set)

    def add_file(
        self,
        file_path: str,
        imports: list[str],
    ) -> None:
        self.file_to_imports[
            file_path
        ] = imports

    def add_symbol(
        self,
        symbol_name: str,
        file_path: str,
    ) -> None:
        self.symbol_to_file[
            symbol_name
        ] = file_path

    def add_call(
        self,
        caller: str,
        callee: str,
    ) -> None:

        self.call_graph[
            caller
        ].add(callee)

        self.reverse_call_graph[
            callee
        ].add(caller)

    def get_related_files(
        self,
        file_path: str,
    ) -> list[str]:
        return self.file_to_imports.get(
            file_path,
            [],
        )

    def get_symbol_file(
        self,
        symbol_name: str,
    ) -> str | None:
        return self.symbol_to_file.get(
            symbol_name
        )

    def get_called_symbols(
        self,
        symbol_name: str,
    ) -> list[str]:
        return list(
            self.call_graph.get(
                symbol_name,
                [],
            )
        )

    def get_callers(
        self,
        symbol_name: str,
    ) -> list[str]:
        return list(
            self.reverse_call_graph.get(
                symbol_name,
                [],
            )
        )

    def trace_execution_path(
        self,
        start_symbol: str,
        depth: int = 3,
    ) -> list[dict]:

        visited = set()

        results = []

        def dfs(
            symbol: str,
            current_depth: int,
        ) -> None:

            if (
                current_depth > depth
                or symbol in visited
            ):
                return

            visited.add(symbol)

            callees = (
                self.get_called_symbols(
                    symbol
                )
            )

            callers = (
                self.get_callers(
                    symbol
                )
            )

            results.append(
                {
                    "symbol": symbol,
                    "file": (
                        self.get_symbol_file(
                            symbol
                        )
                    ),
                    "calls": callees,
                    "called_by": callers,
                }
            )

            for callee in callees:
                dfs(
                    callee,
                    current_depth + 1,
                )

        dfs(
            start_symbol,
            0,
        )

        return results
