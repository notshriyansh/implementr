import ast

from pathlib import Path

from app.schemas.repository_map import (
    FileNode,
    RepositoryMap,
)

from app.architecture.repository_graph import (
    RepositoryGraph,
)

from app.code_ingestion.repository_scanner import (
    RepositoryScanner,
)


class RepositoryAnalyzer:
    def __init__(
        self,
        graph: RepositoryGraph,
        scanner: RepositoryScanner,
    ) -> None:
        self.graph = graph
        self.scanner = scanner

    def analyze(
        self,
        repository_root: Path,
    ) -> RepositoryMap:


        files = []

        files_to_analyze = [
            file
            for file in self.scanner.scan(
                repository_root
            )
            if file.suffix == ".py"
        ]

        for file in files_to_analyze:

            if any(
                ignored in file.parts
                for ignored in [
                    ".venv",
                    "__pycache__",
                    ".git",
                ]
            ):
                continue

            try:
                source = file.read_text(
                    encoding="utf-8",
                )

                tree = ast.parse(source)

                parent_map: dict[ast.AST, ast.AST] = {}

                for parent_node in ast.walk(tree):
                    for child in ast.iter_child_nodes(
                        parent_node
                    ):
                        parent_map[
                            child
                        ] = parent_node

                imports: list[str] = []

                functions = []

                classes = []

                relative_path = str(
                    file.relative_to(
                        repository_root
                    )
                )

                for node in ast.walk(tree):

                    if isinstance(
                        node,
                        ast.Import,
                    ):
                        imports.extend(
                            alias.name
                            for alias in node.names
                        )

                    elif isinstance(
                        node,
                        ast.ImportFrom,
                    ):
                        if node.module:
                            imports.append(
                                node.module
                            )

                    elif isinstance(
                        node,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef,
                        ),
                    ):

                        enclosing_parent = (
                            parent_map.get(
                                node
                            )
                        )

                        if isinstance(
                            enclosing_parent,
                            ast.ClassDef,
                        ):
                            qualified_name = (
                                f"{enclosing_parent.name}."
                                f"{node.name}"
                            )
                        else:
                            qualified_name = (
                                node.name
                            )

                        functions.append(
                            qualified_name
                        )

                        self.graph.add_symbol(
                            symbol_name=(
                                qualified_name
                            ),
                            file_path=(
                                relative_path
                            ),
                        )

                        for child in ast.walk(
                            node
                        ):

                            if not isinstance(
                                child,
                                ast.Call,
                            ):
                                continue

                            called_name = None

                            if isinstance(
                                child.func,
                                ast.Name,
                            ):
                                called_name = (
                                    child.func.id
                                )

                            elif isinstance(
                                child.func,
                                ast.Attribute,
                            ):

                                if (
                                    isinstance(
                                        child.func.value,
                                        ast.Name,
                                    )
                                    and child.func.value.id
                                    == "self"
                                ):
                                    called_name = (
                                        f"{enclosing_parent.name}."
                                        f"{child.func.attr}"
                                        if isinstance(
                                            enclosing_parent,
                                            ast.ClassDef,
                                        )
                                        else child.func.attr
                                    )

                                elif (
                                    isinstance(
                                        child.func.value,
                                        ast.Attribute,
                                    )
                                    and isinstance(
                                        child.func.value.value,
                                        ast.Name,
                                    )
                                    and child.func.value.value.id
                                    == "self"
                                ):
                                    called_name = (
                                        f"{child.func.value.attr}."
                                        f"{child.func.attr}"
                                    )

                                elif isinstance(
                                    child.func.value,
                                    ast.Name,
                                ):
                                    called_name = (
                                        f"{child.func.value.id}."
                                        f"{child.func.attr}"
                                    )

                                else:
                                    called_name = (
                                        child.func.attr
                                    )

                            if called_name:

                                self.graph.add_call(
                                    caller=(
                                        qualified_name
                                    ),
                                    callee=(
                                        called_name
                                    ),
                                )

                    elif isinstance(
                        node,
                        ast.ClassDef,
                    ):

                        classes.append(
                            node.name
                        )

                        self.graph.add_symbol(
                            symbol_name=node.name,
                            file_path=relative_path,
                        )

                self.graph.add_file(
                    file_path=relative_path,
                    imports=imports,
                )

                files.append(
                    FileNode(
                        path=relative_path,
                        imports=imports,
                        functions=functions,
                        classes=classes,
                    )
                )

            except Exception:
                continue

        return RepositoryMap(
            files=files
        )