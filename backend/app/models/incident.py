import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, JSON, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


def _make_incident_id() -> str:
    return f"inc-{uuid.uuid4().hex[:12]}"


def _make_note_id() -> str:
    return f"note-{uuid.uuid4().hex[:8]}"


incident_alerts = Table(
    "incident_alerts",
    Base.metadata,
    Column("incident_id", String, ForeignKey("incidents.id"), primary_key=True),
    Column("alert_id", String, ForeignKey("alerts.id"), primary_key=True),
)


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=_make_incident_id
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="new")
    assigned_to: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_providers: Mapped[list | None] = mapped_column(JSON, nullable=True)
    mitre_tactics: Mapped[list | None] = mapped_column(JSON, nullable=True)
    detection_rule: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    alerts = relationship("Alert", secondary=incident_alerts, backref="incidents")
    notes = relationship("IncidentNote", back_populates="incident", cascade="all, delete-orphan")


class IncidentNote(Base):
    __tablename__ = "incident_notes"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_make_note_id)
    incident_id: Mapped[str] = mapped_column(
        String, ForeignKey("incidents.id"), nullable=False
    )
    content: Mapped[str] = mapped_column(String(5000), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    incident = relationship("Incident", back_populates="notes")
