from fastapi import APIRouter
from fastapi import Depends

from app.schemas.workspace_output import (
    SaveWorkspaceOutputRequest,
)

from app.workspaces.workspace_output_service import (
    WorkspaceOutputService,
)

from app.core.dependencies import (
    get_workspace_output_service,
)

router = APIRouter(
    prefix="/workspace-outputs",
    tags=["workspace-outputs"],
)


@router.post("")
def save_outputs(
    payload: SaveWorkspaceOutputRequest,
    service: WorkspaceOutputService = Depends(
        get_workspace_output_service
    ),
):
    return service.save_outputs(
        payload
    )


@router.get("/{workspace_id}")
def get_outputs(
    workspace_id: str,
    service: WorkspaceOutputService = Depends(
        get_workspace_output_service
    ),
):
    return service.get_outputs(
        workspace_id
    )