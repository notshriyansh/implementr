from pydantic import BaseModel


class SaveWorkspaceOutputRequest(
    BaseModel,
):
    workspace_id: str

    hybrid_result: dict | None = None

    reproduction_result: dict | None = None

    blueprint_result: dict | None = None

    evaluation_result: dict | None = None


class WorkspaceOutputResponse(
    BaseModel,
):
    id: str

    workspace_id: str

    hybrid_result: dict | None

    reproduction_result: dict | None

    blueprint_result: dict | None

    evaluation_result: dict | None