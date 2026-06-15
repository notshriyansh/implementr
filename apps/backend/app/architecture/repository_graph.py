from collections import defaultdict


class RepositoryGraph:
    def __init__(self) -> None:
        self.file_to_imports = (
            defaultdict(list)
        )

        self.symbol_to_file = {}

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