import asyncio

from app.hybrid.hybrid_retrieval_service import HybridRetrievalService


class FakePaperRetrieval:
    def __init__(self):
        self.calls = []

    async def retrieve(self, query, k=5):
        self.calls.append({"query": query, "k": k})
        return []


class FakeCodeRetrieval:
    def __init__(self):
        self.calls = []

    async def retrieve(self, query, k=5, repository_id=None):
        self.calls.append(
            {
                "query": query,
                "k": k,
                "repository_id": repository_id,
            }
        )
        return []


def test_repository_scope_applies_only_to_code_retrieval():
    paper = FakePaperRetrieval()
    code = FakeCodeRetrieval()
    service = HybridRetrievalService(paper, code)

    paper_chunks, code_chunks = asyncio.run(
        service.retrieve(
            query="implement attention",
            paper_k=4,
            code_k=6,
            repository_id="repo-a",
        )
    )

    assert paper_chunks == []
    assert code_chunks == []

    assert paper.calls == [
        {"query": "implement attention", "k": 4}
    ]
    assert code.calls == [
        {
            "query": "implement attention",
            "k": 6,
            "repository_id": "repo-a",
        }
    ]


def test_hybrid_retrieval_without_scope_remains_compatible():
    paper = FakePaperRetrieval()
    code = FakeCodeRetrieval()
    service = HybridRetrievalService(paper, code)

    asyncio.run(
        service.retrieve("explain the architecture")
    )

    assert paper.calls == [
        {"query": "explain the architecture", "k": 3}
    ]
    assert code.calls == [
        {
            "query": "explain the architecture",
            "k": 3,
            "repository_id": None,
        }
    ]