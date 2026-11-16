import asyncio

import numpy as np
import pytest

from app.code_vectorstores.symbol_vector_store import SymbolVectorStore
from app.schemas.code_symbol import CodeSymbol


def make_symbol(
    symbol_id: str,
    repository_id: str,
    importance: int = 1,
) -> CodeSymbol:
    return CodeSymbol(
        symbol_id=symbol_id,
        repository_id=repository_id,
        repository_name=repository_id,
        relative_path=f"src/{symbol_id}.py",
        symbol_name=symbol_id,
        symbol_type="function",
        code=f"def {symbol_id}(): pass",
        start_line=1,
        end_line=1,
        importance=importance,
    )


def make_store(tmp_path, monkeypatch) -> SymbolVectorStore:
    monkeypatch.setattr(
        SymbolVectorStore,
        "INDEX_PATH",
        tmp_path / "symbol.index",
    )
    monkeypatch.setattr(
        SymbolVectorStore,
        "METADATA_PATH",
        tmp_path / "symbols.json",
    )
    return SymbolVectorStore(embedding_dimension=2)


def test_scoped_search_finds_symbols_beyond_global_top_k(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    symbols = [
        make_symbol("other_repo_best", "repo-b"),
        make_symbol("target_repo_best", "repo-a"),
        make_symbol("target_repo_second", "repo-a"),
    ]
    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.8, 0.6],
            [0.6, 0.8],
        ],
        dtype=np.float32,
    )

    asyncio.run(store.add_symbols(embeddings, symbols))

    results = asyncio.run(
        store.similarity_search(
            np.array([[1.0, 0.0]], dtype=np.float32),
            k=1,
            repository_id="repo-a",
        )
    )

    assert len(results) == 1
    assert results[0].symbol_id == "target_repo_best"
    assert all(symbol.repository_id == "repo-a" for symbol in results)


def test_scoped_search_preserves_importance_adjusted_ranking(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    symbols = [
        make_symbol("high_similarity", "repo-a", importance=1),
        make_symbol("high_importance", "repo-a", importance=2),
    ]
    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.8, 0.6],
        ],
        dtype=np.float32,
    )

    asyncio.run(store.add_symbols(embeddings, symbols))

    results = asyncio.run(
        store.similarity_search(
            np.array([[1.0, 0.0]], dtype=np.float32),
            k=2,
            repository_id="repo-a",
        )
    )

    assert [symbol.symbol_id for symbol in results] == [
        "high_importance",
        "high_similarity",
    ]


def test_global_search_remains_compatible(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    symbols = [
        make_symbol("repo_a_symbol", "repo-a"),
        make_symbol("repo_b_symbol", "repo-b"),
    ]
    embeddings = np.array(
        [
            [0.8, 0.6],
            [1.0, 0.0],
        ],
        dtype=np.float32,
    )

    asyncio.run(store.add_symbols(embeddings, symbols))

    results = asyncio.run(
        store.similarity_search(
            np.array([[1.0, 0.0]], dtype=np.float32),
            k=1,
        )
    )

    assert len(results) == 1
    assert results[0].symbol_id == "repo_b_symbol"


def test_scoped_search_returns_empty_for_unknown_repository(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    symbols = [make_symbol("existing_symbol", "repo-a")]
    embeddings = np.array([[1.0, 0.0]], dtype=np.float32)

    asyncio.run(store.add_symbols(embeddings, symbols))

    results = asyncio.run(
        store.similarity_search(
            np.array([[1.0, 0.0]], dtype=np.float32),
            k=5,
            repository_id="missing-repo",
        )
    )

    assert results == []


def test_repository_index_contains_only_its_symbols(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    symbols = [
        make_symbol("a1", "repo-a"),
        make_symbol("a2", "repo-a"),
        make_symbol("b1", "repo-b"),
    ]
    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.8, 0.6],
            [0.0, 1.0],
        ],
        dtype=np.float32,
    )

    asyncio.run(store.add_symbols(embeddings, symbols))

    assert store._repository_indexes["repo-a"].ntotal == 2
    assert store._repository_indexes["repo-b"].ntotal == 1


