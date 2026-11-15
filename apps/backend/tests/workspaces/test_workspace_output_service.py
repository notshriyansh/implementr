from types import SimpleNamespace
from unittest.mock import MagicMock

from app.schemas.workspace_output import SaveWorkspaceOutputRequest
from app.workspaces.workspace_output_service import WorkspaceOutputService


def make_service(existing_output):
    db = MagicMock()
    db.query.return_value.filter.return_value.first.side_effect = [
        SimpleNamespace(id="workspace-1", user_id="user-1"),
        existing_output,
    ]

    service = WorkspaceOutputService(db)
    return service, db


def test_partial_save_preserves_existing_outputs():
    existing = SimpleNamespace(
        hybrid_result={"answer": "original analysis"},
        reproduction_result={"plan": "original plan"},
        blueprint_result={"steps": ["step 1"]},
        evaluation_result={"score": 0.8},
    )
    service, db = make_service(existing)

    payload = SaveWorkspaceOutputRequest(
        workspace_id="workspace-1",
        blueprint_result={"steps": ["updated step"]},
    )

    result = service.save_outputs(payload, "user-1")

    assert result is existing
    assert existing.hybrid_result == {"answer": "original analysis"}
    assert existing.reproduction_result == {"plan": "original plan"}
    assert existing.blueprint_result == {"steps": ["updated step"]}
    assert existing.evaluation_result == {"score": 0.8}
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(existing)


def test_partial_save_can_explicitly_clear_an_output():
    existing = SimpleNamespace(
        hybrid_result={"answer": "analysis"},
        reproduction_result={"plan": "plan"},
        blueprint_result={"steps": ["step"]},
        evaluation_result={"score": 0.8},
    )
    service, _ = make_service(existing)

    payload = SaveWorkspaceOutputRequest.model_validate(
        {
            "workspace_id": "workspace-1",
            "evaluation_result": None,
        }
    )

    result = service.save_outputs(payload, "user-1")

    assert result is existing
    assert existing.hybrid_result == {"answer": "analysis"}
    assert existing.reproduction_result == {"plan": "plan"}
    assert existing.blueprint_result == {"steps": ["step"]}
    assert existing.evaluation_result is None
