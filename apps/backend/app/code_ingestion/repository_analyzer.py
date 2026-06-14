import ast
from pathlib import Path

from app.schemas.repository_map import (
    FileNode,
    RepositoryMap,
)


class RepositoryAnalyzer:
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

                for node in ast.walk(tree):
                    if isinstance(
                        node,
                        ast.Import,
                    ):
                        imports.extend(
                            alias.name
                            for alias in (
                                node.names
                            )
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
                        ast.FunctionDef,
                    ):
                        functions.append(
                            node.name
                        )

                    elif isinstance(
                        node,
                        ast.ClassDef,
                    ):
                        classes.append(
                            node.name
                        )

                files.append(
                    FileNode(
                        path=str(
                            file.relative_to(
                                root
                            )
                        ),
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