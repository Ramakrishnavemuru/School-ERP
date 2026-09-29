from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.exam import Exam
from backend.app.models.class_model import ClassModel
from backend.app.models.academic_year import AcademicYear
from backend.app.schemas.exam import ExamCreate, ExamUpdate, ExamResponse
from backend.app.services.notification_service import notification_service
from backend.app.utils.permissions import require_roles, get_current_active_user
from backend.app.utils.helpers import log_audit_action

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.get("", response_model=List[ExamResponse])
def list_exams(
    class_id: Optional[int] = None,
    is_published: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(Exam).options(
        joinedload(Exam.academic_year),
        joinedload(Exam.class_obj)
    )

    if current_user.role == "STUDENT" and current_user.student_profile:
        query = query.filter(Exam.class_id == current_user.student_profile.class_id)
    elif class_id:
        query = query.filter(Exam.class_id == class_id)

    if is_published is not None:
        query = query.filter(Exam.is_published == is_published)

    exams = query.order_by(Exam.start_date.desc()).all()
    return [
        ExamResponse(
            id=e.id,
            name=e.name,
            exam_type=e.exam_type,
            academic_year_id=e.academic_year_id,
            class_id=e.class_id,
            start_date=e.start_date,
            end_date=e.end_date,
            is_published=e.is_published,
            academic_year_name=e.academic_year.name if e.academic_year else None,
            class_name=e.class_obj.name if e.class_obj else None,
            created_at=e.created_at,
            updated_at=e.updated_at
        )
        for e in exams
    ]

@router.post("", response_model=ExamResponse)
def create_exam(
    exam_in: ExamCreate,
    current_user: User = Depends(require_roles(["ADMIN", "TEACHER"])),
    db: Session = Depends(get_db)
):
    exam = Exam(
        name=exam_in.name,
        exam_type=exam_in.exam_type,
        academic_year_id=exam_in.academic_year_id,
        class_id=exam_in.class_id,
        start_date=exam_in.start_date,
        end_date=exam_in.end_date,
        is_published=exam_in.is_published
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)

    log_audit_action(db, "EXAM_CREATE", "Exam", str(exam.id), f"Created exam {exam.name}", current_user.id)

    return ExamResponse(
        id=exam.id,
        name=exam.name,
        exam_type=exam.exam_type,
        academic_year_id=exam.academic_year_id,
        class_id=exam.class_id,
        start_date=exam.start_date,
        end_date=exam.end_date,
        is_published=exam.is_published,
        created_at=exam.created_at,
        updated_at=exam.updated_at
    )

@router.put("/{exam_id}", response_model=ExamResponse)
def update_exam(
    exam_id: int,
    exam_in: ExamUpdate,
    current_user: User = Depends(require_roles(["ADMIN", "TEACHER"])),
    db: Session = Depends(get_db)
):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    if exam_in.name is not None:
        exam.name = exam_in.name
    if exam_in.exam_type is not None:
        exam.exam_type = exam_in.exam_type
    if exam_in.academic_year_id is not None:
        exam.academic_year_id = exam_in.academic_year_id
    if exam_in.class_id is not None:
        exam.class_id = exam_in.class_id
    if exam_in.start_date is not None:
        exam.start_date = exam_in.start_date
    if exam_in.end_date is not None:
        exam.end_date = exam_in.end_date
    if exam_in.is_published is not None:
        exam.is_published = exam_in.is_published

    db.commit()
    db.refresh(exam)
    return ExamResponse(
        id=exam.id,
        name=exam.name,
        exam_type=exam.exam_type,
        academic_year_id=exam.academic_year_id,
        class_id=exam.class_id,
        start_date=exam.start_date,
        end_date=exam.end_date,
        is_published=exam.is_published,
        created_at=exam.created_at,
        updated_at=exam.updated_at
    )

@router.patch("/{exam_id}/publish")
def publish_exam(
    exam_id: int,
    current_user: User = Depends(require_roles(["ADMIN", "TEACHER", "PRINCIPAL"])),
    db: Session = Depends(get_db)
):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    exam.is_published = True
    db.commit()

    # Notify students and parents
    notification_service.notify_role(
        db=db,
        role="STUDENT",
        title="Exam Results Published",
        message=f"Results for '{exam.name}' have been officially published.",
        link="/frontend/student/results.html",
        notification_type="SUCCESS"
    )

    log_audit_action(db, "EXAM_PUBLISH", "Exam", str(exam.id), f"Published results for {exam.name}", current_user.id)
    return {"message": f"Results for '{exam.name}' published successfully"}

@router.delete("/{exam_id}")
def delete_exam(
    exam_id: int,
    current_user: User = Depends(require_roles(["ADMIN"])),
    db: Session = Depends(get_db)
):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    db.delete(exam)
    db.commit()
    log_audit_action(db, "EXAM_DELETE", "Exam", str(exam_id), "Deleted exam", current_user.id)
    return {"message": "Exam deleted successfully"}
