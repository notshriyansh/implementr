from app.concepts.concept_index import ConceptIndex
from app.schemas.concept import Concept


def make_concept(
    name: str,
    repository_id: str,
    file_path: str,
) -> Concept:
    return Concept(
        name=name,
        source="repository",
        repository_id=repository_id,
        file_path=file_path,
        symbol_name=f"{name}_symbol",
    )


def test_replace_repository_replaces_only_target_repository():
    index = ConceptIndex()

    index.add(make_concept("attention", "repo-a", "src/old.py"))
    index.add(make_concept("transformer", "repo-b", "src/model.py"))

    index.replace_repository(
        "repo-a",
        [
            make_concept("embedding", "repo-a", "src/new.py"),
        ],
    )

    assert index.get("attention") == []
    assert len(index.get("transformer")) == 1
    assert len(index.get("embedding")) == 1

    assert index.get("transformer")[0].repository_id == "repo-b"
    assert index.get("embedding")[0].repository_id == "repo-a"


def test_replace_repository_with_empty_list_removes_only_target():
    index = ConceptIndex()

    index.add(make_concept("attention", "repo-a", "src/a.py"))
    index.add(make_concept("attention", "repo-b", "src/b.py"))

    index.replace_repository("repo-a", [])

    remaining = index.get("attention")

    assert len(remaining) == 1
    assert remaining[0].repository_id == "repo-b"


def test_replace_repository_preserves_other_repositories_with_same_name():
    index = ConceptIndex()

    index.add(make_concept("attention", "repo-a", "src/a.py"))
    index.add(make_concept("attention", "repo-b", "src/b.py"))

    index.replace_repository(
        "repo-a",
        [make_concept("attention", "repo-a", "src/new.py")],
    )

    attention_concepts = index.get("attention")

    assert len(attention_concepts) == 2
    assert {
        concept.file_path for concept in attention_concepts
    } == {"src/new.py", "src/b.py"}
