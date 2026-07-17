from pydantic import BaseModel


class CreateWorkspaceRequest(BaseModel):
    name: str

    selected_repository: str | None = None

    workspace_question: str | None = None

    blueprint_target_file: str | None = None

    blueprint_target_symbol: str | None = None

    blueprint_target_reason: str | None = None

    selected_paper: str | None = None


class WorkspaceResponse(BaseModel):
    id: str

    name: str

    selected_repository: str | None

    workspace_question: str | None

    blueprint_target_file: str | None

    blueprint_target_symbol: str | None

    blueprint_target_reason: str | None

    selected_paper: str | None


class UpdateWorkspaceRequest(
    BaseModel,
):
    name: str | None = None

    selected_paper: str | None = None

    selected_repository: str | None = None

    workspace_question: str | None = None

    blueprint_target_file: str | None = None

    blueprint_target_symbol: str | None = None

    blueprint_target_reason: str | None = None