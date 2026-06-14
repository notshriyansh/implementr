import uuid
from pathlib import Path

from app.schemas.code_chunk import (
    CodeChunk,
)


class CodeChunker:
    def __init__(
        self,
        chunk_size: int = 80,
    ) -> None:
        self.chunk_size = chunk_size

    def chunk_file(
        self,
        file_path: Path,
    ) -> list[CodeChunk]:
        text = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        lines = text.splitlines()

        chunks = []

        for i in range(
            0,
            len(lines),
            self.chunk_size,
        ):
            chunk_lines = lines[
                i : i + self.chunk_size
            ]

            chunk_text = "\n".join(
                chunk_lines
            )

            chunks.append(
                CodeChunk(
                    chunk_id=str(
                        uuid.uuid4()
                    ),
                    file_path=str(
                        file_path
                    ),
                    language=(
                        file_path.suffix
                    ),
                    content=chunk_text,
                    start_line=i + 1,
                    end_line=min(
                        i + self.chunk_size,
                        len(lines),
                    ),
                )
            )

        return chunks