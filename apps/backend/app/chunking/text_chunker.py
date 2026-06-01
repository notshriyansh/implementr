import uuid

from app.chunking.base import BaseChunker
from app.schemas.chunk import DocumentChunk
from app.schemas.document import ParsedDocument


class TextChunker(BaseChunker):
    CHUNK_SIZE = 1200

    async def chunk(
        self,
        document: ParsedDocument,
        paper_id: str,
        user_id: str,
    ) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []

        chunk_index = 0

        for page in document.pages:
            text = page.text

            start = 0

            while start < len(text):
                end = start + self.CHUNK_SIZE

                chunk_text = text[start:end]

                chunks.append(
                    DocumentChunk(
                        chunk_id=str(
                            uuid.uuid4()
                        ),
                        text=chunk_text,
                        page_number=page.page_number,
                        chunk_index=chunk_index,
                        paper_id=paper_id,
                        user_id=user_id,
                    )
                )

                chunk_index += 1

                start = end

        return chunks