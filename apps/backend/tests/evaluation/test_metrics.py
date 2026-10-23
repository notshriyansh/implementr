import pytest

from app.evaluation.metrics import (
    evaluate_ranking,
    keyword_match_score,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_recall_at_k_counts_relevant_results_in_top_k() -> None:
    assert recall_at_k(["a", "b", "c"], {"b", "c", "d"}, 2) == pytest.approx(1 / 3)


def test_precision_at_k_uses_k_as_denominator_when_fewer_results_exist() -> None:
    assert precision_at_k(["a", "b"], {"b"}, 5) == pytest.approx(1 / 5)


def test_metrics_ignore_duplicate_ids_after_first_occurrence() -> None:
    assert recall_at_k(["a", "a", "b"], {"b"}, 2) == 1.0
    assert reciprocal_rank(["a", "a", "b"], {"b"}) == pytest.approx(1 / 2)


def test_reciprocal_rank_is_zero_when_no_relevant_item_is_retrieved() -> None:
    assert reciprocal_rank(["a", "b"], {"c"}) == 0.0


def test_ndcg_rewards_relevant_results_at_higher_ranks() -> None:
    relevance = {"best": 3, "okay": 1, "irrelevant": 0}
    best_first = ndcg_at_k(["best", "okay", "irrelevant"], relevance, 3)
    worst_first = ndcg_at_k(["irrelevant", "okay", "best"], relevance, 3)
    assert best_first == pytest.approx(1.0)
    assert worst_first < best_first


def test_ndcg_returns_zero_for_zero_ideal_gain() -> None:
    assert ndcg_at_k(["a", "b"], {"a": 0, "b": 0}, 2) == 0.0


@pytest.mark.parametrize("k", [0, -1, True, 1.5])
def test_ranking_metrics_reject_invalid_k(k: int) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        recall_at_k(["a"], {"a"}, k)  # type: ignore[arg-type]


@pytest.mark.parametrize("metric", [recall_at_k, precision_at_k, reciprocal_rank])
def test_unlabeled_query_is_not_silently_scored_as_failure(metric) -> None:
    args = (["a"], set()) if metric is reciprocal_rank else (["a"], set(), 1)
    with pytest.raises(ValueError, match="relevant_ids"):
        metric(*args)



def test_evaluate_ranking_returns_consistent_metric_names() -> None:
    result = evaluate_ranking(["a", "b", "c"], {"b", "c"}, k=2)

    assert result["recall@2"] == pytest.approx(0.5)
    assert result["precision@2"] == pytest.approx(0.5)
    assert result["reciprocal_rank"] == pytest.approx(0.5)
    assert result["ndcg@2"] == pytest.approx(0.3868528072)


def test_keyword_metric_remains_backward_compatible_and_handles_empty_labels() -> None:
    assert keyword_match_score("Transformers use attention", ["attention", "CNN"]) == 0.5
    assert keyword_match_score("anything", []) == 0.0


def test_ranked_relevance_evaluator_uses_retrieval_only_and_returns_ids() -> None:
    import asyncio
    from types import SimpleNamespace

    from app.evaluation.retrieval_eval import RetrievalEvaluator

    class FakeRetrievalService:
        async def retrieve(self, query: str, k: int = 5):
            assert query == "question"
            return [
                SimpleNamespace(chunk_id="irrelevant"),
                SimpleNamespace(chunk_id="relevant"),
            ][:k]

    result = asyncio.run(
        RetrievalEvaluator(FakeRetrievalService()).evaluate_ranked_relevance(
            question="question",
            relevant_chunk_ids={"relevant"},
            k=2,
        )
    )

    assert result["recall@2"] == 1.0
    assert result["precision@2"] == 0.5
    assert result["reciprocal_rank"] == 0.5
    assert result["retrieved_chunk_ids"] == ["irrelevant", "relevant"]
