def test_user_registration_and_login(client):
    res = client.post("/api/auth/register", json={
        "name": "Test Student",
        "email": "student_test@cloud.edu",
        "password": "securepassword",
        "role": "student"
    })
    assert res.status_code == 201
    assert res.json()["email"] == "student_test@cloud.edu"

    login_res = client.post("/api/auth/login", json={
        "email": "student_test@cloud.edu",
        "password": "securepassword"
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()
