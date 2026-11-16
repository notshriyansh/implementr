
import asyncio

from app.hybrid.hybrid_retrieval_service import HybridRetrievalService


class FakePaperRetrieval:
    def __init__(self):
        self.calls = []

    async def retrieve(
        self,
        query,
        k=5,
        paper_id=None,
    ):
        self.calls.append(
            {
                "query": query,
                "k": k,
                "paper_id": paper_id,
            }
        )
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
        {
            "query": "implement attention",
            "k": 4,
            "paper_id": None,
        }
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
        {
            "query": "explain the architecture",
            "k": 3,
            "paper_id": None,
        }
    ]

    assert code.calls == [
        {
            "query": "explain the architecture",
            "k": 3,
            "repository_id": None,
        }
    ]


def test_paper_and_repository_scopes_are_forwarded_independently():
    paper_retrieval = FakePaperRetrieval()
    code_retrieval = FakeCodeRetrieval()

    service = HybridRetrievalService(
        paper_retrieval=paper_retrieval,
        code_retrieval=code_retrieval,
    )

    asyncio.run(
        service.retrieve(
            query="Explain attention",
            paper_id="2401.12345",
            repository_id="repo-123",
        )
    )

    assert paper_retrieval.calls == [
        {
            "query": "Explain attention",
            "k": 3,
            "paper_id": "2401.12345",
        }
    ]

    assert code_retrieval.calls == [
        {
            "query": "Explain attention",
            "k": 3,
            "repository_id": "repo-123",
        }
    ]
