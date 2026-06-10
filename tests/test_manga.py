import pytest
from main import app
from fastapi.testclient import TestClient
import sys
import os
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)
manga_id = None


@pytest.fixture(scope="module")
def token():
    client.post("/users", json={
        "username": "mangatest_user",
        "email": "mangatest@gmail.com",
        "password": "test123"
    })
    response = client.post("/login", data={
        "username": "mangatest_user",
        "password": "test123"
    })
    return response.json()["access_token"]


def test_add_manga(token):
    global manga_id
    unique_title = f"Solo Max Level Newbie {uuid.uuid4()}"
    response = client.post("/manga_list", json={
        "title": unique_title,
        "genre": "Action",
        "is_favourite": True,
        "chapter_read": 237,
        "status": "Completed",
        "rating": 10.0,
        "review": "Masterpiece"
    }, headers={"Authorization": f"Bearer {token}"})

    manga_id = response.json()["id"]
    assert response.status_code == 200
    assert response.json()["title"] == unique_title


def test_get_manga(token):
    response = client.get("/manga_list",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_manga(token):
    response = client.put(f"manga_list/{manga_id}",
                          json={"rating": 9.4},
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_delete_manga(token):
    response = client.delete(f"/manga_list/{manga_id}",
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
