import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_and_unregister():
    # Sign up a new student
    signup_resp = client.post("/activities/Chess Club/signup", params={"email": "teststudent@mergington.edu"})
    assert signup_resp.status_code == 200
    # Duplicate signup should fail
    dup_resp = client.post("/activities/Chess Club/signup", params={"email": "teststudent@mergington.edu"})
    assert dup_resp.status_code == 400
    # Unregister the student
    unregister_resp = client.post(
        "/activities/Chess Club/unregister",
        json={"email": "teststudent@mergington.edu"}
    )
    assert unregister_resp.status_code == 200
    # Unregister again should fail
    unregister_again = client.post(
        "/activities/Chess Club/unregister",
        json={"email": "teststudent@mergington.edu"}
    )
    assert unregister_again.status_code == 404

def test_signup_activity_not_found():
    resp = client.post("/activities/Nonexistent/signup", params={"email": "nobody@mergington.edu"})
    assert resp.status_code == 404

def test_unregister_activity_not_found():
    resp = client.post("/activities/Nonexistent/unregister", json={"email": "nobody@mergington.edu"})
    assert resp.status_code == 404
