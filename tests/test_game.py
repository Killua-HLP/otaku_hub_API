import pytest
from main import app
from fastapi.testclient import TestClient
import sys
import os
import uuid
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)
game_id = None


@pytest.fixture(scope="module")
def token():
    client.post("/users", json={
        "username": "gametest_user",
        "email": "gametest@gmail.com",
        "password": "test123"
    })
    response = client.post("/login", data={
        "username": "gametest_user",
        "password": "test123"
    })
    return response.json()["access_token"]


def test_add_game(token):
    global game_id
    unique_title = f"Valorant {uuid.uuid4}"
    response = client.post("/game", json={
        "title": unique_title,
        "genre": "FPS",
        "rank": "999",
        "hour_played": 223,
        "started_date": "2024-01-01",
        "finished_date": "2026-01-01",
        "rating": 1,
        "notes": "nth"
    }, headers={"Authorization": f"Bearer {token}"})

    game_id = response.json()["id"]
    assert response.status_code == 200
    assert response.json()["title"] == unique_title


def test_get_game(token):
    response = client.get("/game",
                          headers={"Authorization": f"Bearer {token}"})
    assert isinstance(response.json(), list)


def test_update_game(token):
    response = client.put(f"/game/{game_id}",
                          json={"rating": 4.5},
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_delete_game(token):
    response = client.delete(f"/game/{game_id}",
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
