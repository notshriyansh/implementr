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

from app.concepts.concept_service import (
    ConceptService,
)


from app.reproduction.gap_analyzer import (
    GapAnalyzer,
)

from app.code_retrieval.symbol_retrieval_service import (
    SymbolRetrievalService,
)

from app.llm.base import BaseLLM


class ResearchReproductionService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        code_retrieval_service: CodeRetrievalService,
        symbol_retrieval_service: SymbolRetrievalService,
        architecture_service: ArchitectureReasoningService,
        concept_service: ConceptService,
        gap_analyzer: GapAnalyzer,
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

        self.symbol_retrieval_service = (
            symbol_retrieval_service
        )

        self.concept_service = (
            concept_service
        )

        self.gap_analyzer = (
            gap_analyzer
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
            "PAPER_SUMMARY:",
            "REPOSITORY_TARGETS:",
            "CONCEPT_MAPPINGS:",
            "ARCHITECTURE_GAPS:",
            "IMPLEMENTATION_STEPS:",
            "MODIFICATION_TARGETS:",
            "GAP_TO_SYMBOL_MAPPING:",
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

        if not paper_chunks:
            return ResearchReproductionPlan(
                paper_summary=(
                    "No paper context available."
                ),
                repository_targets=[],
                required_changes=[],
                training_changes=[],
                evaluation_changes=[],
                benchmark_tasks=[],
                success_criteria=[],
                risks=[
                    "Paper must be ingested first."
                ],
                confidence=0.0,
            )
        
        paper_context = "\n\n".join(
            chunk.text
            for chunk in paper_chunks
        ).strip()

        if not paper_context:
            return ResearchReproductionPlan(
                paper_summary=(
                    "No paper context available."
                ),
                repository_targets=[],
                required_changes=[],
                training_changes=[],
                evaluation_changes=[],
                benchmark_tasks=[],
                success_criteria=[],
                risks=[
                    "Paper must be ingested first."
                ],
                confidence=0.0,
            )

        code_chunks = (
            await self.code_retrieval_service.retrieve(
                query=question,
                k=5,
            )
        )

        symbols = await (
            self.symbol_retrieval_service.retrieve(
                query=question,
                k=25,
            )
        )

        architecture = (
            await self.architecture_service.analyze(
                question
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

        symbols_context = "\n".join(
            (
                f"{symbol.symbol_name} "
                f"({symbol.symbol_type}) "
                f"in {symbol.file_path}"
            )
            for symbol in symbols
        )

        concept_map = (
            self.concept_service
            .build_concept_map(
                paper_text=paper_context,
                symbols=symbols,
            )
        )

        paper_concepts = [
            concept.name
            for concept in (
                concept_map[
                    "paper_concepts"
                ]
            )
        ]

        repo_concepts = [
            concept.name
            for concept in (
                concept_map[
                    "repository_concepts"
                ]
            )
        ]

        semantic_matches = (
            concept_map["matches"]
        )

        concept_mappings = [
            (
                f"{match.paper_concept}"
                f" -> "
                f"{match.repository_concept}"
                f" ({match.similarity})"
            )
            for match in semantic_matches
        ]

        architecture_gaps = (
            self.gap_analyzer.analyze(
                paper_concepts,
                repo_concepts,
            )
        )

        prompt = (
            REPRODUCTION_PROMPT.format(
                question=question,
                paper_context=paper_context,
                repository_context=repository_context,
                architecture_context=architecture_context,
                symbols_context=symbols_context,
                paper_concepts="\n".join(
                    f"- {concept}"
                    for concept in paper_concepts
                ),
                repo_concepts="\n".join(
                    f"- {concept}"
                    for concept in repo_concepts
                ),
                concept_mappings="\n".join(
                    f"- {mapping}"
                    for mapping in concept_mappings
                ),
                architecture_gaps="\n".join(
                    f"- {gap}"
                    for gap in architecture_gaps
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

        concept_mappings = (
            self.parse_bullet_section(
                self.extract_section(
                    response,
                    "CONCEPT_MAPPINGS",
                )
            )
        )

        implementation_steps = (
            self.parse_bullet_section(
                self.extract_section(
                    response,
                    "IMPLEMENTATION_STEPS",
                )
            )
        )

        modification_targets = (
            self.parse_bullet_section(
                self.extract_section(
                    response,
                    "MODIFICATION_TARGETS",
                )
            )
        )

        gap_to_symbol_mapping = (
            self.parse_bullet_section(
                self.extract_section(
                    response,
                    "GAP_TO_SYMBOL_MAPPING",
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
                len(repository_targets)
                + len(concept_mappings)
                + len(implementation_steps)
            )
            / 15,
        )

        return (
            ResearchReproductionPlan(
                paper_summary=(
                    paper_summary
                ),
                repository_targets=(
                    repository_targets
                ),
                concept_mappings=(
                    concept_mappings
                ),
                architecture_gaps=(
                    architecture_gaps
                ),
                implementation_steps=(
                    implementation_steps
                ),
                modification_targets=(
                    modification_targets
                ),
                gap_to_symbol_mapping=(
                    gap_to_symbol_mapping
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