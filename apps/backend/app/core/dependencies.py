from app.repositories.arxiv_repository import ArxivRepository
from app.services.paper_service import PaperService
from app.ingestion.pdf_downloader import PDFDownloader
from app.services.ingestion_service import IngestionService
from app.storage.local_storage import LocalStorage

def get_arxiv_repository() -> ArxivRepository:
    return ArxivRepository()

def get_paper_service() -> PaperService:
    arxiv_repository = get_arxiv_repository()

    return PaperService(
        arxiv_repository=arxiv_repository,
    )

def get_local_storage() -> LocalStorage:
    return LocalStorage()


def get_pdf_downloader() -> PDFDownloader:
    storage = get_local_storage()

    return PDFDownloader(
        storage=storage,
    )


def get_ingestion_service() -> IngestionService:
    pdf_downloader = get_pdf_downloader()

    return IngestionService(
        pdf_downloader=pdf_downloader,
    )