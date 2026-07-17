from sqlalchemy.orm import Session

from app.db.models import Workspace

from app.schemas.workspace import (
    CreateWorkspaceRequest,
    UpdateWorkspaceRequest,
)


class WorkspaceService:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create_workspace(
        self,
        payload: CreateWorkspaceRequest,
    ) -> Workspace:

        workspace = Workspace(
            name=payload.name,
            selected_repository=(
                payload.selected_repository
            ),
            workspace_question=(
                payload.workspace_question
            ),
            blueprint_target_file=(
                payload.blueprint_target_file
            ),
            blueprint_target_symbol=(
                payload.blueprint_target_symbol
            ),
            blueprint_target_reason=(
                payload.blueprint_target_reason
            ),
            selected_paper=(
                payload.selected_paper
            ),
        )

        self.db.add(workspace)

        self.db.commit()

        self.db.refresh(workspace)

        return workspace

    def list_workspaces(
        self,
    ) -> list[Workspace]:

        return (
            self.db.query(
                Workspace
            )
            .order_by(
                Workspace.updated_at.desc()
            )
            .all()
        )
    
    def get_workspace(
        self,
        workspace_id: str,
    ):
        return (
            self.db.query(Workspace)
            .filter(
                Workspace.id == workspace_id
            )
            .first()
        )
    

    def update_workspace(
        self,
        workspace_id: str,
        payload: UpdateWorkspaceRequest,
    ):
        workspace = (
            self.db.query(Workspace)
            .filter(
                Workspace.id == workspace_id
            )
            .first()
        )

        if not workspace:
            return None

        updates = payload.model_dump(
            exclude_unset=True,
        )

        for key, value in updates.items():
            setattr(
                workspace,
                key,
                value,
            )

        self.db.commit()

        self.db.refresh(workspace)

        return workspace