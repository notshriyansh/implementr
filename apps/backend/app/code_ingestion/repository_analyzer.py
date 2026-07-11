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
        repo_path: str,
    ) -> RepositoryMap:

        root = Path(repo_path)

        files = []

        files_to_analyze = [
            file
            for file in self.scanner.scan(
                repo_path
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

                parent_map = {}

                for parent in ast.walk(tree):
                    for child in ast.iter_child_nodes(
                        parent
                    ):
                        parent_map[
                            child
                        ] = parent

                imports = []

                functions = []

                classes = []

                relative_path = str(
                    file.relative_to(root)
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

                        parent = (
                            parent_map.get(
                                node
                            )
                        )

                        if isinstance(
                            parent,
                            ast.ClassDef,
                        ):
                            qualified_name = (
                                f"{parent.name}."
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
                                        f"{parent.name}."
                                        f"{child.func.attr}"
                                        if isinstance(
                                            parent,
                                            ast.ClassDef,
                                        )
                                        else child.func.attr
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