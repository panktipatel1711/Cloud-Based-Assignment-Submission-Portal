import io
from datetime import datetime, timedelta

def test_full_assignment_lifecycle(client):
    client.post("/api/auth/register", json={
        "name": "Prof Smith", "email": "smith_test@cloud.edu", "password": "pass", "role": "teacher"
    })
    t_login = client.post("/api/auth/login", json={"email": "smith_test@cloud.edu", "password": "pass"}).json()
    t_headers = {"Authorization": f"Bearer {t_login['access_token']}"}

    deadline = (datetime.utcnow() + timedelta(days=2)).isoformat()
    assign_res = client.post("/api/assignments", json={
        "course_id": 1,
        "title": "Cloud Computing Lab 1",
        "description": "Upload lab report",
        "deadline": deadline,
        "max_marks": 100.0
    }, headers=t_headers)
    assert assign_res.status_code == 201
    assign_id = assign_res.json()["assignment_id"]

    client.post("/api/auth/register", json={
        "name": "Bob Student", "email": "bob_test@cloud.edu", "password": "pass", "role": "student"
    })
    s_login = client.post("/api/auth/login", json={"email": "bob_test@cloud.edu", "password": "pass"}).json()
    s_headers = {"Authorization": f"Bearer {s_login['access_token']}"}

    file_payload = {"file": ("lab_report.pdf", io.BytesIO(b"%PDF-1.4 Mock Assignment Blob"), "application/pdf")}
    sub_res = client.post(f"/api/assignments/{assign_id}/submit", files=file_payload, headers=s_headers)
    assert sub_res.status_code == 201
    sub_id = sub_res.json()["submission_id"]
    assert sub_res.json()["status"] == "SUBMITTED"

    grade_res = client.post(f"/api/submissions/{sub_id}/grade", json={
        "marks": 96.0,
        "feedback": "Decoupled cloud architecture works as expected."
    }, headers=t_headers)
    assert grade_res.status_code == 200
    assert grade_res.json()["status"] == "GRADED"
