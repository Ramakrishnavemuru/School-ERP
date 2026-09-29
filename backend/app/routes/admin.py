from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.audit_log import AuditLog
from backend.app.utils.permissions import require_roles
from backend.app.utils.pagination import paginate_query
from backend.app.services.report_service import report_service

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/overview")
def get_admin_overview(
    current_user: User = Depends(require_roles(["ADMIN"])),
    db: Session = Depends(get_db)
):
    return report_service.get_admin_dashboard(db)

@router.get("/audit-logs")
def get_audit_logs(
    action: Optional[str] = None,
    entity: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_roles(["ADMIN"])),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action.ilike(f"%{action}%"))
    if entity:
        query = query.filter(AuditLog.entity.ilike(f"%{entity}%"))
    query = query.order_by(AuditLog.timestamp.desc())

    paginated = paginate_query(query, page, page_size)
    items = []
    for log in paginated["items"]:
        items.append({
            "id": log.id,
            "user_id": log.user_id,
            "username": log.user.username if log.user else "System",
            "action": log.action,
            "entity": log.entity,
            "entity_id": log.entity_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "timestamp": log.timestamp
        })
    paginated["items"] = items
    return paginated

@router.get("/settings")
def get_system_settings(
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    from backend.app.config import settings
    return {
        "project_name": settings.PROJECT_NAME,
        "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_MB,
        "allowed_extensions": settings.ALLOWED_EXTENSIONS,
        "token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES
    }
