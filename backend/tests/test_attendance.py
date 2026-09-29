import pytest
from datetime import date
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def get_teacher_token():
    res = client.post("/api/auth/login", json={"username": "teacher", "password": "Password123!"})
    return res.json()["access_token"]

def get_student_token():
    res = client.post("/api/auth/login", json={"username": "student", "password": "Password123!"})
    return res.json()["access_token"]

def test_mark_attendance_teacher():
    teacher_token = get_teacher_token()
    payload = {
        "class_id": 1,
        "section_id": 1,
        "date": "2025-10-15",
        "records": [
            {"student_id": 1, "status": "Present", "remarks": "Prompt"},
            {"student_id": 2, "status": "Late", "remarks": "Late bus"}
        ]
    }
    response = client.post("/api/attendance", json=payload, headers={"Authorization": f"Bearer {teacher_token}"})
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 2

def test_attendance_stats_calculation():
    student_token = get_student_token()
    response = client.get("/api/students/1/attendance", headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 200
    data = response.json()
    assert "stats" in data
    assert data["stats"]["total_days"] >= 1
    assert data["stats"]["percentage"] >= 0.0

def test_student_cannot_mark_attendance():
    student_token = get_student_token()
    payload = {
        "class_id": 1,
        "section_id": 1,
        "date": "2025-10-16",
        "records": [{"student_id": 1, "status": "Present"}]
    }
    response = client.post("/api/attendance", json=payload, headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 403
