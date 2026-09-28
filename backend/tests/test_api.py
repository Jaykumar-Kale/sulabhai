import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_register_and_login():
    r = client.post("/api/auth/register", json={
        "name": "Test User", "email": "testuser1@example.com",
        "password": "testpass123", "role": "citizen",
    })
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data

    r2 = client.post("/api/auth/login", json={
        "email": "testuser1@example.com", "password": "testpass123",
    })
    assert r2.status_code == 200
    assert "access_token" in r2.json()


def test_duplicate_register_fails():
    client.post("/api/auth/register", json={
        "name": "Dup", "email": "dup@example.com", "password": "pass1234",
    })
    r = client.post("/api/auth/register", json={
        "name": "Dup2", "email": "dup@example.com", "password": "pass1234",
    })
    assert r.status_code == 400


def test_list_schemes_empty_ok():
    r = client.get("/api/schemes")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_eligibility_requires_id():
    r = client.post("/api/eligibility/check", json={"age": 20})
    assert r.status_code == 400


def test_chat_requires_auth():
    r = client.post("/api/chat", json={"message": "hello"})
    assert r.status_code == 401


@pytest.fixture(autouse=True, scope="session")
def cleanup():
    yield
    if os.path.exists("test.db"):
        os.remove("test.db")
