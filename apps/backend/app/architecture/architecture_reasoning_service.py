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

from app.prompts.architecture_prompt import (
    ARCHITECTURE_REASONING_PROMPT,
)


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

        flow_context = await (
            self.execution_flow_service
            .expand_query(query)
        )

        relevant_files = list(
            dict.fromkeys(
                chunk.file_path
                for chunk in code_chunks
            )
        )

        relevant_symbols = list(
            dict.fromkeys(
                symbol.symbol_name
                for symbol in symbols
            )
        )

        files_context = "\n".join(
            relevant_files
        )

        symbols_context = "\n".join(
            (
                f"{symbol.symbol_name} "
                f"({symbol.symbol_type}) "
                f"in {symbol.file_path}"
            )
            for symbol in symbols
        )

        code_context = "\n\n".join(
            (
                f"FILE: {chunk.file_path}\n"
                f"{chunk.content}"
            )
            for chunk in code_chunks
        )

        prompt = (
            ARCHITECTURE_REASONING_PROMPT
            .format(
                query=query,
                files=files_context,
                symbols=symbols_context,
                flow=flow_context,
                code=code_context,
            )
        )

        reasoning = await (
            self.llm.generate(prompt)
        )

        summary = (
            reasoning[:400] + "..."
            if len(reasoning) > 400
            else reasoning
        )

        return ArchitectureInsight(
            query=query,
            summary=summary,
            relevant_files=(
                relevant_files
            ),
            relevant_symbols=(
                relevant_symbols
            ),
            reasoning=reasoning,
        )