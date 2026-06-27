from app.hybrid.hybrid_retrieval_service import (
    HybridRetrievalService,
)

from app.llm.base import BaseLLM

from app.prompts.hybrid_prompts import (
    HYBRID_IMPLEMENTATION_PROMPT,
)

from app.schemas.hybrid import (
    HybridAnalysisResponse,
)

from app.concepts.concept_service import (
    ConceptService,
)


class HybridImplementationAgent:
    def __init__(
        self,
        retrieval_service: (
            HybridRetrievalService
        ),
        concept_service: (
            ConceptService
        ),
        llm: BaseLLM,
    ) -> None:
        self.retrieval_service = (
            retrieval_service
        )

        self.llm = llm

        self.concept_service = (
            concept_service
        )

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
            "RELEVANT_FILES:",
            "RELEVANT_SYMBOLS:",
            "IMPLEMENTATION_STEPS:",
            "RISKS:",
            "DETAILED_REASONING:",
        ]

        end = len(remaining)

        for next_section in next_sections:
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

    def parse_bullets(
        self,
        text: str,
    ) -> list[str]:
        return [
            item.strip()
            for item in text.split("- ")
            if item.strip()
        ]

    async def analyze(
        self,
        question: str,
    ) -> HybridAnalysisResponse:

        (
            paper_chunks,
            code_chunks,
        ) = await (
            self.retrieval_service.retrieve(
                query=question,
            )
        )

        paper_context = "\n\n".join(
            chunk.text
            for chunk in paper_chunks
        )

        code_context = "\n\n".join(
            (
                f"FILE: {chunk.file_path}\n"
                f"{chunk.content}"
            )
            for chunk in code_chunks
        )

        concept_map = (
            self.concept_service
            .build_concept_map(
                paper_text=paper_context,
                code_text=code_context,
            )
        )

        concept_context = "\n".join(
            (
                f"{item['paper_concept']} "
                f"-> "
                f"{item['repository_concept']}"
            )
            for item in concept_map
        )

        if not concept_context:
            concept_context = (
                "No direct concept mappings found."
            )

        prompt = (
            HYBRID_IMPLEMENTATION_PROMPT.format(
                question=question,
                paper_context=(
                    paper_context
                ),
                concept_mappings=(
                    concept_context
                ),
                code_context=(
                    code_context
                ),
            )
        )

        reasoning = await (
            self.llm.generate(
                prompt
            )
        )

        summary = (
            self.extract_section(
                reasoning,
                "SUMMARY",
            )
        )

        relevant_files = (
            self.parse_bullets(
                self.extract_section(
                    reasoning,
                    "RELEVANT_FILES",
                )
            )
        )

        relevant_symbols = (
            self.parse_bullets(
                self.extract_section(
                    reasoning,
                    "RELEVANT_SYMBOLS",
                )
            )
        )

        implementation_steps = (
            self.parse_bullets(
                self.extract_section(
                    reasoning,
                    (
                        "IMPLEMENTATION_STEPS"
                    ),
                )
            )
        )

        risks = (
            self.parse_bullets(
                self.extract_section(
                    reasoning,
                    "RISKS",
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

        return (
            HybridAnalysisResponse(
                summary=summary,
                relevant_files=(
                    relevant_files
                ),
                relevant_symbols=(
                    relevant_symbols
                ),
                implementation_steps=(
                    implementation_steps
                ),
                risks=risks,
                confidence=confidence,
                reasoning=(
                    detailed_reasoning
                ),
            )
        )