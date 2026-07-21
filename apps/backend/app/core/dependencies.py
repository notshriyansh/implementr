from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.container import Container
from app.db.session import get_db

from app.orchestration.service import JobService

if TYPE_CHECKING:
    from app.agents.autonomous_agent import AutonomousResearchAgent
    from app.agents.implementation_agent import ImplementationAgent
    from app.agents.research_graph import ResearchGraph
    from app.architecture.architecture_reasoning_service import (
        ArchitectureReasoningService,
    )
    from app.architecture.context_expander import ContextExpander
    from app.architecture.execution_flow_service import ExecutionFlowService
    from app.architecture.repository_graph import RepositoryGraph
    from app.blueprints.implementation_blueprint_service import (
        ImplementationBlueprintService,
    )
    from app.code_embeddings.code_embedding_model import CodeEmbeddingModel
    from app.code_ingestion.code_chunker import CodeChunker
    from app.code_ingestion.ingestion_service import CodeIngestionService
    from app.code_ingestion.repository_analyzer import RepositoryAnalyzer
    from app.code_ingestion.repository_scanner import RepositoryScanner
    from app.chat.rag_chat_service import RAGChatService
    from app.agents.hybrid_implementation_agent import (
        HybridImplementationAgent,
    )
    from app.code_ingestion.symbol_extractor import SymbolExtractor
    from app.code_retrieval.code_retrieval_service import CodeRetrievalService
    from app.code_retrieval.symbol_retrieval_service import SymbolRetrievalService
    from app.code_vectorstores.code_vector_store import CodeVectorStore
    from app.concepts.concept_index import ConceptIndex
    from app.concepts.concept_service import ConceptService
    from app.evaluation.benchmark_runner import BenchmarkRunner
    from app.evaluation.blueprint_eval import BlueprintEvaluator
    from app.evaluation.rag_eval import RAGEvaluator
    from app.evaluation.retrieval_eval import RetrievalEvaluator
    from app.hybrid.hybrid_retrieval_service import HybridRetrievalService
    from app.ingestion.pdf_downloader import PDFDownloader
    from app.repositories.arxiv_repository import ArxivRepository
    from app.reproduction.gap_analyzer import GapAnalyzer
    from app.reproduction.research_reproduction_service import (
        ResearchReproductionService,
    )
    from app.retrieval.retrieval_service import RetrievalService
    from app.services.ingestion_service import IngestionService
    from app.services.paper_service import PaperService
    from app.storage.local_storage import LocalStorage
    from app.tools.planning_tool import PlanningTool
    from app.tools.retrieval_tool import RetrievalTool
    from app.workspaces.workspace_output_service import WorkspaceOutputService
    from app.workspaces.workspace_service import WorkspaceService


@lru_cache
def get_container() -> Container:
    """Return the lazily constructed application dependency container."""
    return Container()


def get_concept_index() -> ConceptIndex:
    return get_container().concept_index

def get_arxiv_repository() -> ArxivRepository:
    from app.repositories.arxiv_repository import ArxivRepository

    return ArxivRepository()


def get_paper_service() -> PaperService:
    from app.services.paper_service import PaperService

    return PaperService(arxiv_repository=get_arxiv_repository())


def get_local_storage() -> LocalStorage:
    from app.storage.local_storage import LocalStorage

    return LocalStorage()


def get_pdf_downloader() -> PDFDownloader:
    from app.ingestion.pdf_downloader import PDFDownloader

    return PDFDownloader(storage=get_local_storage())


def get_retrieval_service() -> RetrievalService:
    return get_container().retrieval_service


def get_ingestion_service() -> IngestionService:
    from app.services.ingestion_service import IngestionService

    return IngestionService(
        pdf_downloader=get_pdf_downloader(),
        retrieval_service=get_container().retrieval_service,
    )


def get_concept_service() -> ConceptService:
    return get_container().concept_service


def get_gap_analyzer() -> GapAnalyzer:
    return get_container().gap_analyzer


def get_rag_chat_service() -> RAGChatService:
    from app.chat.rag_chat_service import RAGChatService

    return RAGChatService(
        retrieval_service=get_container().retrieval_service,
        llm=get_container().llm,
        memory=get_container().conversation_memory,
    )


def get_implementation_agent() -> ImplementationAgent:
    from app.agents.implementation_agent import ImplementationAgent

    return ImplementationAgent(
        retrieval_service=get_container().retrieval_service,
        llm=get_container().llm,
    )


