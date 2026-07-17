from datetime import datetime
from uuid import uuid4

from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from app.db.base import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String,
    )

    selected_repository: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    workspace_question: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    blueprint_target_file: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    blueprint_target_symbol: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    blueprint_target_reason: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    selected_paper: Mapped[str] = mapped_column(
    Text,
    nullable=True,
)

class WorkspaceOutput(Base):
    __tablename__ = "workspace_outputs"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    workspace_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("workspaces.id"),
    )

    hybrid_result: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
    )

    reproduction_result: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
    )

    blueprint_result: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
    )

    evaluation_result: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )