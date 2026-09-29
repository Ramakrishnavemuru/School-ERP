# REST API Documentation & Endpoint Reference

## 1. Authentication & Protocols
All protected endpoints require the HTTP Bearer Authentication scheme:
```http
Authorization: Bearer <access_token>
```
All API responses use standard JSON payloads and HTTP status codes:
- `200 OK`: Successful retrieval or update.
- `201 Created`: Successful resource creation.
- `400 Bad Request`: Validation failure or semantic conflict.
- `401 Unauthorized`: Invalid or expired JWT token.
- `403 Forbidden`: Insufficient role permissions or resource ownership check failed.
- `404 Not Found`: Target resource does not exist.
- `422 Unprocessable Entity`: Request body failed Pydantic schema validation.

---

## 2. API Endpoints Catalog

### Authentication (`/api/auth`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/auth/login` | Public | Authenticate username/password; returns JWT bearer token & role |
| `GET` | `/api/auth/me` | Authenticated | Retrieve current user profile and role details |
| `POST` | `/api/auth/change-password` | Authenticated | Change user account password |
| `POST` | `/api/auth/logout` | Authenticated | Logout signal and audit logging |

---

### Administration & User Management (`/api/admin`, `/api/users`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/admin/overview` | `ADMIN` | High-level statistics, counters, and recent activity logs |
| `GET` | `/api/admin/audit-logs` | `ADMIN` | Immutable security audit trail with action/entity filters |
| `GET` | `/api/admin/settings` | `ADMIN` | System environment configuration and parameters |
| `GET` | `/api/users` | `ADMIN` | Paginated search of all user accounts across roles |
| `POST` | `/api/users` | `ADMIN` | Create administrative, faculty, or student accounts |
| `PATCH` | `/api/users/{id}/toggle-status` | `ADMIN` | Enable or disable user account access |
| `DELETE` | `/api/users/{id}` | `ADMIN` | Delete user account and associated profile |

---

### Students & Admissions (`/api/students`, `/api/student`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/students` | `ADMIN`, `PRINCIPAL`, `TEACHER` | Paginated student directory with class, section, search filters |
| `POST` | `/api/students` | `ADMIN` | Register student, create login, and establish class enrollment |
| `GET` | `/api/students/{id}` | Staff & Guardian | View comprehensive student academic, attendance, and fee summary |
| `DELETE` | `/api/students/{id}` | `ADMIN` | Delete student record |
| `GET` | `/api/student/dashboard` | `STUDENT` | Student dashboard summary (presence, balance, assignments, grades) |
| `GET` | `/api/student/profile` | `STUDENT` | Retrieve student personal record |
| `PUT` | `/api/student/profile` | `STUDENT` | Update permitted contact information (phone, address) |
| `GET` | `/api/student/timetable` | `STUDENT` | Class timetable schedule |
| `GET` | `/api/student/attendance` | `STUDENT` | Presence statistics and chronological attendance records |
| `GET` | `/api/student/assignments` | `STUDENT` | Class assignments and submission status |
| `GET` | `/api/student/results` | `STUDENT` | Published exam report cards and letter grades |
| `GET` | `/api/student/fees` | `STUDENT` | Assigned tuition dues and payment records |
| `GET` | `/api/student/study-materials` | `STUDENT` | Downloadable class syllabus materials |

---

### Faculty & Teachers (`/api/teachers`, `/api/teacher`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/teachers` | `ADMIN`, `PRINCIPAL` | Directory of instructors and department assignments |
| `POST` | `/api/teachers` | `ADMIN` | Register new faculty member |
| `GET` | `/api/teachers/{id}` | `ADMIN`, `PRINCIPAL` | Faculty profile, qualifications, and taught subjects |
| `DELETE` | `/api/teachers/{id}` | `ADMIN` | Delete faculty account |
| `GET` | `/api/teacher/profile` | `TEACHER` | Current instructor profile details |
| `GET` | `/api/teacher/classes` | `TEACHER` | Assigned classes, sections, and teaching subjects |
| `GET` | `/api/teacher/students` | `TEACHER` | Student roster scoped to instructor's assigned classes |
| `GET` | `/api/teacher/timetable` | `TEACHER` | Weekly instructional schedule |
| `GET` | `/api/teacher/submissions` | `TEACHER` | Student assignment submissions awaiting evaluation |

---

### Parents & Guardians (`/api/parents`, `/api/parent`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/parents` | `ADMIN`, `PRINCIPAL` | Directory of registered guardians and child links |
| `POST` | `/api/parents` | `ADMIN` | Register new parent account |
| `POST` | `/api/parents/{id}/link-student/{student_id}` | `ADMIN` | Establish child guardianship link |
| `DELETE` | `/api/parents/{id}` | `ADMIN` | Delete parent account |
| `GET` | `/api/parent/children` | `PARENT` | Retrieve list of verified linked children |
| `GET` | `/api/parent/child/{child_id}/profile` | `PARENT` | Scoped child profile |
| `GET` | `/api/parent/child/{child_id}/attendance`| `PARENT` | Child presence percentage and log |
| `GET` | `/api/parent/child/{child_id}/results` | `PARENT` | Child published report card |
| `GET` | `/api/parent/child/{child_id}/fees` | `PARENT` | Child fee balances and dues |
| `GET` | `/api/parent/child/{child_id}/assignments`| `PARENT` | Child coursework and homework status |

---

