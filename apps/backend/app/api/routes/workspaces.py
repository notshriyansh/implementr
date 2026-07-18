from fastapi import APIRouter
from fastapi import Depends

from app.schemas.workspace import (
    CreateWorkspaceRequest,
    UpdateWorkspaceRequest,
)

from app.workspaces.workspace_service import (
    WorkspaceService,
)

from app.core.dependencies import (
    get_workspace_service,
)

from app.auth.clerk import get_current_user

from app.auth.current_user import CurrentUser

router = APIRouter(
    prefix="/workspaces",
    tags=["workspaces"],
)


@router.post("")
def create_workspace(
    payload: CreateWorkspaceRequest,
    current_user: CurrentUser = Depends(
        get_current_user,
    ),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return service.create_workspace(
        payload,
        current_user.user_id,
    )


@router.get("")
def list_workspaces(
    current_user: CurrentUser = Depends(
        get_current_user,
    ),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return service.list_workspaces(
        current_user.user_id
    )

@router.get("/{workspace_id}")
def get_workspace(
    workspace_id: str,
    current_user: CurrentUser = Depends(
        get_current_user,
    ),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return service.get_workspace(
        current_user.user_id,
        workspace_id,
    )

@router.put("/{workspace_id}")
def update_workspace(
    workspace_id: str,
    payload: UpdateWorkspaceRequest,
    current_user: CurrentUser = Depends(
        get_current_user,
    ),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return service.update_workspace(
        current_user.user_id,
        workspace_id,
        payload,
    )