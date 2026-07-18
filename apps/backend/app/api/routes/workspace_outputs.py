from fastapi import APIRouter
from fastapi import Depends

from app.auth.clerk import get_current_user
from app.auth.current_user import CurrentUser

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
    current_user: CurrentUser = Depends(
        get_current_user,
    ),
    service: WorkspaceOutputService = Depends(
        get_workspace_output_service,
    ),
):
    return service.save_outputs(
        payload,
        current_user.user_id,
    )


@router.get("/{workspace_id}")
def get_outputs(
    workspace_id: str,
    current_user: CurrentUser = Depends(
        get_current_user,
    ),
    service: WorkspaceOutputService = Depends(
        get_workspace_output_service,
    ),
):
    return service.get_outputs(
        current_user.user_id,
        workspace_id,
    )