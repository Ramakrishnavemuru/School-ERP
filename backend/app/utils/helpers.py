import json
from typing import Optional, Any
from sqlalchemy.orm import Session
from backend.app.models.audit_log import AuditLog

def calculate_percentage(obtained: float, max_marks: float) -> float:
    if max_marks <= 0:
        return 0.0
    return round((obtained / max_marks) * 100.0, 2)

def calculate_grade(percentage: float) -> str:
    if percentage >= 90.0:
        return "A+"
    elif percentage >= 80.0:
        return "A"
    elif percentage >= 70.0:
        return "B"
    elif percentage >= 60.0:
        return "C"
    elif percentage >= 50.0:
        return "D"
    else:
        return "F"

def log_audit_action(
    db: Session,
    action: str,
    entity: Optional[str] = None,
    entity_id: Optional[str] = None,
    details: Optional[Any] = None,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None
) -> AuditLog:
    details_str = json.dumps(details) if isinstance(details, (dict, list)) else str(details) if details else None
    audit = AuditLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=str(entity_id) if entity_id is not None else None,
        details=details_str,
        ip_address=ip_address
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit
