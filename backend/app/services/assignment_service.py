from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from backend.app.models.assignment import Assignment
from backend.app.models.submission import Submission
from backend.app.models.student import Student
from backend.app.schemas.assignment import AssignmentCreate, AssignmentUpdate

class AssignmentService:
    @staticmethod
    def create_assignment(
        db: Session,
        teacher_id: int,
        assignment_in: AssignmentCreate,
        attachment_path: Optional[str] = None
    ) -> Assignment:
        assignment = Assignment(
            title=assignment_in.title,
            description=assignment_in.description,
            class_id=assignment_in.class_id,
            section_id=assignment_in.section_id,
            subject_id=assignment_in.subject_id,
            teacher_id=teacher_id,
            due_date=assignment_in.due_date,
            max_marks=assignment_in.max_marks,
            attachment_path=attachment_path
        )
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def submit_assignment(
        db: Session,
        assignment_id: int,
        student_id: int,
        file_path: str
    ) -> Submission:
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )

        now = datetime.now()
        sub_status = "late" if now > assignment.due_date else "submitted"

        submission = db.query(Submission).filter(
            Submission.assignment_id == assignment_id,
            Submission.student_id == student_id
        ).first()

        if submission:
            submission.file_path = file_path
            submission.submission_date = now
            submission.status = sub_status
        else:
            submission = Submission(
                assignment_id=assignment_id,
                student_id=student_id,
                file_path=file_path,
                submission_date=now,
                status=sub_status
            )
            db.add(submission)

        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def grade_submission(
        db: Session,
        submission_id: int,
        marks_obtained: float,
        feedback: Optional[str] = None
    ) -> Submission:
        sub = db.query(Submission).filter(Submission.id == submission_id).first()
        if not sub:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Submission not found"
            )
        sub.marks_obtained = marks_obtained
        sub.feedback = feedback
        sub.status = "graded"
        db.commit()
        db.refresh(sub)
        return sub

assignment_service = AssignmentService()
