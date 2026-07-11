from app.schemas.reproduction import (
    ResearchReproductionPlan,
)

from app.retrieval.retrieval_service import (
    RetrievalService,
)

from app.code_retrieval.code_retrieval_service import (
    CodeRetrievalService,
)

from app.architecture.architecture_reasoning_service import (
    ArchitectureReasoningService,
)

from app.prompts.reproduction_prompt import (
    REPRODUCTION_PROMPT,
)

from app.llm.base import BaseLLM


class ResearchReproductionService:
    def __init__(
        self,
        retrieval_service: (
            RetrievalService
        ),
        code_retrieval_service: (
            CodeRetrievalService
        ),
        architecture_service: (
            ArchitectureReasoningService
        ),
        llm: BaseLLM,
    ) -> None:

        self.retrieval_service = (
            retrieval_service
        )

        self.code_retrieval_service = (
            code_retrieval_service
        )

        self.architecture_service = (
            architecture_service
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
            "PAPER_SUMMARY:",
            "REPOSITORY_TARGETS:",
            "REQUIRED_CHANGES:",
            "TRAINING_CHANGES:",
            "EVALUATION_CHANGES:",
            "BENCHMARK_TASKS:",
            "SUCCESS_CRITERIA:",
            "RISKS:",
        ]

        end = len(
            remaining
        )

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
            for item in content.split(
                "- "
            )
            if item.strip()
        ]

    async def generate(
        self,
        question: str,
    ) -> ResearchReproductionPlan:

        paper_chunks = (
            await self.retrieval_service.retrieve(
                query=question,
                k=5,
            )
        )

        code_chunks = (
            await self.code_retrieval_service.retrieve(
                query=question,
                k=5,
            )
        )

        architecture = (
            await self.architecture_service.analyze(
                question
            )
        )

        paper_context = (
            "\n\n".join(
                chunk.text
                for chunk in paper_chunks
            )
        )

        repository_context = (
            "\n\n".join(
                (
                    f"{chunk.file_path}\n"
                    f"{chunk.content}"
                )
                for chunk in code_chunks
            )
        )

        architecture_context = (
            architecture.reasoning
        )

        prompt = (
            REPRODUCTION_PROMPT.format(
                question=question,
                paper_context=(
                    paper_context
                ),
                repository_context=(
                    repository_context
                ),
                architecture_context=(
                    architecture_context
                ),
            )
        )

        response = (
            await self.llm.generate(
                prompt
            )
        )

        paper_summary = (
            self.extract_section(
                response,
                "PAPER_SUMMARY",
            )
        )

        repository_targets = (
            self.parse_bullet_section(
                self.extract_section(
                    response,
                    (
                        "REPOSITORY_TARGETS"
                    ),
                )
            )
        )

        required_changes = (
            self.parse_bullet_section(
                self.extract_section(
                    response,
                    (
                        "REQUIRED_CHANGES"
                    ),
                )
            )
        )

        training_changes = (
            self.parse_bullet_section(
                self.extract_section(
                    response,
                    (
                        "TRAINING_CHANGES"
                    ),
                )
            )
        )

        evaluation_changes = (
            self.parse_bullet_section(
                self.extract_section(
                    response,
                    (
                        "EVALUATION_CHANGES"
                    ),
                )
            )
        )

        benchmark_tasks = (
            self.parse_bullet_section(
                self.extract_section(
                    response,
                    (
                        "BENCHMARK_TASKS"
                    ),
                )
            )
        )

        success_criteria = (
            self.parse_bullet_section(
                self.extract_section(
                    response,
                    (
                        "SUCCESS_CRITERIA"
                    ),
                )
            )
        )

        risks = (
            self.parse_bullet_section(
                self.extract_section(
                    response,
                    "RISKS",
                )
            )
        )

        confidence = min(
            1.0,
            (
                len(
                    repository_targets
                )
                + len(
                    required_changes
                )
            )
            / 10,
        )

        return (
            ResearchReproductionPlan(
                paper_summary=(
                    paper_summary
                ),
                repository_targets=(
                    repository_targets
                ),
                required_changes=(
                    required_changes
                ),
                training_changes=(
                    training_changes
                ),
                evaluation_changes=(
                    evaluation_changes
                ),
                benchmark_tasks=(
                    benchmark_tasks
                ),
                success_criteria=(
                    success_criteria
                ),
                risks=risks,
                confidence=confidence,
            )
        )