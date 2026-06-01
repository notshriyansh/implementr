from pathlib import Path

from app.chunking.text_chunker import (
    TextChunker,
)
from app.ingestion.pdf_downloader import (
    PDFDownloader,
)
from app.parsing.pdf_parser import PDFParser
from app.schemas.chunk import DocumentChunk


class IngestionService:
    def __init__(
        self,
        pdf_downloader: PDFDownloader,
    ) -> None:
        self.pdf_downloader = pdf_downloader

        self.pdf_parser = PDFParser()

        self.text_chunker = TextChunker()

    async def ingest_paper(
        self,
        pdf_url: str,
        user_id: str,
        paper_id: str,
    ) -> list[DocumentChunk]:
        saved_path = (
            await self.pdf_downloader.download_pdf(
                pdf_url=pdf_url,
                user_id=user_id,
                paper_id=paper_id,
            )
        )

        parsed_document = (
            await self.pdf_parser.parse(
                file_path=Path(saved_path),
            )
        )

        chunks = await self.text_chunker.chunk(
            document=parsed_document,
            paper_id=paper_id,
            user_id=user_id,
        )

        return chunks