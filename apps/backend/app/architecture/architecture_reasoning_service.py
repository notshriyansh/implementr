from app.schemas.architecture import (
    ArchitectureInsight,
)

from app.code_retrieval.code_retrieval_service import (
    CodeRetrievalService,
)

from app.code_retrieval.symbol_retrieval_service import (
    SymbolRetrievalService,
)

from app.architecture.execution_flow_service import (
    ExecutionFlowService,
)

from app.llm.base import BaseLLM


class ArchitectureReasoningService:
    def __init__(
        self,
        code_retrieval_service: (
            CodeRetrievalService
        ),
        symbol_retrieval_service: (
            SymbolRetrievalService
        ),
        execution_flow_service: (
            ExecutionFlowService
        ),
        llm: BaseLLM,
    ) -> None:
        self.code_retrieval_service = (
            code_retrieval_service
        )

        self.symbol_retrieval_service = (
            symbol_retrieval_service
        )

        self.execution_flow_service = (
            execution_flow_service
        )

        self.llm = llm

    async def analyze(
        self,
        query: str,
    ) -> ArchitectureInsight:
        code_chunks = await (
            self.code_retrieval_service
            .retrieve(
                query=query,
                k=5,
            )
        )

        symbols = await (
            self.symbol_retrieval_service
            .retrieve(
                query=query,
                k=5,
            )
        )

        code_context = "\n\n".join(
            chunk.content
            for chunk in code_chunks
        )

        symbol_context = "\n\n".join(
            (
                f"{symbol.symbol_name}"
                f" ({symbol.symbol_type})\n"
                f"{symbol.code}"
            )
            for symbol in symbols
        )

        flow_context = await (
            self.execution_flow_service
            .expand_query(query)
        )

        prompt = f"""
You are an expert software architect.

Analyze the repository context below.

User Question:
{query}

Code Context:
{code_context}

Symbol Context:
{symbol_context}

Execution Flow Context:
{flow_context}

Your task:
1. Explain the architecture relevant to the query
2. Explain execution flow
3. Identify important files
4. Identify important symbols/functions/classes
5. Explain engineering reasoning carefully
6. Suggest where modifications should happen if relevant

Return a detailed engineering explanation.
"""

        reasoning = await (
            self.llm.generate(prompt)
        )

        return ArchitectureInsight(
            query=query,
            summary=(
                reasoning[:300]
            ),
            relevant_files=[
                chunk.file_path
                for chunk in code_chunks
            ],
            relevant_symbols=[
                symbol.symbol_name
                for symbol in symbols
            ],
            reasoning=reasoning,
        )