import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


def _make_asset_id() -> str:
    return f"ast-{uuid.uuid4().hex[:12]}"


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_make_asset_id)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    provider: Mapped[str] = mapped_column(String(20), nullable=False)
    environment: Mapped[str] = mapped_column(String(30), nullable=False, default="production")
    owner: Mapped[str | None] = mapped_column(String(255), nullable=True)
    criticality: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    risk_score: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
