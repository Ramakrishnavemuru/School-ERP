# Database Schema & Relational Specifications

## 1. Overview
The database engine is **SQLite 3**, configured with foreign key enforcement pragmas (`PRAGMA foreign_keys=ON;`) and WAL (Write-Ahead Logging) journal mode for multi-reader concurrency.

Database file location:
`backend/school_erp.db`

The schema consists of **29 relational tables** modeled via SQLAlchemy ORM.

---

## 2. Core Entities & Relationships

### Identity & Access
1. **`roles`**:
   - `id` (INTEGER, PK)
   - `name` (VARCHAR, Unique, Indexed): `ADMIN`, `PRINCIPAL`, `TEACHER`, `STUDENT`, `PARENT`
   - `description` (TEXT)
   - `created_at` (DATETIME)

2. **`users`**:
   - `id` (INTEGER, PK)
   - `username` (VARCHAR, Unique, Indexed)
   - `email` (VARCHAR, Unique, Indexed)
   - `hashed_password` (VARCHAR)
   - `full_name` (VARCHAR)
   - `role` (VARCHAR, Indexed)
   - `phone` (VARCHAR, Nullable)
   - `avatar_url` (VARCHAR, Nullable)
   - `is_active` (BOOLEAN, Default True)
   - `created_at`, `updated_at` (DATETIME)

3. **`audit_logs`**:
   - `id` (INTEGER, PK)
   - `user_id` (INTEGER, FK -> `users.id`, Nullable)
   - `action` (VARCHAR, Indexed)
   - `entity` (VARCHAR, Indexed)
   - `entity_id` (VARCHAR, Nullable)
   - `details` (TEXT, Nullable)
   - `ip_address` (VARCHAR, Nullable)
   - `timestamp` (DATETIME, Indexed)

---

### Academic Infrastructure
4. **`academic_years`**:
   - `id` (INTEGER, PK)
   - `name` (VARCHAR, Unique)
   - `start_date` (DATE)
   - `end_date` (DATE)
   - `is_current` (BOOLEAN, Indexed)
   - `created_at` (DATETIME)

5. **`departments`**:
   - `id` (INTEGER, PK)
   - `name` (VARCHAR, Unique, Indexed)
   - `code` (VARCHAR, Unique, Indexed)
   - `description` (TEXT, Nullable)
   - `created_at` (DATETIME)

6. **`classes`**:
   - `id` (INTEGER, PK)
   - `name` (VARCHAR, Indexed)
   - `grade_level` (INTEGER, Indexed)
   - `department_id` (INTEGER, FK -> `departments.id`, Nullable)
   - `academic_year_id` (INTEGER, FK -> `academic_years.id`, Nullable)
   - `created_at` (DATETIME)

7. **`sections`**:
   - `id` (INTEGER, PK)
   - `name` (VARCHAR)
   - `class_id` (INTEGER, FK -> `classes.id`, Indexed)
   - `room_number` (VARCHAR, Nullable)
   - `class_teacher_id` (INTEGER, FK -> `teachers.id`, Nullable)
   - `created_at` (DATETIME)

8. **`subjects`**:
   - `id` (INTEGER, PK)
   - `name` (VARCHAR, Indexed)
   - `code` (VARCHAR, Indexed)
   - `class_id` (INTEGER, FK -> `classes.id`, Indexed)
   - `teacher_id` (INTEGER, FK -> `teachers.id`, Nullable)
   - `created_at` (DATETIME)

9. **`timetables`**:
   - `id` (INTEGER, PK)
   - `class_id` (INTEGER, FK -> `classes.id`, Indexed)
   - `section_id` (INTEGER, FK -> `sections.id`, Nullable)
   - `subject_id` (INTEGER, FK -> `subjects.id`, Indexed)
   - `teacher_id` (INTEGER, FK -> `teachers.id`, Indexed)
   - `day_of_week` (VARCHAR, Indexed)
   - `start_time` (VARCHAR)
   - `end_time` (VARCHAR)
   - `room_number` (VARCHAR, Nullable)
   - `created_at` (DATETIME)

---

### Role Profiles
10. **`principals`**:
    - `id` (INTEGER, PK)
    - `user_id` (INTEGER, FK -> `users.id`, Unique)
    - `qualification` (VARCHAR, Nullable)
    - `joining_date` (DATE, Nullable)

11. **`teachers`**:
    - `id` (INTEGER, PK)
    - `user_id` (INTEGER, FK -> `users.id`, Unique)
    - `employee_id` (VARCHAR, Unique, Indexed)
    - `department_id` (INTEGER, FK -> `departments.id`, Nullable)
    - `qualification` (VARCHAR, Nullable)
    - `designation` (VARCHAR, Default 'Teacher')
    - `phone` (VARCHAR, Nullable)
    - `address` (TEXT, Nullable)
    - `joining_date` (DATE, Nullable)

