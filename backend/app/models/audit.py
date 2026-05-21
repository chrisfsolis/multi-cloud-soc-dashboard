import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


def _make_audit_id() -> str:
    return f"aud-{uuid.uuid4().hex[:8]}"


class AuditEntry(Base):
    __tablename__ = "audit_entries"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_make_audit_id)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    actor: Mapped[str] = mapped_column(String(255), nullable=False, default="system")
    before_state: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    after_state: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
