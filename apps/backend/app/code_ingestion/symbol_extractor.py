import ast
import uuid

from pathlib import Path

from app.schemas.code_symbol import (
    CodeSymbol,
)

from app.code_ingestion.symbol_constants import (
    STOP_SYMBOLS,
    HIGH_VALUE_SUFFIXES,
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

            if not isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                ),
            ):
                continue

            if node.name in STOP_SYMBOLS:
                continue

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

            importance = 1

            if symbol_type == "class":
                importance += 2

            if any(
                node.name.endswith(
                    suffix
                )
                for suffix in HIGH_VALUE_SUFFIXES
            ):
                importance += 3

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
                    importance=importance,
                )
            )

        return symbols