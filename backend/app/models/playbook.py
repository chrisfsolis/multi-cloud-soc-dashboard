import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Boolean, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


def _make_playbook_id() -> str:
    return f"pb-{uuid.uuid4().hex[:12]}"


def _make_run_id() -> str:
    return f"run-{uuid.uuid4().hex[:12]}"


class Playbook(Base):
    __tablename__ = "playbooks"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=_make_playbook_id
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    trigger: Mapped[str | None] = mapped_column(String(100), nullable=True)
    approval_required: Mapped[bool] = mapped_column(Boolean, default=False)
    steps: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    run_count: Mapped[int] = mapped_column(Integer, default=0)
    last_run: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    runs = relationship("PlaybookRun", back_populates="playbook", cascade="all, delete-orphan")


class PlaybookRun(Base):
    __tablename__ = "playbook_runs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_make_run_id)
    playbook_id: Mapped[str] = mapped_column(
        String, ForeignKey("playbooks.id"), nullable=False
    )
    incident_id: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    triggered_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    steps: Mapped[list | None] = mapped_column(JSON, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    playbook = relationship("Playbook", back_populates="runs")
