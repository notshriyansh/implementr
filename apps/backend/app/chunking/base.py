from abc import ABC, abstractmethod

from app.schemas.chunk import DocumentChunk
from app.schemas.document import ParsedDocument


class BaseChunker(ABC):
    @abstractmethod
    async def chunk(
        self,
        document: ParsedDocument,
        paper_id: str,
        user_id: str,
    ) -> list[DocumentChunk]:
        pass