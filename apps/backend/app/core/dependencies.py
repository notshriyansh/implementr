from app.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingModel,
)

from app.ingestion.pdf_downloader import (
    PDFDownloader,
)

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

from app.llm.groq_client import (
    GroqLLM,
)

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

from app.agents.hybrid_implementation_agent import (
    HybridImplementationAgent,
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

from app.code_ingestion.repository_analyzer import (
    RepositoryAnalyzer,
)

from app.code_ingestion.symbol_extractor import (
    SymbolExtractor,
)

from app.code_embeddings.code_embedding_model import (
    CodeEmbeddingModel,
)

from app.code_retrieval.code_retrieval_service import (
    CodeRetrievalService,
)

from app.code_retrieval.symbol_retrieval_service import (
    SymbolRetrievalService,
)

from app.code_vectorstores.code_vector_store import (
    CodeVectorStore,
)

from app.code_vectorstores.symbol_vector_store import (
    SymbolVectorStore,
)

from app.hybrid.hybrid_retrieval_service import (
    HybridRetrievalService,
)

from app.architecture.repository_graph import (
    RepositoryGraph,
)

from app.architecture.execution_flow_service import (
    ExecutionFlowService,
)

from app.architecture.architecture_reasoning_service import (
    ArchitectureReasoningService,
)

from app.architecture.context_expander import (
    ContextExpander,
)

from app.concepts.concept_extractor import (
    ConceptExtractor,
)

from app.concepts.concept_matcher import (
    ConceptMatcher,
)

from app.concepts.concept_service import (
    ConceptService,
)

from app.concepts.concept_index import (
    ConceptIndex,
)

from app.reproduction.research_reproduction_service import (
    ResearchReproductionService,
)

from app.reproduction.gap_analyzer import (
    GapAnalyzer,
)

from app.blueprints.implementation_blueprint_service import (
    ImplementationBlueprintService,
)

from app.cache.memory_cache import (
    MemoryCache,
)

embedding_model = (
    SentenceTransformerEmbeddingModel()
)

vector_store = (
    FAISSVectorStore()
)

llm = (
    GroqLLM()
)

memory_cache = (
    MemoryCache()
)

conversation_memory = (
    ConversationMemory()
)

retrieval_service = (
    RetrievalService(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )
)

code_embedding_model = (
    CodeEmbeddingModel()
)

code_vector_store = (
    CodeVectorStore()
)

code_retrieval_service = (
    CodeRetrievalService(
        embedding_model=code_embedding_model,
        vector_store=code_vector_store,
    )
)

symbol_vector_store = (
    SymbolVectorStore()
)

symbol_extractor = (
    SymbolExtractor()
)

symbol_retrieval_service = (
    SymbolRetrievalService(
        embedding_model=code_embedding_model,
        vector_store=symbol_vector_store,
    )
)

repository_graph = (
    RepositoryGraph()
)

context_expander = (
    ContextExpander(
        graph=repository_graph,
    )
)

repository_analyzer = (
    RepositoryAnalyzer(
        graph=repository_graph,
        scanner=RepositoryScanner(),
    )
)

execution_flow_service = (
    ExecutionFlowService(
        graph=repository_graph,
        symbol_service=(
            symbol_retrieval_service
        ),
    )
)

hybrid_retrieval_service = (
    HybridRetrievalService(
        paper_retrieval=retrieval_service,
        code_retrieval=code_retrieval_service,
    )
)

architecture_reasoning_service = (
    ArchitectureReasoningService(
        code_retrieval_service=(
            code_retrieval_service
        ),
        symbol_retrieval_service=(
            symbol_retrieval_service
        ),
        execution_flow_service=(
            execution_flow_service
        ),
        context_expander=(
            context_expander
        ),
        llm=llm,
        cache=memory_cache,
    )
)


concept_extractor = (
    ConceptExtractor()
)

concept_matcher = (
    ConceptMatcher()
)

concept_service = (
    ConceptService(
        extractor=(
            concept_extractor
        ),
        matcher=(
            concept_matcher
        ),
    )
)

concept_index = (
    ConceptIndex()
)


gap_analyzer = (
    GapAnalyzer()
)

research_reproduction_service = (
    ResearchReproductionService(
        retrieval_service=(
            retrieval_service
        ),
        code_retrieval_service=(
            code_retrieval_service
        ),
        symbol_retrieval_service=(
            symbol_retrieval_service
        ),
        architecture_service=(
            architecture_reasoning_service
        ),
        concept_service=(
            concept_service
        ),
        gap_analyzer=(
            gap_analyzer
        ),
        llm=llm,
        cache=memory_cache,
    )
)

implementation_blueprint_service = (
    ImplementationBlueprintService(
        reproduction_service=(
            research_reproduction_service
        ),
        symbol_retrieval_service=(
            symbol_retrieval_service
        ),
        llm=llm,
    )
)

hybrid_agent = (
    HybridImplementationAgent(
        retrieval_service=(
            hybrid_retrieval_service
        ),
        concept_service=(
            concept_service
        ),
        llm=llm,
    )
)

def get_arxiv_repository(
) -> ArxivRepository:
    return ArxivRepository()


def get_paper_service(
) -> PaperService:
    return PaperService(
        arxiv_repository=(
            get_arxiv_repository()
        ),
    )


def get_local_storage(
) -> LocalStorage:
    return LocalStorage()


def get_pdf_downloader(
) -> PDFDownloader:
    return PDFDownloader(
        storage=(
            get_local_storage()
        ),
    )


def get_retrieval_service(
) -> RetrievalService:
    return retrieval_service


def get_ingestion_service(
) -> IngestionService:
    return IngestionService(
        pdf_downloader=(
            get_pdf_downloader()
        ),
        retrieval_service=(
            retrieval_service
        ),
    )


def get_concept_service(
) -> ConceptService:
    return concept_service

def get_gap_analyzer(
):
    return gap_analyzer


def get_rag_chat_service(
) -> RAGChatService:
    return RAGChatService(
        retrieval_service=(
            retrieval_service
        ),
        llm=llm,
        memory=conversation_memory,
    )


def get_implementation_agent(
) -> ImplementationAgent:
    return ImplementationAgent(
        retrieval_service=(
            retrieval_service
        ),
        llm=llm,
    )


def get_research_graph(
) -> ResearchGraph:
    return ResearchGraph(
        retrieval_service=(
            retrieval_service
        ),
        llm=llm,
    )


def get_retrieval_tool(
) -> RetrievalTool:
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
    return RetrievalEvaluator(
        retrieval_service
    )


def get_rag_evaluator(
) -> RAGEvaluator:
    return RAGEvaluator(
        get_rag_chat_service()
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


def get_repository_graph(
) -> RepositoryGraph:
    return repository_graph

def get_repository_scanner(
) -> RepositoryScanner:
    return RepositoryScanner()


def get_code_chunker(
) -> CodeChunker:
    return CodeChunker()


def get_code_embedding_model(
) -> CodeEmbeddingModel:
    return code_embedding_model


def get_code_vector_store(
) -> CodeVectorStore:
    return code_vector_store


def get_code_retrieval_service(
) -> CodeRetrievalService:
    return code_retrieval_service


def get_symbol_extractor(
) -> SymbolExtractor:
    return symbol_extractor


def get_symbol_retrieval_service(
) -> SymbolRetrievalService:
    return symbol_retrieval_service


def get_repository_analyzer(
) -> RepositoryAnalyzer:
    return repository_analyzer


def get_execution_flow_service(
) -> ExecutionFlowService:
    return execution_flow_service


def get_hybrid_retrieval_service(
) -> HybridRetrievalService:
    return hybrid_retrieval_service


def get_hybrid_agent(
) -> HybridImplementationAgent:
    return hybrid_agent


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
            code_retrieval_service
        ),
        symbol_extractor=(
            symbol_extractor
        ),
        symbol_retrieval_service=(
            symbol_retrieval_service
        ),
        concept_service=(
            concept_service
        ),
        concept_index=(
            concept_index
        ),
        repository_analyzer=(
            repository_analyzer
        ),
    )


def get_architecture_reasoning_service(
) -> ArchitectureReasoningService:
    return architecture_reasoning_service

def get_context_expander(
) -> ContextExpander:
    return context_expander

def get_research_reproduction_service(
) -> ResearchReproductionService:
    return (
        research_reproduction_service
    )

def get_implementation_blueprint_service():
    return implementation_blueprint_service