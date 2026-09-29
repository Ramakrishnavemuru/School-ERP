import os
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.document import Document
from backend.app.services.file_service import file_service
from backend.app.utils.permissions import require_roles, get_current_active_user, get_current_user
from backend.app.utils.helpers import log_audit_action

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("")
def upload_document(
    title: str = Form(...),
    document_type: str = Form("General"),
    user_id: Optional[int] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    target_user_id = current_user.id
    if user_id and current_user.role in ["ADMIN", "PRINCIPAL"]:
        target_user_id = user_id

    stored_path = file_service.save_upload_file(file, "documents")
    abs_path = file_service.get_absolute_path(stored_path)
    file_size = os.path.getsize(abs_path) if abs_path.exists() else None

    doc = Document(
        user_id=target_user_id,
        title=title,
        file_path=stored_path,
        document_type=document_type,
        file_size=file_size
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    log_audit_action(db, "DOCUMENT_UPLOAD", "Document", str(doc.id), f"Uploaded document {title}", current_user.id)

    return {
        "message": "Document uploaded successfully",
        "id": doc.id,
        "title": doc.title,
        "file_path": doc.file_path,
        "document_type": doc.document_type
    }

@router.get("")
def list_documents(
    user_id: Optional[int] = None,
    document_type: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(Document).options(joinedload(Document.user))

    if current_user.role not in ["ADMIN", "PRINCIPAL"]:
        query = query.filter(Document.user_id == current_user.id)
    elif user_id:
        query = query.filter(Document.user_id == user_id)

    if document_type:
        query = query.filter(Document.document_type == document_type)

    docs = query.order_by(Document.uploaded_at.desc()).all()
    return [
        {
            "id": d.id,
            "user_id": d.user_id,
            "user_name": d.user.full_name if d.user else "",
            "title": d.title,
            "file_path": d.file_path,
            "document_type": d.document_type,
            "file_size": d.file_size,
            "uploaded_at": d.uploaded_at
        }
        for d in docs
    ]

@router.get("/download/{document_id}")
def download_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if current_user.role not in ["ADMIN", "PRINCIPAL"] and doc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot access this document")

    abs_path = file_service.get_absolute_path(doc.file_path)
    return FileResponse(
        path=abs_path,
        filename=os.path.basename(doc.file_path),
        media_type="application/octet-stream"
    )

@router.get("/file/{file_subpath:path}")
def download_file(
    file_subpath: str,
    current_user: User = Depends(get_current_user)
):
    # Authenticated file serving for assignments, study materials, profiles, etc.
    abs_path = file_service.get_absolute_path(file_subpath)
    return FileResponse(
        path=abs_path,
        filename=os.path.basename(abs_path),
        media_type="application/octet-stream"
    )

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if current_user.role != "ADMIN" and doc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot delete this document")

    file_service.delete_file(doc.file_path)
    db.delete(doc)
    db.commit()
    log_audit_action(db, "DOCUMENT_DELETE", "Document", str(document_id), "Deleted document", current_user.id)
    return {"message": "Document deleted successfully"}
