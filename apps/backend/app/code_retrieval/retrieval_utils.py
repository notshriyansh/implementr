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
            chunk.relative_path
            in seen_files
        ):
            continue

        seen_files.add(
            chunk.relative_path
        )

        unique_chunks.append(
            chunk
        )

    return unique_chunks