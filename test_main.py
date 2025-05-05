#!/usr/bin/python3

from fastapi.testclient import TestClient
from main import app
import models
from database import engine

client = TestClient(app)

def setup_module():
    models.Base.metadata.create_all(bind=engine)

def teardown_module():
    models.Base.metadata.drop_all(bind=engine)

def test_create_user():
    response = client.post(
        "api/v1/users/",
        json={"email": "test@example.com", "username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["username"] == "testuser"

def test_login():
    response = client.post(
        "api/v1/token",
        data={"username": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]

def test_protected_route():
    token = test_login()
    response = client.get(
        "api/v1/users/me/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_create_book():
    token = test_login()
    response = client.post(
        "api/v1/books/",
        json={
            "title": "Test Book",
            "description": "Test Description",
            "genre": "Test",
            "publication_date": "2023-01-01",
            "author_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

def test_get_recommendations():
    token = test_login()
    response = client.get(
        "api/v1/recommendations/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
