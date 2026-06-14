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
from app.code_embeddings.code_embedding_model import (
    CodeEmbeddingModel,
)
from app.code_retrieval.code_retrieval_service import (
    CodeRetrievalService,
)
from app.code_vectorstores.code_vector_store import (
    CodeVectorStore,
)
from app.hybrid.hybrid_retrieval_service import (
    HybridRetrievalService,
)
from app.agents.hybrid_implementation_agent import (
    HybridImplementationAgent,
)
from app.code_ingestion.repository_analyzer import (
    RepositoryAnalyzer,
)
from app.code_ingestion.symbol_extractor import (
    SymbolExtractor,
)
from app.code_retrieval.symbol_retrieval_service import (
    SymbolRetrievalService,
)
from app.code_vectorstores.symbol_vector_store import (
    SymbolVectorStore,
)

embedding_model = (
    SentenceTransformerEmbeddingModel()
)

vector_store = FAISSVectorStore()

llm = GroqLLM()

conversation_memory = (
    ConversationMemory()
)

code_embedding_model = (
    CodeEmbeddingModel()
)

code_vector_store = (
    CodeVectorStore()
)

code_retrieval_service = (
    CodeRetrievalService(
        embedding_model=(
            code_embedding_model
        ),
        vector_store=(
            code_vector_store
        ),
    )
)

repository_analyzer = (
    RepositoryAnalyzer()
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
        retrieval_service=(
            get_code_retrieval_service()
        ),
        symbol_extractor=(
            get_symbol_extractor()
        ),
        symbol_retrieval_service=(
            get_symbol_retrieval_service()
        ),
    )

def get_code_embedding_model(
) -> CodeEmbeddingModel:
    return code_embedding_model


def get_code_vector_store(
) -> CodeVectorStore:
    return code_vector_store

def get_hybrid_retrieval_service(
) -> HybridRetrievalService:
    return hybrid_retrieval_service


def get_hybrid_agent(
) -> HybridImplementationAgent:
    return HybridImplementationAgent(
        retrieval_service=(
            get_hybrid_retrieval_service()
        ),
        llm=llm,
    )


def get_code_retrieval_service(
) -> CodeRetrievalService:
    return code_retrieval_service

hybrid_retrieval_service = (
    HybridRetrievalService(
        paper_retrieval=(
            get_retrieval_service()
        ),
        code_retrieval=(
            get_code_retrieval_service()
        ),
    )
)

symbol_vector_store = (
    SymbolVectorStore()
)

symbol_retrieval_service = (
    SymbolRetrievalService(
        embedding_model=(
            get_code_embedding_model()
        ),
        vector_store=(
            symbol_vector_store
        ),
    )
)

symbol_extractor = (
    SymbolExtractor()
)

def get_repository_analyzer(
) -> RepositoryAnalyzer:
    return repository_analyzer

def get_symbol_extractor(
) -> SymbolExtractor:
    return symbol_extractor


def get_symbol_retrieval_service(
) -> SymbolRetrievalService:
    return (
        symbol_retrieval_service
    )