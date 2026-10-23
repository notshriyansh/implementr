from pathlib import Path

from app.evaluation.code_retrieval_dataset import (
    CODE_RETRIEVAL_BENCHMARKS,
)


BACKEND_ROOT = Path(__file__).resolve().parents[2]


def test_benchmark_dataset_is_not_empty():
    assert CODE_RETRIEVAL_BENCHMARKS


def test_benchmark_case_ids_are_unique():
    case_ids = [
        case.case_id
        for case in CODE_RETRIEVAL_BENCHMARKS
    ]

    assert len(case_ids) == len(set(case_ids))


def test_every_case_has_a_question_and_relevant_files():
    for case in CODE_RETRIEVAL_BENCHMARKS:
        assert case.question.strip()
        assert case.expected_files

        assert all(
            path.strip()
            for path in case.expected_files
        )


def test_all_labeled_files_exist():
    missing_files = {
        path
        for case in CODE_RETRIEVAL_BENCHMARKS
        for path in case.expected_files
        if not (BACKEND_ROOT / path).is_file()
    }

    assert not missing_files, (
        f"Benchmark labels reference missing files: "
        f"{sorted(missing_files)}"
    )


def test_paths_are_relative_and_use_forward_slashes():
    for case in CODE_RETRIEVAL_BENCHMARKS:
        for path in case.expected_files:
            assert not Path(path).is_absolute()
            assert "\\" not in path
            assert ".." not in Path(path).parts