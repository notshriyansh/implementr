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

from app.agents.implementation_agent import (
    ImplementationAgent,
)

from app.agents.research_graph import (
    ResearchGraph,
)
from app.agents.autonomous_agent import (
    AutonomousResearchAgent,
)
from app.tools.planning_tool import (
    PlanningTool,
)
from app.tools.retrieval_tool import (
    RetrievalTool,
)
from app.evaluation.benchmark_runner import (
    BenchmarkRunner,
)
from app.evaluation.rag_eval import (
    RAGEvaluator,
)
from app.evaluation.retrieval_eval import (
    RetrievalEvaluator,
)
from app.code_ingestion.code_chunker import (
    CodeChunker,
)
from app.code_ingestion.ingestion_service import (
    CodeIngestionService,
)
from app.code_ingestion.repository_scanner import (
    RepositoryScanner,
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

def get_implementation_agent(
) -> ImplementationAgent:
    retrieval_service = (
        get_retrieval_service()
    )

    return ImplementationAgent(
        retrieval_service=retrieval_service,
        llm=llm,
    )

def get_research_graph(
) -> ResearchGraph:
    retrieval_service = (
        get_retrieval_service()
    )

    return ResearchGraph(
        retrieval_service=retrieval_service,
        llm=llm,
    )

def get_retrieval_tool(
) -> RetrievalTool:
    retrieval_service = (
        get_retrieval_service()
    )

    return RetrievalTool(
        retrieval_service
    )


def get_planning_tool(
) -> PlanningTool:
    return PlanningTool(llm)


def get_autonomous_agent(
) -> AutonomousResearchAgent:
    return AutonomousResearchAgent(
        llm=llm,
        retrieval_tool=(
            get_retrieval_tool()
        ),
        planning_tool=(
            get_planning_tool()
        ),
    )

def get_retrieval_evaluator(
) -> RetrievalEvaluator:
    retrieval_service = (
        get_retrieval_service()
    )

    return RetrievalEvaluator(
        retrieval_service
    )


def get_rag_evaluator(
) -> RAGEvaluator:
    rag_service = (
        get_rag_chat_service()
    )

    return RAGEvaluator(
        rag_service
    )


def get_benchmark_runner(
) -> BenchmarkRunner:
    return BenchmarkRunner(
        retrieval_evaluator=(
            get_retrieval_evaluator()
        ),
        rag_evaluator=(
            get_rag_evaluator()
        ),
    )

def get_repository_scanner(
) -> RepositoryScanner:
    return RepositoryScanner()


def get_code_chunker(
) -> CodeChunker:
    return CodeChunker()


def get_code_ingestion_service(
) -> CodeIngestionService:
    return CodeIngestionService(
        scanner=(
            get_repository_scanner()
        ),
        chunker=(
            get_code_chunker()
        ),
    )