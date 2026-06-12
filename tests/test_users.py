from main import app
from fastapi.testclient import TestClient
import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


client = TestClient(app)


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Otaku Hub" in response.json()["message"]


def test_register_user(client):
    import random
    rand = random.randint(1000, 9999)
    response = client.post("/users", json={
        "username": f"testuser_{rand}",
        "email": f"testuser_{rand}@gmail.com",
        "password": "test123"
    })
    assert response.status_code == 200


def test_register_duplicate_user(client):
    client.post("/users", json={
        "username": "dupuser",
        "email": "dup@gmail.com",
        "password": "test123"
    })
    response = client.post("/users", json={
        "username": "dupuser",
        "email": "dup@gmail.com",
        "password": "test123"
    })
    assert response.status_code == 400


def test_login_success():
    client.post("/users", json={
        "username": "logintest",
        "email": "logintest@gmail.com",
        "password": "test123"
    })
    response = client.post("/login", data={
        "username": "logintest",
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    response = client.post("/login", data={
        "username": "logintest",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_access_protected_without_token():
    response = client.get("/anime_list")
    assert response.status_code == 401


def test_access_protected_with_invalid_token():
    response = client.get("/anime_list",
                          headers={"Authorization": "Bearer invalidtoken123"}
                          )
    assert response.status_code == 401
