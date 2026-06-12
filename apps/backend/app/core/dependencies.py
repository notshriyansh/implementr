from app.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingModel,
)
from app.ingestion.pdf_downloader import PDFDownloader
from app.repositories.arxiv_repository import (
    ArxivRepository,
)
from app.retrieval.retrieval_service import (
    RetrievalService,
)
from app.services.ingestion_service import (
    IngestionService,
)
from app.services.paper_service import (
    PaperService,
)
from app.storage.local_storage import (
    LocalStorage,
)
from app.vectorstores.faiss_store import (
    FAISSVectorStore,
)
from app.chat.rag_chat_service import (
    RAGChatService,
)
from app.llm.groq_client import GroqLLM

from app.memory.conversation_memory import (
    ConversationMemory,
)

embedding_model = (
    SentenceTransformerEmbeddingModel()
)

vector_store = FAISSVectorStore()

llm = GroqLLM()

conversation_memory = (
    ConversationMemory()
)


def get_arxiv_repository() -> ArxivRepository:
    return ArxivRepository()


def get_paper_service() -> PaperService:
    arxiv_repository = (
        get_arxiv_repository()
    )

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


def get_retrieval_service() -> RetrievalService:
    return RetrievalService(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )


def get_ingestion_service() -> IngestionService:
    pdf_downloader = get_pdf_downloader()

    retrieval_service = (
        get_retrieval_service()
    )

    return IngestionService(
        pdf_downloader=pdf_downloader,
        retrieval_service=retrieval_service,
    )

def get_rag_chat_service(
) -> RAGChatService:
    retrieval_service = (
        get_retrieval_service()
    )

    return RAGChatService(
        retrieval_service=retrieval_service,
        llm=llm,
        memory=conversation_memory,
    )