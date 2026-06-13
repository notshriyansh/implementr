from pydantic import BaseModel


class BenchmarkExample(
    BaseModel,
):
    question: str

    expected_keywords: list[str]

    expected_paper_id: str


BENCHMARK_DATASET = [
    BenchmarkExample(
        question=(
            "Why are transformers "
            "effective in low-labeled "
            "video settings?"
        ),
        expected_keywords=[
            "transformers",
            "representation",
            "CNNs",
        ],
        expected_paper_id=(
            "video-transformers"
        ),
    ),
    BenchmarkExample(
        question=(
            "What architecture does "
            "the paper propose?"
        ),
        expected_keywords=[
            "Uniformer",
            "attention",
            "MHSA",
        ],
        expected_paper_id=(
            "video-transformers"
        ),
    ),
]