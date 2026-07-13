import json

from app.schemas.implementation_blueprint import (
    BlueprintStep,
    ImplementationBlueprint,
)

from app.reproduction.research_reproduction_service import (
    ResearchReproductionService,
)

from app.prompts.blueprint_prompt import (
    BLUEPRINT_PROMPT,
)

from app.llm.base import BaseLLM


class ImplementationBlueprintService:
    def __init__(
        self,
        reproduction_service: (
            ResearchReproductionService
        ),
        llm: BaseLLM,
    ) -> None:

        self.reproduction_service = (
            reproduction_service
        )

        self.llm = llm

    async def generate(
        self,
        question: str,
    ) -> ImplementationBlueprint:

        plan = await (
            self.reproduction_service.generate(
                question
            )
        )

        if not plan.modification_targets:

            return (
                ImplementationBlueprint(
                    paper_summary=(
                        plan.paper_summary
                    ),
                    blueprint_steps=[],
                    risks=(
                        plan.risks
                    ),
                    confidence=0.0,
                )
            )

        prompt = (
            BLUEPRINT_PROMPT.format(
                question=question,
                paper_summary=(
                    plan.paper_summary
                ),
                modification_targets=(
                    "\n".join(
                        plan.modification_targets
                    )
                ),
                gap_to_symbol_mapping=(
                    "\n".join(
                        plan.gap_to_symbol_mapping
                    )
                ),
            )
        )

        response = (
            await self.llm.generate(
                prompt
            )
        )

        try:

            cleaned = (
                response
                .replace(
                    "```json",
                    "",
                )
                .replace(
                    "```",
                    "",
                )
                .strip()
            )

            payload = json.loads(
                cleaned
            )

        except Exception:

            payload = {
                "blueprint_steps": []
            }

        blueprint_steps = []

        for step in payload.get(
            "blueprint_steps",
            [],
        ):

            try:

                blueprint_steps.append(
                    BlueprintStep(
                        **step
                    )
                )

            except Exception:
                continue

        if not blueprint_steps:

            blueprint_steps = [
                BlueprintStep(
                    file_path="",
                    symbol_name="",
                    change_type="",
                    reason=(
                        "Blueprint generation failed."
                    ),
                    implementation_steps=[],
                    validation_steps=[],
                    expected_outcome="",
                )
            ]

        confidence = min(
            1.0,
            (
                len(
                    blueprint_steps
                )
                + len(
                    plan.modification_targets
                )
            )
            / 10,
        )

        return (
            ImplementationBlueprint(
                paper_summary=(
                    plan.paper_summary
                ),
                blueprint_steps=(
                    blueprint_steps
                ),
                risks=(
                    plan.risks
                ),
                confidence=(
                    confidence
                ),
            )
        )