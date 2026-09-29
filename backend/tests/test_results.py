import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def get_teacher_token():
    res = client.post("/api/auth/login", json={"username": "teacher", "password": "Password123!"})
    return res.json()["access_token"]

def get_student_token():
    res = client.post("/api/auth/login", json={"username": "student", "password": "Password123!"})
    return res.json()["access_token"]

def test_record_results_and_grade_calc():
    teacher_token = get_teacher_token()
    payload = {
        "exam_id": 1,
        "student_id": 1,
        "subject_id": 3,  # English
        "marks_obtained": 91.0,
        "max_marks": 100.0,
        "remarks": "Excellent essay writing"
    }
    response = client.post("/api/results", json=payload, headers={"Authorization": f"Bearer {teacher_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["marks_obtained"] == 91.0
    assert data["grade"] == "A+"
    assert data["percentage"] == 91.0

def test_student_report_card():
    student_token = get_student_token()
    response = client.get("/api/results/report-card?exam_id=1&student_id=1", headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["student_name"] == "Alice Smith"
    assert data["exam_name"] == "Term 1 Mid-Session Examination"
    assert len(data["results"]) >= 2
    assert "total_obtained" in data
    assert "grade" in data

def test_student_cannot_modify_results():
    student_token = get_student_token()
    response = client.post(
        "/api/results",
        json={"exam_id": 1, "student_id": 1, "subject_id": 1, "marks_obtained": 100.0, "max_marks": 100.0},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 403
