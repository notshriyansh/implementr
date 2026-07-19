"""Lazy application dependency container.

This module intentionally imports concrete services inside their properties so
importing the FastAPI application does not import or construct heavyweight AI
and vector-store dependencies.
"""

from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.architecture.architecture_reasoning_service import (
        ArchitectureReasoningService,
    )
    from app.architecture.context_expander import ContextExpander
    from app.architecture.execution_flow_service import ExecutionFlowService
    from app.architecture.repository_graph import RepositoryGraph
    from app.agents.hybrid_implementation_agent import HybridImplementationAgent
    from app.blueprints.implementation_blueprint_service import (
        ImplementationBlueprintService,
    )
    from app.cache.memory_cache import MemoryCache
    from app.code_embeddings.code_embedding_model import CodeEmbeddingModel
    from app.code_ingestion.repository_analyzer import RepositoryAnalyzer
    from app.code_ingestion.symbol_extractor import SymbolExtractor
    from app.code_retrieval.code_retrieval_service import CodeRetrievalService
    from app.code_retrieval.symbol_retrieval_service import SymbolRetrievalService
    from app.code_vectorstores.code_vector_store import CodeVectorStore
    from app.code_vectorstores.symbol_vector_store import SymbolVectorStore
    from app.concepts.concept_extractor import ConceptExtractor
    from app.concepts.concept_index import ConceptIndex
    from app.concepts.concept_matcher import ConceptMatcher
    from app.concepts.concept_service import ConceptService
    from app.embeddings.sentence_transformer import SentenceTransformerEmbeddingModel
    from app.hybrid.hybrid_retrieval_service import HybridRetrievalService
    from app.llm.groq_client import GroqLLM
    from app.memory.conversation_memory import ConversationMemory
    from app.reproduction.gap_analyzer import GapAnalyzer
    from app.reproduction.research_reproduction_service import (
        ResearchReproductionService,
    )
    from app.retrieval.retrieval_service import RetrievalService
    from app.vectorstores.faiss_store import FAISSVectorStore


