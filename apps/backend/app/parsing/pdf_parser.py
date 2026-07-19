from pathlib import Path

import fitz  # type: ignore[import-untyped]

from app.parsing.base import BaseParser
from app.schemas.document import (
    DocumentPage,
    ParsedDocument,
)


class PDFParser(BaseParser):
    async def parse(
        self,
        file_path: Path,
    ) -> ParsedDocument:
        pdf_document = fitz.open(file_path)

        pages: list[DocumentPage] = []

        for page_index in range(
            len(pdf_document)
        ):
            page = pdf_document.load_page(
                page_index
            )

            text = page.get_text()

            pages.append(
                DocumentPage(
                    page_number=page_index + 1,
                    text=text,
                )
            )

        return ParsedDocument(
            pages=pages,
            total_pages=len(pages),
        )