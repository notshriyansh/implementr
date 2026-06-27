from app.schemas.code_chunk import (
    CodeChunk,
)


def deduplicate_files(
    chunks: list[CodeChunk],
) -> list[CodeChunk]:
    seen_files = set()

    unique_chunks = []

    for chunk in chunks:
        if (
            chunk.file_path
            in seen_files
        ):
            continue

        seen_files.add(
            chunk.file_path
        )

        unique_chunks.append(
            chunk
        )

    return unique_chunks