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

from app.observability.tracing import (
    trace_execution,
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

    def extract_section(
        self,
        text: str,
        section: str,
    ) -> str:
        marker = f"{section}:"
        if marker not in text:
            return ""

        start = (
            text.index(marker)
            + len(marker)
        )

        remaining = text[start:]

        next_sections = [
            "SUMMARY:",
            "EXECUTION_STEPS:",
            "ENGINEERING_NOTES:",
            "MODIFICATION_POINTS:",
            "DETAILED_REASONING:",
        ]

        end = len(remaining)

        for next_section in (
            next_sections
        ):
            idx = remaining.find(
                next_section
            )

            if (
                idx != -1
                and idx < end
            ):
                end = idx

        return (
            remaining[:end]
            .strip()
        )

    def parse_bullet_section(
        self,
        content: str,
    ) -> list[str]:
        if not content:
            return []

        return [
            item.strip()
            for item in content.split("- ")
            if item.strip()
        ]

    @trace_execution(
        "architecture_analysis"
    )
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
                f"FILE: "
                f"{chunk.file_path}\n\n"
                f"{chunk.content}"
            )
            for chunk in code_chunks
        )

        flow_text = "\n".join(
            (
                f"SYMBOL: "
                f"{item['symbol']}\n"
                f"FILE: "
                f"{item['file']}\n"
                f"IMPORTS: "
                f"{', '.join(item['imports'])}"
            )
            for item in (
                flow_context[
                    "symbols"
                ]
            )
        )

        prompt = (
            ARCHITECTURE_REASONING_PROMPT
            .format(
                query=query,
                files_context=files_context,
                symbols_context=symbols_context,
                flow_context=flow_text,
                code_context=code_context,
            )
        )

        try:
            reasoning = await (
                self.llm.generate(
                    prompt
                )
            )

        except Exception:
            reasoning = (
                "LLM generation failed."
            )

        summary = (
            self.extract_section(
                reasoning,
                "SUMMARY",
            )
        )

        execution_steps = (
            self.parse_bullet_section(
                self.extract_section(
                    reasoning,
                    (
                        "EXECUTION_STEPS"
                    ),
                )
            )
        )

        engineering_notes = (
            self.parse_bullet_section(
                self.extract_section(
                    reasoning,
                    (
                        "ENGINEERING_NOTES"
                    ),
                )
            )
        )

        modification_points = (
            self.parse_bullet_section(
                self.extract_section(
                    reasoning,
                    (
                        "MODIFICATION_POINTS"
                    ),
                )
            )
        )

        detailed_reasoning = (
            self.extract_section(
                reasoning,
                (
                    "DETAILED_REASONING"
                ),
            )
        )

        confidence = min(
            1.0,
            (
                len(relevant_files)
                + len(
                    relevant_symbols
                )
            )
            / 10,
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
            execution_steps=(
                execution_steps
            ),
            engineering_notes=(
                engineering_notes
            ),
            modification_points=(
                modification_points
            ),
            confidence=confidence,
            reasoning=(
                detailed_reasoning
            ),
        )