class Container:

    @cached_property
    def embedding_model(self) -> "SentenceTransformerEmbeddingModel":
        from app.embeddings.sentence_transformer import SentenceTransformerEmbeddingModel

        return SentenceTransformerEmbeddingModel()

    @cached_property
    def vector_store(self) -> "FAISSVectorStore":
        from app.vectorstores.faiss_store import FAISSVectorStore

        return FAISSVectorStore()

    @cached_property
    def llm(self) -> "GroqLLM":
        from app.llm.groq_client import GroqLLM

        return GroqLLM()

    @cached_property
    def memory_cache(self) -> "MemoryCache":
        from app.cache.memory_cache import MemoryCache

        return MemoryCache()

    @cached_property
    def conversation_memory(self) -> "ConversationMemory":
        from app.memory.conversation_memory import ConversationMemory

        return ConversationMemory()

    @cached_property
    def retrieval_service(self) -> "RetrievalService":
        from app.retrieval.retrieval_service import RetrievalService

        return RetrievalService(
            embedding_model=self.embedding_model,
            vector_store=self.vector_store,
        )

    @cached_property
    def code_embedding_model(self) -> "CodeEmbeddingModel":
        from app.code_embeddings.code_embedding_model import CodeEmbeddingModel

        return CodeEmbeddingModel()

    @cached_property
    def code_vector_store(self) -> "CodeVectorStore":
        from app.code_vectorstores.code_vector_store import CodeVectorStore

        return CodeVectorStore()

    @cached_property
    def code_retrieval_service(self) -> "CodeRetrievalService":
        from app.code_retrieval.code_retrieval_service import CodeRetrievalService

        return CodeRetrievalService(
            embedding_model=self.code_embedding_model,
            vector_store=self.code_vector_store,
        )

    @cached_property
    def symbol_vector_store(self) -> "SymbolVectorStore":
        from app.code_vectorstores.symbol_vector_store import SymbolVectorStore

        return SymbolVectorStore()

    @cached_property
    def symbol_extractor(self) -> "SymbolExtractor":
        from app.code_ingestion.symbol_extractor import SymbolExtractor

        return SymbolExtractor()

    @cached_property
    def symbol_retrieval_service(self) -> "SymbolRetrievalService":
        from app.code_retrieval.symbol_retrieval_service import SymbolRetrievalService

        return SymbolRetrievalService(
            embedding_model=self.code_embedding_model,
            vector_store=self.symbol_vector_store,
        )

    @cached_property
    def repository_graph(self) -> "RepositoryGraph":
        from app.architecture.repository_graph import RepositoryGraph

        return RepositoryGraph()

    @cached_property
    def context_expander(self) -> "ContextExpander":
        from app.architecture.context_expander import ContextExpander

        return ContextExpander(graph=self.repository_graph)

    @cached_property
    def repository_analyzer(self) -> "RepositoryAnalyzer":
        from app.code_ingestion.repository_analyzer import RepositoryAnalyzer
        from app.code_ingestion.repository_scanner import RepositoryScanner

        return RepositoryAnalyzer(
            graph=self.repository_graph,
            scanner=RepositoryScanner(),
        )

    @cached_property
    def execution_flow_service(self) -> "ExecutionFlowService":
        from app.architecture.execution_flow_service import ExecutionFlowService

        return ExecutionFlowService(
            graph=self.repository_graph,
            symbol_service=self.symbol_retrieval_service,
        )

    @cached_property
    def hybrid_retrieval_service(self) -> "HybridRetrievalService":
        from app.hybrid.hybrid_retrieval_service import HybridRetrievalService

        return HybridRetrievalService(
            paper_retrieval=self.retrieval_service,
            code_retrieval=self.code_retrieval_service,
        )

    @cached_property
    def architecture_reasoning_service(self) -> "ArchitectureReasoningService":
        from app.architecture.architecture_reasoning_service import (
            ArchitectureReasoningService,
        )

        return ArchitectureReasoningService(
            code_retrieval_service=self.code_retrieval_service,
            symbol_retrieval_service=self.symbol_retrieval_service,
            execution_flow_service=self.execution_flow_service,
            context_expander=self.context_expander,
            llm=self.llm,
            cache=self.memory_cache,
        )

    @cached_property
    def concept_extractor(self) -> "ConceptExtractor":
        from app.concepts.concept_extractor import ConceptExtractor

        return ConceptExtractor()

    @cached_property
    def concept_matcher(self) -> "ConceptMatcher":
        from app.concepts.concept_matcher import ConceptMatcher

        return ConceptMatcher()

    @cached_property
    def concept_service(self) -> "ConceptService":
        from app.concepts.concept_service import ConceptService

        return ConceptService(
            extractor=self.concept_extractor,
            matcher=self.concept_matcher,
        )

    @cached_property
    def concept_index(self) -> "ConceptIndex":
        from app.concepts.concept_index import ConceptIndex

        return ConceptIndex()

    @cached_property
    def gap_analyzer(self) -> "GapAnalyzer":
        from app.reproduction.gap_analyzer import GapAnalyzer

        return GapAnalyzer()

    @cached_property
    def research_reproduction_service(self) -> "ResearchReproductionService":
        from app.reproduction.research_reproduction_service import (
            ResearchReproductionService,
        )

        return ResearchReproductionService(
            retrieval_service=self.retrieval_service,
            code_retrieval_service=self.code_retrieval_service,
            symbol_retrieval_service=self.symbol_retrieval_service,
            architecture_service=self.architecture_reasoning_service,
            concept_service=self.concept_service,
            gap_analyzer=self.gap_analyzer,
            llm=self.llm,
            cache=self.memory_cache,
        )

    @cached_property
    def implementation_blueprint_service(self) -> "ImplementationBlueprintService":
        from app.blueprints.implementation_blueprint_service import (
            ImplementationBlueprintService,
        )

        return ImplementationBlueprintService(
            reproduction_service=self.research_reproduction_service,
            symbol_retrieval_service=self.symbol_retrieval_service,
            llm=self.llm,
        )

    @cached_property
    def hybrid_agent(self) -> "HybridImplementationAgent":
        from app.agents.hybrid_implementation_agent import HybridImplementationAgent

        return HybridImplementationAgent(
            retrieval_service=self.hybrid_retrieval_service,
            symbol_retrieval_service=self.symbol_retrieval_service,
            concept_service=self.concept_service,
            llm=self.llm,
        )
