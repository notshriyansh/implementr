from app.schemas.code_chunk import CodeChunk


def deduplicate_files(
    chunks: list[CodeChunk],
) -> list[CodeChunk]:
    seen_files: set[tuple[str, str]] = set()
    unique_chunks: list[CodeChunk] = []

    for chunk in chunks:
        file_key = (
            chunk.repository_id,
            chunk.relative_path,
        )

        if file_key in seen_files:
            continue

        seen_files.add(file_key)
        unique_chunks.append(chunk)

    return unique_chunks
