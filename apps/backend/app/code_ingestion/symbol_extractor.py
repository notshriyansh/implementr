import ast
import uuid
from pathlib import Path

from app.schemas.code_symbol import (
    CodeSymbol,
)


class SymbolExtractor:
    def extract_symbols(
        self,
        file_path: str,
    ) -> list[CodeSymbol]:

        path = Path(file_path)

        if path.suffix != ".py":
            return []

        try:
            source = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            tree = ast.parse(source)

        except Exception:
            return []

        lines = source.splitlines()

        symbols = []

        for node in ast.walk(tree):
            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                ),
            ):
                start = node.lineno

                end = getattr(
                    node,
                    "end_lineno",
                    start,
                )

                code = "\n".join(
                    lines[start - 1 : end]
                )

                symbol_type = (
                    "class"
                    if isinstance(
                        node,
                        ast.ClassDef,
                    )
                    else "function"
                )

                symbols.append(
                    CodeSymbol(
                        symbol_id=str(
                            uuid.uuid4()
                        ),
                        file_path=str(path),
                        symbol_name=node.name,
                        symbol_type=symbol_type,
                        code=code,
                        start_line=start,
                        end_line=end,
                    )
                )

        return symbols