from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.models.attendance import Attendance
from backend.app.models.student import Student
from backend.app.schemas.attendance import AttendanceRecord, AttendanceStats

class AttendanceService:
    @staticmethod
    def mark_attendance(
        db: Session,
        class_id: int,
        section_id: int,
        att_date: date,
        records: List[AttendanceRecord],
        recorded_by: Optional[int] = None
    ) -> List[Attendance]:
        saved_records = []
        for item in records:
            # Check if record already exists for this student and date
            existing = db.query(Attendance).filter(
                Attendance.student_id == item.student_id,
                Attendance.date == att_date
            ).first()

            if existing:
                existing.status = item.status
                existing.remarks = item.remarks
                existing.recorded_by = recorded_by
                existing.class_id = class_id
                existing.section_id = section_id
                saved_records.append(existing)
            else:
                att = Attendance(
                    student_id=item.student_id,
                    class_id=class_id,
                    section_id=section_id,
                    date=att_date,
                    status=item.status,
                    remarks=item.remarks,
                    recorded_by=recorded_by
                )
                db.add(att)
                saved_records.append(att)

        db.commit()
        for r in saved_records:
            db.refresh(r)
        return saved_records

    @staticmethod
    def get_student_stats(db: Session, student_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None) -> AttendanceStats:
        query = db.query(Attendance).filter(Attendance.student_id == student_id)
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        if end_date:
            query = query.filter(Attendance.date <= end_date)

        records = query.all()
        total_days = len(records)
        present_days = sum(1 for r in records if r.status.lower() == "present")
        absent_days = sum(1 for r in records if r.status.lower() == "absent")
        late_days = sum(1 for r in records if r.status.lower() == "late")
        excused_days = sum(1 for r in records if r.status.lower() == "excused")

        # In standard attendance, late can count towards present or half, but here percentage = (present + late) / total * 100
        effective_present = present_days + late_days
        percentage = round((effective_present / total_days * 100), 2) if total_days > 0 else 0.0

        return AttendanceStats(
            total_days=total_days,
            present_days=present_days,
            absent_days=absent_days,
            late_days=late_days,
            excused_days=excused_days,
            percentage=percentage
        )

attendance_service = AttendanceService()
