import pytest
from main import app
from fastapi.testclient import TestClient
import sys
import os
import uuid
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)
anime_id = None


@pytest.fixture(scope="module")
def token():
    client.post("/users", json={
        "username": "animetest_user",
        "email": "animetest@gmail.com",
        "password": "test123"
    })
    response = client.post("/login", data={
        "username": "animetest_user",
        "password": "test123"
    })
    return response.json()["access_token"]


def test_add_anime(token):
    global anime_id
    unique_title = f"Hunter x Hunter {uuid.uuid4()}"
    response = client.post("/anime_list", json={
        "title": unique_title,
        "genre": "Action",
        "is_favourite": True,
        "episode_watched": 148,
        "status": "Completed",
        "rating": 10.0,
        "review": "Masterpiece"
    }, headers={"Authorization": f"Bearer {token}"})

    anime_id = response.json()["id"]
    assert response.status_code == 200
    assert response.json()["title"] == unique_title


def test_get_anime(token):
    response = client.get("/anime_list",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_anime(token):
    response = client.put(f"/anime_list/{anime_id}",
                          json={"rating": 9.5},
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_delete_anime(token):
    response = client.delete(f"/anime_list/{anime_id}",
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
