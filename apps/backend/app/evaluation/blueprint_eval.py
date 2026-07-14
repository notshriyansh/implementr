from app.blueprints.implementation_blueprint_service import (
    ImplementationBlueprintService,
)

from app.schemas.blueprint_evaluation import (
    BlueprintEvaluationResult,
)


class BlueprintEvaluator:
    def __init__(
        self,
        blueprint_service: (
            ImplementationBlueprintService
        ),
    ) -> None:

        self.blueprint_service = (
            blueprint_service
        )

    async def evaluate(
        self,
        question: str,
        expected_files: list[str],
        expected_symbols: list[str],
        expected_gaps: list[str],
    ) -> BlueprintEvaluationResult:

        blueprint = await (
            self.blueprint_service.generate(
                question
            )
        )

        predicted_files = {
            step.file_path
            for step
            in blueprint.blueprint_steps
        }

        predicted_symbols = {
            step.symbol_name
            for step
            in blueprint.blueprint_steps
        }

        file_hits = sum(
            1
            for file
            in expected_files
            if file in predicted_files
        )

        symbol_hits = sum(
            1
            for symbol
            in expected_symbols
            if symbol in predicted_symbols
        )

        target_file_score = (
            file_hits / len(expected_files)
            if expected_files
            else 0
        )

        target_symbol_score = (
            symbol_hits
            / len(expected_symbols)
            if expected_symbols
            else 0
        )

        gap_coverage_score = min(
            1.0,
            len(
                blueprint.blueprint_steps
            )
            / max(
                len(expected_gaps),
                1,
            ),
        )

        implementation_score = min(
            1.0,
            len(
                blueprint.blueprint_steps
            )
            / 5,
        )

        risk_score = min(
            1.0,
            len(
                blueprint.risks
            )
            / 5,
        )

        overall_score = (
            target_file_score
            + target_symbol_score
            + gap_coverage_score
            + implementation_score
            + risk_score
        ) / 5

        return (
            BlueprintEvaluationResult(
                target_file_score=(
                    target_file_score
                ),
                target_symbol_score=(
                    target_symbol_score
                ),
                gap_coverage_score=(
                    gap_coverage_score
                ),
                implementation_score=(
                    implementation_score
                ),
                risk_score=(
                    risk_score
                ),
                overall_score=(
                    round(
                        overall_score,
                        3,
                    )
                ),
            )
        )