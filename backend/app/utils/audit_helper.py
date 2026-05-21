from sqlalchemy.orm import Session

from app.models.audit import AuditEntry


def create_audit_entry(
    db: Session,
    entity_type: str,
    entity_id: str,
    action: str,
    actor: str = "system",
    before_state: dict | None = None,
    after_state: dict | None = None,
    ip_address: str | None = None,
) -> AuditEntry:
    entry = AuditEntry(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        actor=actor,
        before_state=before_state,
        after_state=after_state,
        ip_address=ip_address,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
