from app.schemas.chunk import DocumentChunk


def deduplicate_chunks(
    chunks: list[DocumentChunk],
) -> list[DocumentChunk]:
    seen = set()

    unique_chunks = []

    for chunk in chunks:
        key = (
            chunk.paper_id,
            chunk.page_number,
            chunk.chunk_index,
        )

        if key not in seen:
            seen.add(key)

            unique_chunks.append(chunk)

    return unique_chunks

def limit_chunks(
    chunks: list[DocumentChunk],
    max_chunks: int = 5,
) -> list[DocumentChunk]:
    return chunks[:max_chunks]