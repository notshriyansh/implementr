import ast

from pathlib import Path

from app.schemas.repository_map import (
    FileNode,
    RepositoryMap,
)

from app.architecture.repository_graph import (
    RepositoryGraph,
)


class RepositoryAnalyzer:
    def __init__(
        self,
        graph: RepositoryGraph,
    ) -> None:
        self.graph = graph

    def analyze(
        self,
        repo_path: str,
    ) -> RepositoryMap:
        root = Path(repo_path)

        files = []

        for file in root.rglob("*.py"):
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

                        functions.append(
                            node.name
                        )

                        self.graph.add_symbol(
                            symbol_name=node.name,
                            file_path=str(
                                file.relative_to(root)
                            ),
                        )

                        for child in ast.walk(node):

                            if isinstance(
                                child,
                                ast.Call,
                            ):

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
                                    called_name = (
                                        child.func.attr
                                    )

                                if called_name:
                                    self.graph.add_call(
                                        caller=node.name,
                                        callee=called_name,
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
                            file_path=str(
                                file.relative_to(root)
                            ),
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