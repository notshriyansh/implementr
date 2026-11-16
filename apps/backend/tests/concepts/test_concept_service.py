from app.concepts.concept_service import ConceptService
from app.schemas.code_symbol import CodeSymbol


def test_symbol_to_concepts_preserves_repository_id():
    service = ConceptService(extractor=None, matcher=None)

    symbol = CodeSymbol(
        symbol_id="symbol-1",
        repository_id="repo-a",
        repository_name="repository-a",
        relative_path="src/attention.py",
        symbol_name="MultiHeadAttention",
        symbol_type="class",
        code="class MultiHeadAttention: pass",
        start_line=1,
        end_line=2,
    )

    concepts = service.symbol_to_concepts(symbol)

    assert concepts
    assert all(
        concept.repository_id == "repo-a"
        for concept in concepts
    )
    assert all(
        concept.source == "repository"
        for concept in concepts
    )
    assert all(
        concept.file_path == "src/attention.py"
        for concept in concepts
    )
