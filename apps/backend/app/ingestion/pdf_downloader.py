import httpx

from app.storage.base import BaseStorage

class PDFDownloader:
    def __init__(
            self,
            storage: BaseStorage,
    ) -> None:
        self.storage = storage

    async def download_pdf(
            self,
            pdf_url: str,
            user_id: str,
            paper_id: str,
    ) -> str:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=60.0,
        ) as client:
            response = await client.get(pdf_url)

        response.raise_for_status()

        filename = f"{paper_id}.pdf"

        saved_path = await self.storage.save_file(
            content=response.content,
            user_id=user_id,
            filename=filename,
        )

        return str(saved_path)