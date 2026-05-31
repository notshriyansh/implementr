from app.ingestion.pdf_downloader import PDFDownloader


class IngestionService:
    def __init__(
        self,
        pdf_downloader: PDFDownloader,
    ) -> None:
        self.pdf_downloader = pdf_downloader

    async def ingest_paper(
        self,
        pdf_url: str,
        user_id: str,
        paper_id: str,
    ) -> str:
        saved_path = await self.pdf_downloader.download_pdf(
            pdf_url=pdf_url,
            user_id=user_id,
            paper_id=paper_id,
        )

        return saved_path