# School/College ERP - Architecture & Technical Specification

## 1. Architectural Philosophy
The School/College ERP system is implemented as a **Modular Monolith** designed for high maintainability, rapid deployment, and minimal operational overhead.

### Key Architectural Tenets:
- **Zero-Microservices Simplicity:** All business domains (Academics, Finance, Attendance, Examination, Grievance, Auditing) operate within a single, highly cohesive FastAPI codebase with clear domain isolation.
- **Pure Web Standards Frontend:** Standard HTML5, CSS3, and Vanilla ECMAScript (ES6+) styled with Bootstrap 5 and visual charts via Chart.js. Eliminates heavy node_modules build dependencies, Webpack/Vite bundlers, and frontend state synchronization complexity.
- **Stateless RESTful APIs with Stateful Relational Storage:** The backend provides REST endpoints secured via HTTP Bearer JSON Web Tokens (JWT). SQLite via SQLAlchemy ORM powers structured, transactional ACID guarantees.
- **Server-Side Security Enforcement:** All business rules, role-based access control (RBAC), file upload constraints, and resource ownership validations are executed server-side.

---

## 2. Technology Stack

| Layer | Component | Technology / Library | Purpose |
|---|---|---|---|
| **Frontend UI** | Markup & Structure | HTML5 | Semantic structure for 50+ role-based views |
| | Styling & Grid | Bootstrap 5.3.3 + Custom CSS | Responsive layout across mobile, tablet, and desktop |
| | Dynamics & Logic | Vanilla JavaScript (ES6 Modules) | Client-side DOM controllers, API fetch client, state |
| | Data Visualizations | Chart.js 4.4.1 | Attendance breakdowns, grade curves, revenue charts |
| **Backend API** | Web Framework | FastAPI (Python 3.10+) | High-performance async ASGI application |
| | ASGI Server | Uvicorn | Production-ready HTTP/1.1 and WebSocket server |
| | Data Validation | Pydantic v2 | Request/Response schema validation and serialization |
| | Security & Hashing | Passlib + Bcrypt + Python-JOSE | JWT access tokens and salted password encryption |
| **Data Layer** | ORM | SQLAlchemy 2.0 | Object Relational Mapping & query abstractions |
| | Database Engine | SQLite 3 | Embedded transactional ACID database (`backend/school_erp.db`) |
| **Storage** | File System | Local File Storage | Categorized storage in `uploads/` with safe UUID hashing |

---

## 3. High-Level System Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                  CLIENT LAYER                                     |
|                                                                                   |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  |   Admin Portal     |   |   Principal Portal    |   |    Teacher Portal      |  |
|  | (/frontend/admin/) |   | (/frontend/principal/)|   |  (/frontend/teacher/)  |  |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  |   Student Portal   |   |     Parent Portal     |   |     Public / Auth      |  |
|  |(/frontend/student/)|   |  (/frontend/parent/)  |   | (/frontend/login.html) |  |
|  +--------------------+   +-----------------------+   +------------------------+  |
|                                     |                                             |
|                     HTTP / HTTPS (JSON REST + Bearer JWT)                         |
+-------------------------------------|---------------------------------------------+
                                      v
+-----------------------------------------------------------------------------------+
|                                 APPLICATION LAYER                                 |
|                                                                                   |
|   FastAPI Main Application (`backend/app/main.py`)                                 |
|   +---------------------------------------------------------------------------+   |
|   | Global Middleware: CORS (Cross-Origin), Request Logging, Error Handlers    |   |
|   +---------------------------------------------------------------------------+   |
|   | Security & Auth: JWT Bearer Token Extraction, RBAC Permissions Guard      |   |
|   +---------------------------------------------------------------------------+   |
|   | REST API Routers (28 Routers):                                            |   |
|   |  - /api/auth             - /api/users          - /api/students            |   |
|   |  - /api/teachers         - /api/parents        - /api/departments         |   |
|   |  - /api/classes          - /api/subjects       - /api/timetable           |   |
|   |  - /api/attendance       - /api/leave          - /api/assignments         |   |
|   |  - /api/materials        - /api/exams          - /api/results             |   |
|   |  - /api/fees             - /api/notices        - /api/notifications       |   |
|   |  - /api/events           - /api/messages       - /api/complaints          |   |
|   |  - /api/documents        - /api/reports        - /api/dashboard           |   |
|   +---------------------------------------------------------------------------+   |
|   | Service Layer:                                                            |   |
|   |  - AuthService   - FileService         - AttendanceService - FeeService   |   |
|   |  - ExamService   - NotificationService - ReportService                    |   |
|   +---------------------------------------------------------------------------+   |
|                                     |                                             |
+-------------------------------------|---------------------------------------------+
                                      v
+-----------------------------------------------------------------------------------+
|                                PERSISTENCE LAYER                                  |
|                                                                                   |
|  +-------------------------------------+   +-----------------------------------+  |
|  |       SQLAlchemy ORM (29 Models)    |   |      Local File System Storage    |  |
|  |  SQLite Database: school_erp.db     |   |  - uploads/profiles/              |  |
|  |  - Foreign Key Pragmas Enabled      |   |  - uploads/assignments/           |  |
|  |  - Transactional ACID Operations    |   |  - uploads/study-materials/       |  |
|  |  - Indexed Lookups & Constraints    |   |  - uploads/documents/             |  |
|  +-------------------------------------+   +-----------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 4. Frontend Component & Script Architecture
The frontend architecture organizes modular JavaScript controllers matching the functional domain models:

- **`api.js`**: Unified asynchronous fetch wrapper. Automatically attaches `Authorization: Bearer <token>` headers, formats multipart payloads, intercepts 401 Unauthenticated errors, and redirects to `/frontend/login.html`.
- **`auth.js`**: Token storage, login submission, credentials decoding, user profile extraction, and logout teardown.
- **`permissions.js`**: Client-side route protection guard `permissions.enforcePageAccess(['ROLE'])`.
- **`components.js`**: Dynamic layout renderer. Injects responsive sidebar navigation matching the user's role, updates notification bell dropdowns, and generates pagination footers.
- **`utils.js`**: Formatting tools for timestamps, currencies, letter grades, status badges, and debounce helpers.
- **Domain Controllers (`students.js`, `teachers.js`, `attendance.js`, `assignments.js`, `exams.js`, `results.js`, `fees.js`, `reports.js`, `messages.js`, `notifications.js`)**: Encapsulate CRUD logic, modal toggling, and data binding for each specific domain.

---

## 5. Security & File Upload Pipeline
1. **Filename Sanitization:** Uploaded files are renamed using cryptographic UUIDs with preserved valid extensions to prevent path traversal attacks (`../../etc/passwd`).
2. **Extension Whitelisting:** Strictly validates against permitted formats (`pdf`, `doc`, `docx`, `txt`, `png`, `jpg`, `jpeg`, `zip`, `csv`, `xlsx`).
3. **File Size Enforcement:** Uploads exceeding `MAX_UPLOAD_SIZE_MB` (default 10 MB) are rejected before memory saturation.
4. **Authenticated Download Gateway:** Files located in `uploads/` are never served as unprotected static files. The `/api/documents/file/{path}` endpoint enforces bearer token authentication and user verification before streaming files.
