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

router = APIRouter(
    prefix="/workspaces",
    tags=["workspaces"],
)


@router.post("")
def create_workspace(
    payload: CreateWorkspaceRequest,
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return service.create_workspace(
        payload
    )


@router.get("")
def list_workspaces(
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return service.list_workspaces()

@router.get("/{workspace_id}")
def get_workspace(
    workspace_id: str,
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return service.get_workspace(
        workspace_id
    )

@router.put("/{workspace_id}")
def update_workspace(
    workspace_id: str,
    payload: UpdateWorkspaceRequest,
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return service.update_workspace(
        workspace_id,
        payload,
    )