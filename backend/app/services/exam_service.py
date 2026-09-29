from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from backend.app.models.exam import Exam
from backend.app.models.result import Result
from backend.app.models.student import Student
from backend.app.schemas.result import ResultItem, StudentReportCard, ResultResponse
from backend.app.utils.helpers import calculate_grade, calculate_percentage

class ExamService:
    @staticmethod
    def record_results_bulk(
        db: Session,
        exam_id: int,
        subject_id: int,
        records: List[ResultItem]
    ) -> List[Result]:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found"
            )

        saved = []
        for rec in records:
            pct = calculate_percentage(rec.marks_obtained, rec.max_marks)
            grade = calculate_grade(pct)

            existing = db.query(Result).filter(
                Result.exam_id == exam_id,
                Result.student_id == rec.student_id,
                Result.subject_id == subject_id
            ).first()

            if existing:
                existing.marks_obtained = rec.marks_obtained
                existing.max_marks = rec.max_marks
                existing.grade = grade
                existing.remarks = rec.remarks
                saved.append(existing)
            else:
                res = Result(
                    exam_id=exam_id,
                    student_id=rec.student_id,
                    subject_id=subject_id,
                    marks_obtained=rec.marks_obtained,
                    max_marks=rec.max_marks,
                    grade=grade,
                    remarks=rec.remarks
                )
                db.add(res)
                saved.append(res)

        db.commit()
        for r in saved:
            db.refresh(r)
        return saved

    @staticmethod
    def get_student_report(db: Session, exam_id: int, student_id: int) -> StudentReportCard:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found"
            )

        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        results = db.query(Result).options(
            joinedload(Result.subject)
        ).filter(
            Result.exam_id == exam_id,
            Result.student_id == student_id
        ).all()

        total_obtained = sum(r.marks_obtained for r in results)
        total_max = sum(r.max_marks for r in results)
        pct = calculate_percentage(total_obtained, total_max) if total_max > 0 else 0.0
        overall_grade = calculate_grade(pct) if total_max > 0 else "N/A"

        result_responses = []
        for r in results:
            result_responses.append(ResultResponse(
                id=r.id,
                exam_id=r.exam_id,
                student_id=r.student_id,
                subject_id=r.subject_id,
                marks_obtained=r.marks_obtained,
                max_marks=r.max_marks,
                percentage=calculate_percentage(r.marks_obtained, r.max_marks),
                grade=r.grade,
                remarks=r.remarks,
                exam_name=exam.name,
                student_name=student.user.full_name if student.user else None,
                admission_number=student.admission_number,
                roll_number=student.roll_number,
                subject_name=r.subject.name if r.subject else None,
                created_at=r.created_at
            ))

        return StudentReportCard(
            exam_id=exam.id,
            exam_name=exam.name,
            student_id=student.id,
            student_name=student.user.full_name if student.user else "",
            admission_number=student.admission_number,
            class_name=student.class_obj.name if student.class_obj else None,
            section_name=student.section.name if student.section else None,
            results=result_responses,
            total_obtained=round(total_obtained, 2),
            total_max=round(total_max, 2),
            percentage=pct,
            grade=overall_grade
        )

exam_service = ExamService()
