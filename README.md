# School/College ERP System

A production-ready, full-stack, role-based Enterprise Resource Planning (ERP) platform for managing educational institutions (schools and colleges). Built with pure web standards (HTML5/Vanilla JavaScript/Bootstrap 5) on the frontend and an asynchronous Python/FastAPI/SQLAlchemy/SQLite backend.

---

## 1. Project Description
The School/College ERP streamlines administrative operations, academic schedules, student enrollments, faculty workloads, grading, tuition management, attendance tracking, and communications. The platform enforces strict role-based access control (RBAC) across five user roles: **Admin**, **Principal**, **Teacher**, **Student**, and **Parent**, ensuring data isolation, compliance, and multi-tenant security.

---

## 2. Features

### Role-Based Portals:
- **Admin Portal (16 Views):** System overview dashboard, user accounts management, student registration, faculty directory, guardian linking, departments, academic years, classes, sections, subjects, timetable scheduling, tuition fee structures & payment collection, broadcast circulars, reports & analytics, security audit trail, system settings.
- **Principal Portal (9 Views):** Executive dashboard, student records, faculty overview, institution-wide attendance breakdown, grade curves & academic performance, leave request review/approvals, grievance investigation & resolution, official notice publication, executive reports.
- **Teacher Portal (12 Views):** Instructor dashboard, assigned classes & subjects, class rosters, weekly instructional timetable, daily student attendance marking, assignment creation & prompt attachments, student submission review & grading with feedback, study material uploads, exam scheduling, exam marks entry, leave application, faculty profile.
- **Student Portal (14 Views):** Student dashboard, class timetable, presence attendance record & percentage, coursework & homework submissions, assignment details with file upload, study material downloads, upcoming exam schedule, published report cards & grades, tuition fee balances & payment history, official announcements, campus calendar events, absence leave applications, document & certificate repository, profile management.
- **Parent Portal (12 Views):** Multi-child guardian dashboard, linked children directory, child profile view, child attendance history, homework tracking, published exam report cards, tuition fee ledger & balances, school notices, calendar events, guardian leave requests, internal staff messaging, guardian identification documents.

### Academic & Enterprise Modules:
- **Daily Attendance:** Bulk class attendance marking (Present, Absent, Late) with automatic percentage calculations and Chart.js visualizations.
- **Assignments & Coursework:** File attachment uploads, student solution submissions, grading workflows, and instructor feedback.
- **Examinations & Grading:** Standardized assessments, grade calculation, and instant result publishing.
- **Tuition & Finance:** Fee structures, payment recording with transaction IDs, ledger balance tracking.
- **Communications & Alerts:** Broadcast notices, in-app notification center with unread badges, and internal peer messaging.
- **Grievance Resolution:** Structured complaint submission and resolution lifecycle.
- **Security & Auditing:** Immutable audit logs capturing every administrative action, IP address, and timestamp.

---

## 3. Tech Stack

- **Frontend:**
  - HTML5 & CSS3
  - Vanilla JavaScript (ES6 Modules)
  - Bootstrap 5.3.3 (Modern Responsive UI)
  - Chart.js 4.4.1 (Interactive Visualizations)
- **Backend:**
  - Python 3.10+
  - FastAPI (High-performance ASGI framework)
  - Uvicorn (ASGI HTTP Server)
  - Pydantic v2 (Validation & Serialization)
- **Database & Storage:**
  - SQLite 3 (`backend/school_erp.db`)
  - SQLAlchemy 2.0 ORM
  - Local filesystem storage (`uploads/`) with UUID sanitization
- **Authentication & Security:**
  - JSON Web Tokens (JWT) with HTTP Bearer authorization
  - Passlib & Bcrypt password hashing
  - Server-side RBAC and resource ownership verification

---

## 4. Folder Structure

```text
school-college-erp/
├── backend/
│   ├── app/
│   │   ├── models/         # 29 SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic v2 validation schemas
│   │   ├── routes/         # 28 REST API route controllers
│   │   ├── services/       # Domain business services
│   │   ├── utils/          # Security, permissions, pagination, validators
│   │   ├── seed/           # Demo database initialization scripts
│   │   ├── config.py       # Pydantic settings & environment configuration
│   │   ├── database.py     # SQLite engine, sessions, init_db()
│   │   └── main.py         # FastAPI application entrypoint & static mounts
│   ├── tests/              # Pytest automated test suite
│   └── school_erp.db       # Relational SQLite database
├── frontend/
│   ├── admin/              # Admin HTML views (16 pages)
│   ├── principal/          # Principal HTML views (9 pages)
│   ├── teacher/            # Teacher HTML views (12 pages)
│   ├── student/            # Student HTML views (14 pages)
│   ├── parent/             # Parent HTML views (12 pages)
│   ├── components/         # Reusable layouts, modals, alerts
│   ├── css/                # Custom stylesheets & Bootstrap CSS
│   ├── js/                 # Domain controllers, API client, auth & RBAC
│   ├── index.html          # Entry redirector
│   ├── login.html          # Authentication page with 1-click demo logins
│   └── forgot-password.html
├── uploads/
│   ├── profiles/           # User avatar images
│   ├── assignments/        # Instructor problem prompts & student work
│   ├── study-materials/    # Lecture notes, syllabus slides
│   ├── documents/          # Certificates, verification records
│   └── reports/            # Exported files
├── docs/                   # Architecture, API, database, setup, & RBAC docs
├── requirements.txt        # Python package dependencies
├── pytest.ini              # Pytest configuration
├── .env.example            # Environment variables template
└── README.md
```

---

## 5. Installation & Setup

### 5.1 Clone or Navigate to Project
```bash
cd school-college-erp
```

### 5.2 Virtual Environment Setup
Create and activate a clean Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 5.4 Environment Configuration
```bash
cp .env.example .env
```

---

## 6. Database Initialization & Seed Data

The database tables are automatically verified and created when the FastAPI server boots.
To populate the database with comprehensive demonstration data (classes, faculty, students, attendance, grades, and fees):
```bash
python3 -m backend.app.seed.seed_database
```

---

## 7. Running the Server

Start the local server using Uvicorn:
```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Open your browser:
- **Application Portal:** [http://127.0.0.1:8000](http://127.0.0.1:8000) (auto-redirects to `/frontend/login.html`)
- **Interactive Swagger API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc API Documentation:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 8. Automated Testing

Run the test suite using `pytest`:
```bash
pytest
```
All 18 unit tests for authentication, role authorization, student management, attendance, assignments, and results will execute and pass.

---

## 9. Demo Credentials

All demonstration accounts share the default development password: **`Password123!`**

| Role | Username | Password | Features Accessible |
|---|---|---|---|
| **ADMIN** | `admin` | `Password123!` | Full system administration, user accounts, fee management, audit logs |
| **PRINCIPAL** | `principal` | `Password123!` | Executive oversight, grievance review, leave approvals, institutional analytics |
| **TEACHER** | `teacher` | `Password123!` | Classroom attendance, coursework assignments, student evaluation, marks entry |
| **STUDENT** | `student` | `Password123!` | Class timetable, attendance statistics, assignment submissions, report cards |
| **PARENT** | `parent` | `Password123!` | Multi-child oversight, child attendance, fee payments, teacher messaging |

*Note: The login page at `/frontend/login.html` features one-click buttons to instantly fill in any of the demo credentials.*
