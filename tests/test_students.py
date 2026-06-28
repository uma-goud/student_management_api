import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

HEADERS = {"X-API-Key": "mysecretapikey123"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "API is running" in response.json()["message"]


def test_create_student():
    response = client.post(
        "/students/",
        json={
            "name": "Test Student",
            "email": "test123@example.com",
            "phone": "9999999999",
            "branch": "CSE",
            "year": 2
        },
        headers=HEADERS
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Student"
    assert data["email"] == "test123@example.com"
    assert data["is_active"] == True


def test_get_all_students():
    response = client.get("/students/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_student_by_id():
    response = client.get("/students/1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "email" in data


def test_get_student_not_found():
    response = client.get("/students/99999")
    assert response.status_code == 404


def test_create_student_without_auth():
    response = client.post(
        "/students/",
        json={
            "name": "No Auth Student",
            "email": "noauth@example.com",
            "phone": "8888888888",
            "branch": "ECE",
            "year": 1
        }
    )
    assert response.status_code == 403


def test_create_student_invalid_email():
    response = client.post(
        "/students/",
        json={
            "name": "Bad Email",
            "email": "notanemail",
            "phone": "7777777777",
            "branch": "MECH",
            "year": 3
        },
        headers=HEADERS
    )
    assert response.status_code == 422


def test_get_students_by_branch():
    response = client.get("/students/branch/CSE")
    assert response.status_code == 200
    assert isinstance(response.json(), list)