from app.architecture.architecture_reasoning_service import (
    ArchitectureReasoningService,
)


class ArchitectureEvaluator:
    def __init__(
        self,
        architecture_service: (
            ArchitectureReasoningService
        ),
    ) -> None:
        self.architecture_service = (
            architecture_service
        )

    async def evaluate(
        self,
        question: str,
        expected_files: list[str],
        expected_symbols: list[str],
    ) -> dict:
        result = await (
            self.architecture_service.analyze(
                question
            )
        )

        retrieved_files = set(
            result.relevant_files
        )

        retrieved_symbols = set(
            result.relevant_symbols
        )

        file_hits = sum(
            1
            for file in expected_files
            if file in retrieved_files
        )

        symbol_hits = sum(
            1
            for symbol in expected_symbols
            if symbol in retrieved_symbols
        )

        file_score = (
            file_hits / len(expected_files)
            if expected_files
            else 0
        )

        symbol_score = (
            symbol_hits
            / len(expected_symbols)
            if expected_symbols
            else 0
        )

        overall_score = (
            file_score + symbol_score
        ) / 2

        return {
            "question": question,
            "file_score": file_score,
            "symbol_score": symbol_score,
            "overall_score": overall_score,
        }