12. **`parents`**:
    - `id` (INTEGER, PK)
    - `user_id` (INTEGER, FK -> `users.id`, Unique)
    - `occupation` (VARCHAR, Nullable)
    - `relation_type` (VARCHAR, Default 'Guardian')
    - `emergency_contact` (VARCHAR, Nullable)
    - `address` (TEXT, Nullable)

13. **`students`**:
    - `id` (INTEGER, PK)
    - `user_id` (INTEGER, FK -> `users.id`, Unique)
    - `admission_number` (VARCHAR, Unique, Indexed)
    - `roll_number` (VARCHAR, Nullable, Indexed)
    - `class_id` (INTEGER, FK -> `classes.id`, Nullable, Indexed)
    - `section_id` (INTEGER, FK -> `sections.id`, Nullable, Indexed)
    - `parent_id` (INTEGER, FK -> `parents.id`, Nullable, Indexed)
    - `date_of_birth` (DATE, Nullable)
    - `gender` (VARCHAR, Nullable)
    - `blood_group` (VARCHAR, Nullable)
    - `admission_date` (DATE, Nullable)
    - `address` (TEXT, Nullable)

14. **`enrollments`**:
    - `id` (INTEGER, PK)
    - `student_id` (INTEGER, FK -> `students.id`)
    - `class_id` (INTEGER, FK -> `classes.id`)
    - `academic_year_id` (INTEGER, FK -> `academic_years.id`)
    - `status` (VARCHAR, Default 'Active')

---

### Academics, Assessments & Coursework
15. **`attendances`**:
    - `id` (INTEGER, PK)
    - `student_id` (INTEGER, FK -> `students.id`, Indexed)
    - `class_id` (INTEGER, FK -> `classes.id`, Indexed)
    - `section_id` (INTEGER, FK -> `sections.id`, Indexed)
    - `date` (DATE, Indexed)
    - `status` (VARCHAR, Indexed): `Present`, `Absent`, `Late`, `Excused`
    - `remarks` (TEXT, Nullable)
    - *Constraint*: Unique index on `(student_id, date)` prevents duplicate records.

16. **`assignments`**:
    - `id` (INTEGER, PK)
    - `title` (VARCHAR)
    - `description` (TEXT, Nullable)
    - `class_id` (INTEGER, FK -> `classes.id`, Indexed)
    - `section_id` (INTEGER, FK -> `sections.id`, Nullable)
    - `subject_id` (INTEGER, FK -> `subjects.id`, Indexed)
    - `teacher_id` (INTEGER, FK -> `teachers.id`, Indexed)
    - `due_date` (DATETIME, Indexed)
    - `max_marks` (FLOAT, Default 100.0)
    - `attachment_path` (VARCHAR, Nullable)
    - `created_at` (DATETIME)

17. **`submissions`**:
    - `id` (INTEGER, PK)
    - `assignment_id` (INTEGER, FK -> `assignments.id`, Indexed)
    - `student_id` (INTEGER, FK -> `students.id`, Indexed)
    - `submission_date` (DATETIME)
    - `file_path` (VARCHAR)
    - `marks_obtained` (FLOAT, Nullable)
    - `status` (VARCHAR, Default 'submitted'): `submitted`, `graded`, `late`
    - `feedback` (TEXT, Nullable)

18. **`study_materials`**:
    - `id` (INTEGER, PK)
    - `title` (VARCHAR)
    - `description` (TEXT, Nullable)
    - `class_id` (INTEGER, FK -> `classes.id`, Indexed)
    - `subject_id` (INTEGER, FK -> `subjects.id`, Indexed)
    - `teacher_id` (INTEGER, FK -> `teachers.id`, Indexed)
    - `file_path` (VARCHAR)
    - `file_type` (VARCHAR, Nullable)
    - `file_size` (INTEGER, Nullable)
    - `upload_date` (DATETIME)

19. **`exams`**:
    - `id` (INTEGER, PK)
    - `name` (VARCHAR, Indexed)
    - `exam_type` (VARCHAR): `Unit Test`, `Mid-Term`, `Final`, `Practical`
    - `class_id` (INTEGER, FK -> `classes.id`, Nullable, Indexed)
    - `academic_year_id` (INTEGER, FK -> `academic_years.id`, Nullable)
    - `start_date` (DATE)
    - `end_date` (DATE)
    - `is_published` (BOOLEAN, Default False, Indexed)

