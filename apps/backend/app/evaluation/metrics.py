from collections.abc import Mapping, Sequence
import math


def keyword_match_score(text: str, keywords: list[str]) -> float:
    if not keywords:
        return 0.0

    text_lower = text.lower()
    matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
    return matches / len(keywords)


def _validate_k(k: int) -> None:
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")


def _unique_in_order(items: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(items))


def recall_at_k(
    retrieved_ids: Sequence[str],
    relevant_ids: set[str] | frozenset[str],
    k: int,
) -> float:
    _validate_k(k)
    if not relevant_ids:
        raise ValueError("relevant_ids must contain at least one item")

    ranked = _unique_in_order(retrieved_ids)[:k]
    return len(set(ranked) & set(relevant_ids)) / len(relevant_ids)


def precision_at_k(
    retrieved_ids: Sequence[str],
    relevant_ids: set[str] | frozenset[str],
    k: int,
) -> float:
    _validate_k(k)
    if not relevant_ids:
        raise ValueError("relevant_ids must contain at least one item")

    ranked = _unique_in_order(retrieved_ids)[:k]
    return len(set(ranked) & set(relevant_ids)) / k


def reciprocal_rank(
    retrieved_ids: Sequence[str],
    relevant_ids: set[str] | frozenset[str],
) -> float:
    if not relevant_ids:
        raise ValueError("relevant_ids must contain at least one item")

    for rank, item_id in enumerate(_unique_in_order(retrieved_ids), start=1):
        if item_id in relevant_ids:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(
    retrieved_ids: Sequence[str],
    relevance_by_id: Mapping[str, int | float],
    k: int,
) -> float:
    _validate_k(k)
    if any(not math.isfinite(float(score)) or score < 0 for score in relevance_by_id.values()):
        raise ValueError("relevance grades must be finite and non-negative")

    ranked = _unique_in_order(retrieved_ids)[:k]

    def dcg(ids: Sequence[str]) -> float:
        return sum(
            (2 ** float(relevance_by_id.get(item_id, 0)) - 1)
            / math.log2(rank + 1)
            for rank, item_id in enumerate(ids, start=1)
        )

    actual = dcg(ranked)
    ideal_ids = sorted(
        relevance_by_id,
        key=lambda item_id: relevance_by_id[item_id],
        reverse=True,
    )[:k]
    ideal = dcg(ideal_ids)
    return actual / ideal if ideal else 0.0



def evaluate_ranking(
    retrieved_ids: Sequence[str],
    relevant_ids: set[str] | frozenset[str],
    k: int = 5,
) -> dict[str, float]:
    return {
        f"recall@{k}": recall_at_k(retrieved_ids, relevant_ids, k),
        f"precision@{k}": precision_at_k(retrieved_ids, relevant_ids, k),
        "reciprocal_rank": reciprocal_rank(retrieved_ids, relevant_ids),
        f"ndcg@{k}": ndcg_at_k(
            retrieved_ids,
            {item_id: 1 for item_id in relevant_ids},
            k,
        ),
    }
