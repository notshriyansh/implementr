from pydantic import BaseModel


class ArchitectureBenchmark(
    BaseModel,
):
    question: str

    expected_files: list[str]

    expected_symbols: list[str]


ARCHITECTURE_BENCHMARKS = [
    ArchitectureBenchmark(
        question=(
            "How does streaming work?"
        ),
        expected_files=[
            (
                "app/chat/"
                "rag_chat_service.py"
            ),
            (
                "app/api/routes/"
                "chat.py"
            ),
        ],
        expected_symbols=[
            "stream_chat",
            "stream_generate",
        ],
    ),
]

