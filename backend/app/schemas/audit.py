from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AuditEntryResponse(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    action: str
    actor: str
    before_state: Any = None
    after_state: Any = None
    ip_address: str | None = None
    timestamp: datetime

    model_config = {"from_attributes": True}
