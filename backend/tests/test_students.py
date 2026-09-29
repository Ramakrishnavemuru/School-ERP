import pytest
import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def get_admin_token():
    res = client.post("/api/auth/login", json={"username": "admin", "password": "Password123!"})
    return res.json()["access_token"]

def get_student_token():
    res = client.post("/api/auth/login", json={"username": "student", "password": "Password123!"})
    return res.json()["access_token"]

def test_list_students_admin():
    token = get_admin_token()
    response = client.get("/api/students", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["total"] >= 2
    assert any(s["admission_number"] == "ADM2025001" for s in data["items"])

def test_create_student():
    token = get_admin_token()
    unique_suffix = uuid.uuid4().hex[:6]
    student_payload = {
        "username": f"test_student_{unique_suffix}",
        "email": f"student_{unique_suffix}@schoolerp.com",
        "password": "Password123!",
        "full_name": f"Test Student {unique_suffix}",
        "phone": "+1-555-9999",
        "admission_number": f"ADM_{unique_suffix}",
        "roll_number": "999",
        "class_id": 1,
        "section_id": 1,
        "gender": "Other",
        "date_of_birth": "2010-01-01"
    }
    response = client.post("/api/students", json=student_payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    created = response.json()
    assert created["admission_number"] == f"ADM_{unique_suffix}"
    assert created["user"]["full_name"] == f"Test Student {unique_suffix}"

def test_student_access_control():
    admin_token = get_admin_token()
    student_token = get_student_token()

    # Get alice (id 1) and bob (id 2)
    students_res = client.get("/api/students", headers={"Authorization": f"Bearer {admin_token}"})
    items = students_res.json()["items"]
    alice = next(s for s in items if s["admission_number"] == "ADM2025001")
    bob = next(s for s in items if s["admission_number"] == "ADM2025002")

    # Alice accessing own record
    res_own = client.get(f"/api/students/{alice['id']}", headers={"Authorization": f"Bearer {student_token}"})
    assert res_own.status_code == 200

    # Alice accessing Bob's record directly -> should be forbidden (403)
    res_other = client.get(f"/api/students/{bob['id']}", headers={"Authorization": f"Bearer {student_token}"})
    assert res_other.status_code == 403
