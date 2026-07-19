from sqlalchemy.orm import Session

from app.db.models import (
    Workspace,
    WorkspaceOutput,
)

from app.schemas.workspace_output import (
    SaveWorkspaceOutputRequest,
)


class WorkspaceOutputService:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def save_outputs(
        self,
        payload: SaveWorkspaceOutputRequest,
        user_id: str,
    ) -> WorkspaceOutput | None:

        workspace = (
            self.db.query(Workspace)
            .filter(
                Workspace.id == payload.workspace_id,
                Workspace.user_id == user_id,
            )
            .first()
        )

        if workspace is None:
            return None

        existing = (
            self.db.query(WorkspaceOutput)
            .filter(
                WorkspaceOutput.workspace_id
                == payload.workspace_id
            )
            .first()
        )

        if existing:

            existing.hybrid_result = payload.hybrid_result
            existing.reproduction_result = payload.reproduction_result
            existing.blueprint_result = payload.blueprint_result
            existing.evaluation_result = payload.evaluation_result

            self.db.commit()
            self.db.refresh(existing)

            return existing

        output = WorkspaceOutput(
            workspace_id=payload.workspace_id,
            hybrid_result=payload.hybrid_result,
            reproduction_result=payload.reproduction_result,
            blueprint_result=payload.blueprint_result,
            evaluation_result=payload.evaluation_result,
        )

        self.db.add(output)

        self.db.commit()

        self.db.refresh(output)

        return output

    def get_outputs(
        self,
        user_id: str,
        workspace_id: str,
    ):

        workspace = (
            self.db.query(Workspace)
            .filter(
                Workspace.id == workspace_id,
                Workspace.user_id == user_id,
            )
            .first()
        )

        if workspace is None:
            return None

        return (
            self.db.query(WorkspaceOutput)
            .filter(
                WorkspaceOutput.workspace_id == workspace_id,
            )
            .first()
        )