def get_research_graph() -> ResearchGraph:
    from app.agents.research_graph import ResearchGraph

    return ResearchGraph(
        retrieval_service=get_container().retrieval_service,
        llm=get_container().llm,
    )


def get_retrieval_tool() -> RetrievalTool:
    from app.tools.retrieval_tool import RetrievalTool

    return RetrievalTool(retrieval_service=get_container().retrieval_service)


def get_planning_tool() -> PlanningTool:
    from app.tools.planning_tool import PlanningTool

    return PlanningTool(llm=get_container().llm)


def get_autonomous_agent() -> AutonomousResearchAgent:
    from app.agents.autonomous_agent import AutonomousResearchAgent

    return AutonomousResearchAgent(
        llm=get_container().llm,
        retrieval_tool=get_retrieval_tool(),
        planning_tool=get_planning_tool(),
    )


def get_retrieval_evaluator() -> RetrievalEvaluator:
    from app.evaluation.retrieval_eval import RetrievalEvaluator

    return RetrievalEvaluator(retrieval_service=get_container().retrieval_service)


def get_rag_evaluator() -> RAGEvaluator:
    from app.evaluation.rag_eval import RAGEvaluator

    return RAGEvaluator(rag_service=get_rag_chat_service())


def get_blueprint_evaluator() -> BlueprintEvaluator:
    from app.evaluation.blueprint_eval import BlueprintEvaluator

    return BlueprintEvaluator(
        blueprint_service=get_container().implementation_blueprint_service
    )


def get_benchmark_runner() -> BenchmarkRunner:
    from app.evaluation.benchmark_runner import BenchmarkRunner

    return BenchmarkRunner(
        retrieval_evaluator=get_retrieval_evaluator(),
        rag_evaluator=get_rag_evaluator(),
    )


def get_repository_graph() -> RepositoryGraph:
    return get_container().repository_graph


def get_repository_scanner() -> RepositoryScanner:
    from app.code_ingestion.repository_scanner import RepositoryScanner

    return RepositoryScanner()


def get_code_chunker() -> CodeChunker:
    from app.code_ingestion.code_chunker import CodeChunker

    return CodeChunker()


def get_code_embedding_model() -> CodeEmbeddingModel:
    return get_container().code_embedding_model


def get_code_vector_store() -> CodeVectorStore:
    return get_container().code_vector_store


def get_code_retrieval_service() -> CodeRetrievalService:
    return get_container().code_retrieval_service


def get_symbol_extractor() -> SymbolExtractor:
    return get_container().symbol_extractor


def get_symbol_retrieval_service() -> SymbolRetrievalService:
    return get_container().symbol_retrieval_service


def get_repository_analyzer() -> RepositoryAnalyzer:
    return get_container().repository_analyzer


def get_execution_flow_service() -> ExecutionFlowService:
    return get_container().execution_flow_service


def get_hybrid_retrieval_service() -> HybridRetrievalService:
    return get_container().hybrid_retrieval_service


def get_hybrid_agent() -> HybridImplementationAgent:
    return get_container().hybrid_agent


def get_code_ingestion_service() -> CodeIngestionService:
    from app.code_ingestion.ingestion_service import CodeIngestionService

    return CodeIngestionService(
        scanner=get_repository_scanner(),
        chunker=get_code_chunker(),
        retrieval_service=get_container().code_retrieval_service,
        symbol_extractor=get_container().symbol_extractor,
        symbol_retrieval_service=get_container().symbol_retrieval_service,
        concept_service=get_container().concept_service,
        concept_index=get_container().concept_index,
        repository_analyzer=get_container().repository_analyzer,
    )


def get_architecture_reasoning_service() -> ArchitectureReasoningService:
    return get_container().architecture_reasoning_service


def get_context_expander() -> ContextExpander:
    return get_container().context_expander


def get_research_reproduction_service() -> ResearchReproductionService:
    return get_container().research_reproduction_service


def get_implementation_blueprint_service() -> ImplementationBlueprintService:
    return get_container().implementation_blueprint_service


def get_workspace_service(
    db: Session = Depends(get_db),
) -> WorkspaceService:
    from app.workspaces.workspace_service import WorkspaceService

    return WorkspaceService(db=db)


def get_workspace_output_service(
    db: Session = Depends(get_db),
) -> WorkspaceOutputService:
    from app.workspaces.workspace_output_service import WorkspaceOutputService

    return WorkspaceOutputService(db=db)

def get_job_service(
    db: Session = Depends(get_db),
) -> JobService:
    return JobService(db)
