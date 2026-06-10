import pytest
from main import app
from fastapi.testclient import TestClient
import sys
import os
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)
vtuber_id = None


@pytest.fixture(scope="module")
def token():
    client.post("/users", json={
        "username": "vtubertest_user",
        "email": "vtubertest@gmail.com",
        "password": "test123"
    })
    response = client.post("/login", data={
        "username": "vtubertest_user",
        "password": "test123"
    })
    return response.json()["access_token"]


def test_add_vtuber(token):
    global vtuber_id
    unique_name = f"Okayun {uuid.uuid4()}"
    response = client.post("/vtuber", json={
        "name": unique_name,
        "gender": "Isekai",
        "agency": "Hololive",
        "rank": "4",
        "debut_date": "2019-08-01",
        "graduation_date": "2222-07-01",
        "is_favourite": True,
        "primary_language": "JP",
        "youtube_id": None,
        "twitter": None
    }, headers={"Authorization": f"Bearer {token}"})

    vtuber_id = response.json()["id"]
    assert response.status_code == 200
    assert response.json()["name"] == unique_name


def test_get_vtuber(token):
    response = client.get("vtuber",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_vtuber(token):
    response = client.put(f"/vtuber/{vtuber_id}",
                          json={"rating": 9.3},
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_delete_vtuber(token):
    response = client.delete(f"/vtuber/{vtuber_id}",
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