### Academic Infrastructure (`/api/departments`, `/api/classes`, `/api/subjects`, `/api/timetable`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/departments` | Authenticated | List all departments |
| `POST` | `/api/departments` | `ADMIN` | Create new department |
| `DELETE`| `/api/departments/{id}` | `ADMIN` | Remove department |
| `GET` | `/api/classes` | Authenticated | List all classes with sections and departments |
| `POST` | `/api/classes` | `ADMIN` | Create academic class / grade tier |
| `DELETE`| `/api/classes/{id}` | `ADMIN` | Delete class |
| `GET` | `/api/classes/academic-years` | Authenticated | List academic sessions |
| `POST` | `/api/classes/academic-years` | `ADMIN` | Add new academic session |
| `PATCH` | `/api/classes/academic-years/{id}/set-current` | `ADMIN` | Activate session |
| `GET` | `/api/classes/{id}/sections` | Authenticated | List class sections |
| `POST` | `/api/classes/{id}/sections` | `ADMIN` | Create section in class |
| `DELETE`| `/api/classes/sections/{id}` | `ADMIN` | Delete section |
| `GET` | `/api/subjects` | Authenticated | List curriculum subjects |
| `POST` | `/api/subjects` | `ADMIN` | Create subject and assign instructor |
| `DELETE`| `/api/subjects/{id}` | `ADMIN` | Delete subject |
| `GET` | `/api/timetable` | Authenticated | Filterable timetable periods |
| `POST` | `/api/timetable` | `ADMIN` | Schedule class lecture period |
| `DELETE`| `/api/timetable/{id}` | `ADMIN` | Remove period |

---

### Attendance (`/api/attendance`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/attendance` | Authenticated | Query attendance records by class, section, date |
| `POST` | `/api/attendance` | `TEACHER`, `ADMIN` | Bulk submit daily classroom attendance |
| `GET` | `/api/attendance/student/{id}` | Staff, Self, Guardian | Retrieve individual attendance statistics |

---

### Assignments & Materials (`/api/assignments`, `/api/materials`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/assignments` | Staff & Students | List assignments |
| `POST` | `/api/assignments` | `TEACHER`, `ADMIN` | Create assignment with optional file attachment |
| `DELETE`| `/api/assignments/{id}` | `TEACHER`, `ADMIN` | Delete assignment |
| `POST` | `/api/assignments/{id}/submit`| `STUDENT` | Upload completed solution file |
| `GET` | `/api/assignments/{id}/submissions` | `TEACHER`, `ADMIN` | List student submissions |
| `PUT` | `/api/assignments/submissions/{id}/grade`| `TEACHER`, `ADMIN` | Evaluate submission and assign marks |
| `GET` | `/api/materials` | Authenticated | Query study materials |
| `POST` | `/api/materials` | `TEACHER`, `ADMIN` | Upload syllabus notes / documents |
| `DELETE`| `/api/materials/{id}` | `TEACHER`, `ADMIN` | Delete study material |

---

### Examinations & Results (`/api/exams`, `/api/results`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/exams` | Authenticated | List scheduled examinations |
| `POST` | `/api/exams` | `TEACHER`, `ADMIN` | Schedule new examination |
| `PATCH` | `/api/exams/{id}/publish` | `TEACHER`, `ADMIN` | Publish exam results to students and parents |
| `DELETE`| `/api/exams/{id}` | `TEACHER`, `ADMIN` | Delete exam |
| `GET` | `/api/results` | Staff | Query marks by exam, class, subject |
| `POST` | `/api/results/bulk` | `TEACHER`, `ADMIN` | Bulk submit student marks |

---

### Tuition Fees & Payments (`/api/fees`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/fees` | Staff | List configured fee structures |
| `POST` | `/api/fees` | `ADMIN` | Create tuition fee structure |
| `DELETE`| `/api/fees/{id}` | `ADMIN` | Remove fee structure |
| `GET` | `/api/fees/payments` | `ADMIN` | Transactional payment logs |
| `POST` | `/api/fees/payments` | `ADMIN` | Record student payment transaction |

---

### Communications, Leaves, Complaints & Documents
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/api/notices` | Authenticated | Role-targeted official circulars |
| `POST` | `/api/notices` | `ADMIN`, `PRINCIPAL`| Broadcast new announcement notice |
| `DELETE`| `/api/notices/{id}` | `ADMIN`, `PRINCIPAL`| Delete notice |
| `GET` | `/api/events` | Authenticated | Academic and cultural calendar events |
| `POST` | `/api/events` | `ADMIN`, `PRINCIPAL`| Create calendar event |
| `GET` | `/api/messages/inbox` | Authenticated | User incoming messages |
| `GET` | `/api/messages/sent` | Authenticated | User sent messages |
| `POST` | `/api/messages` | Authenticated | Send internal message |
| `PATCH` | `/api/messages/{id}/read`| Authenticated | Mark message as read |
| `GET` | `/api/leave` | `ADMIN`, `PRINCIPAL`| Filterable staff/student leave applications |
| `GET` | `/api/leave/my` | Authenticated | User's submitted leave applications |
| `POST` | `/api/leave` | Authenticated | Submit leave application |
| `PATCH` | `/api/leave/{id}/review` | `ADMIN`, `PRINCIPAL`| Approve or reject leave request |
| `GET` | `/api/complaints` | `ADMIN`, `PRINCIPAL`| Filterable grievances |
| `POST` | `/api/complaints` | Authenticated | Submit grievance / complaint |
| `PATCH` | `/api/complaints/{id}/resolve`| `ADMIN`, `PRINCIPAL`| Resolve or dismiss complaint |
| `GET` | `/api/documents` | Authenticated | User's uploaded records |
| `POST` | `/api/documents` | Authenticated | Upload certificate or official document |
| `GET` | `/api/documents/file/{path}`| Authenticated | Secure file streaming download endpoint |