20. **`results`**:
    - `id` (INTEGER, PK)
    - `exam_id` (INTEGER, FK -> `exams.id`, Indexed)
    - `student_id` (INTEGER, FK -> `students.id`, Indexed)
    - `subject_id` (INTEGER, FK -> `subjects.id`, Indexed)
    - `marks_obtained` (FLOAT)
    - `max_marks` (FLOAT, Default 100.0)
    - `grade` (VARCHAR, Nullable)
    - `remarks` (TEXT, Nullable)
    - *Constraint*: Unique index on `(exam_id, student_id, subject_id)`.

---

### Finance & Tuition
21. **`fees`**:
    - `id` (INTEGER, PK)
    - `title` (VARCHAR)
    - `fee_type` (VARCHAR): `Tuition`, `Admission`, `Exam`, `Library`, `Transport`, `Hostel`, `Other`
    - `class_id` (INTEGER, FK -> `classes.id`, Nullable)
    - `academic_year_id` (INTEGER, FK -> `academic_years.id`, Nullable)
    - `amount` (FLOAT)
    - `due_date` (DATE, Indexed)
    - `description` (TEXT, Nullable)

22. **`payments`**:
    - `id` (INTEGER, PK)
    - `fee_id` (INTEGER, FK -> `fees.id`, Indexed)
    - `student_id` (INTEGER, FK -> `students.id`, Indexed)
    - `amount_paid` (FLOAT)
    - `payment_date` (DATE, Indexed)
    - `payment_method` (VARCHAR): `Cash`, `Online`, `Bank Transfer`, `Cheque`
    - `transaction_id` (VARCHAR, Nullable, Indexed)
    - `payment_status` (VARCHAR, Default 'PAID'): `PAID`, `PENDING`, `FAILED`
    - `remarks` (TEXT, Nullable)

---

### Communications, Grievances & Administration
23. **`notices`**:
    - `id` (INTEGER, PK)
    - `title` (VARCHAR)
    - `content` (TEXT)
    - `target_role` (VARCHAR, Indexed): `ALL`, `TEACHER`, `STUDENT`, `PARENT`
    - `published_by` (INTEGER, FK -> `users.id`)
    - `is_published` (BOOLEAN, Default True, Indexed)
    - `publish_date` (DATETIME, Indexed)
    - `expires_at` (DATE, Nullable)

24. **`notifications`**:
    - `id` (INTEGER, PK)
    - `user_id` (INTEGER, FK -> `users.id`, Indexed)
    - `title` (VARCHAR)
    - `message` (TEXT)
    - `link` (VARCHAR, Nullable)
    - `notification_type` (VARCHAR, Default 'INFO')
    - `is_read` (BOOLEAN, Default False, Indexed)
    - `created_at` (DATETIME, Indexed)

25. **`events`**:
    - `id` (INTEGER, PK)
    - `title` (VARCHAR)
    - `description` (TEXT, Nullable)
    - `start_time` (DATETIME, Indexed)
    - `end_time` (DATETIME)
    - `location` (VARCHAR, Nullable)
    - `target_audience` (VARCHAR, Default 'ALL')
    - `created_by` (INTEGER, FK -> `users.id`)

26. **`messages`**:
    - `id` (INTEGER, PK)
    - `sender_id` (INTEGER, FK -> `users.id`, Indexed)
    - `receiver_id` (INTEGER, FK -> `users.id`, Indexed)
    - `subject` (VARCHAR)
    - `body` (TEXT)
    - `is_read` (BOOLEAN, Default False, Indexed)
    - `sent_at` (DATETIME, Indexed)

27. **`leaves`**:
    - `id` (INTEGER, PK)
    - `user_id` (INTEGER, FK -> `users.id`, Indexed)
    - `applicant_role` (VARCHAR)
    - `leave_type` (VARCHAR)
    - `start_date` (DATE)
    - `end_date` (DATE)
    - `reason` (TEXT)
    - `status` (VARCHAR, Default 'PENDING', Indexed): `PENDING`, `APPROVED`, `REJECTED`
    - `reviewed_by` (INTEGER, FK -> `users.id`, Nullable)
    - `remarks` (TEXT, Nullable)

28. **`complaints`**:
    - `id` (INTEGER, PK)
    - `user_id` (INTEGER, FK -> `users.id`, Indexed)
    - `title` (VARCHAR)
    - `description` (TEXT)
    - `status` (VARCHAR, Default 'PENDING', Indexed): `PENDING`, `IN_REVIEW`, `RESOLVED`, `REJECTED`
    - `resolved_by` (INTEGER, FK -> `users.id`, Nullable)
    - `resolution` (TEXT, Nullable)

29. **`documents`**:
    - `id` (INTEGER, PK)
    - `user_id` (INTEGER, FK -> `users.id`, Indexed)
    - `title` (VARCHAR)
    - `file_path` (VARCHAR)
    - `document_type` (VARCHAR, Default 'General')
    - `file_size` (INTEGER, Nullable)
    - `created_at` (DATETIME)