def test_repository_index_updates_when_symbols_are_added(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    asyncio.run(
        store.add_symbols(
            np.array([[1.0, 0.0]], dtype=np.float32),
            [make_symbol("a1", "repo-a")],
        )
    )

    asyncio.run(
        store.add_symbols(
            np.array(
                [
                    [0.0, 1.0],
                    [0.6, 0.8],
                ],
                dtype=np.float32,
            ),
            [
                make_symbol("a2", "repo-a"),
                make_symbol("b1", "repo-b"),
            ],
        )
    )

    assert store._repository_indexes["repo-a"].ntotal == 2
    assert store._repository_indexes["repo-b"].ntotal == 1

    results = asyncio.run(
        store.similarity_search(
            np.array([[0.0, 1.0]], dtype=np.float32),
            k=2,
            repository_id="repo-a",
        )
    )

    assert [symbol.symbol_id for symbol in results] == ["a2", "a1"]


def test_repository_indexes_are_rebuilt_after_reload(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    symbols = [
        make_symbol("a1", "repo-a"),
        make_symbol("b1", "repo-b"),
    ]
    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
        ],
        dtype=np.float32,
    )

    asyncio.run(store.add_symbols(embeddings, symbols))

    reloaded_store = make_store(tmp_path, monkeypatch)

    assert reloaded_store._repository_indexes["repo-a"].ntotal == 1
    assert reloaded_store._repository_indexes["repo-b"].ntotal == 1

    results = asyncio.run(
        reloaded_store.similarity_search(
            np.array([[0.0, 1.0]], dtype=np.float32),
            k=1,
            repository_id="repo-b",
        )
    )

    assert [symbol.symbol_id for symbol in results] == ["b1"]


def test_replace_repository_removes_old_symbols_and_indexes_new_ones(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    asyncio.run(
        store.add_symbols(
            np.array(
                [
                    [1.0, 0.0],
                    [0.0, 1.0],
                    [0.8, 0.6],
                ],
                dtype=np.float32,
            ),
            [
                make_symbol("old_a", "repo-a"),
                make_symbol("keep_b", "repo-b"),
                make_symbol("old_a2", "repo-a"),
            ],
        )
    )

    asyncio.run(
        store.replace_repository(
            "repo-a",
            np.array([[0.6, 0.8]], dtype=np.float32),
            [make_symbol("new_a", "repo-a")],
        )
    )

    assert [s.symbol_id for s in store.symbols] == [
        "keep_b",
        "new_a",
    ]
    assert store.index.ntotal == 2
    assert store._repository_indexes["repo-a"].ntotal == 1
    assert store._repository_indexes["repo-b"].ntotal == 1


def test_replace_repository_preserves_other_repository_search(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    asyncio.run(
        store.add_symbols(
            np.array(
                [
                    [1.0, 0.0],
                    [0.0, 1.0],
                ],
                dtype=np.float32,
            ),
            [
                make_symbol("old_a", "repo-a"),
                make_symbol("keep_b", "repo-b"),
            ],
        )
    )

    asyncio.run(
        store.replace_repository(
            "repo-a",
            np.array([[0.8, 0.6]], dtype=np.float32),
            [make_symbol("new_a", "repo-a")],
        )
    )

    results = asyncio.run(
        store.similarity_search(
            np.array([[0.0, 1.0]], dtype=np.float32),
            k=5,
            repository_id="repo-b",
        )
    )

    assert [s.symbol_id for s in results] == ["keep_b"]


def test_replace_repository_with_empty_symbols_removes_repository(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    asyncio.run(
        store.add_symbols(
            np.array([[1.0, 0.0]], dtype=np.float32),
            [make_symbol("old_a", "repo-a")],
        )
    )

    asyncio.run(
        store.replace_repository(
            "repo-a",
            np.empty((0, 2), dtype=np.float32),
            [],
        )
    )

    assert store.index.ntotal == 0
    assert store.symbols == []
    assert "repo-a" not in store._repository_indexes
    assert "repo-a" not in store._repository_symbol_indices


def test_replace_repository_persists_consistent_indexes_and_metadata(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    asyncio.run(
        store.add_symbols(
            np.array(
                [
                    [1.0, 0.0],
                    [0.0, 1.0],
                ],
                dtype=np.float32,
            ),
            [
                make_symbol("old_a", "repo-a"),
                make_symbol("keep_b", "repo-b"),
            ],
        )
    )

    asyncio.run(
        store.replace_repository(
            "repo-a",
            np.array([[0.6, 0.8]], dtype=np.float32),
            [make_symbol("new_a", "repo-a")],
        )
    )

    assert store.index.ntotal == len(store.symbols)

    reloaded_store = make_store(tmp_path, monkeypatch)

    assert reloaded_store.index.ntotal == 2
    assert [s.symbol_id for s in reloaded_store.symbols] == [
        "keep_b",
        "new_a",
    ]
    assert reloaded_store._repository_indexes["repo-a"].ntotal == 1
    assert reloaded_store._repository_indexes["repo-b"].ntotal == 1

    results = asyncio.run(
        reloaded_store.similarity_search(
            np.array([[0.6, 0.8]], dtype=np.float32),
            k=1,
            repository_id="repo-a",
        )
    )

    assert [s.symbol_id for s in results] == ["new_a"]


def test_replace_repository_rejects_symbols_from_another_repository(
    tmp_path,
    monkeypatch,
):
    store = make_store(tmp_path, monkeypatch)

    with pytest.raises(ValueError):
        asyncio.run(
            store.replace_repository(
                "repo-a",
                np.array([[1.0, 0.0]], dtype=np.float32),
                [make_symbol("wrong_repo", "repo-b")],
            )
        )
