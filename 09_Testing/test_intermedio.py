from fastapi.testclient import TestClient
from intermedio import app

client = TestClient(app)

def test_get_user():
    response = client.get(
        "/users/1",
        headers={"X-Token": "secret-token"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "1", 
        "username": "userone", 
        "email": "user1@gmail.com"
        }

def test_get_user_invalid_token():
    response = client.get(
        "/users/1",
        headers={"X-Token": "invalid-token"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}

def test_get_non_existent_user():
    response = client.get(
        "/users/3",
        headers={"X-Token": "secret-token"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User not found"}

def test_create_user():
    new_user = {
        "id": "3",
        "username": "userthree",
        "email": "user3@gmail.com",
    }
    response = client.post(
        "/users/",
        json=new_user,
        headers={"X-Token": "secret-token"}
    )
    assert response.status_code == 200
    assert response.json() == new_user

def test_create_user_bad_token():
    new_user = {
        "id": "4",
        "username": "userfour",
        "email": "user4@gmail.com",
    }
    response = client.post(
        "/users/",
        json=new_user,
        headers={"X-Token": "bad-token"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}

def test_create_existing_user():
    existing_user = {
        "id": "1",
        "username": "userone",
        "email": "user1@gmail.com",
    }
    response = client.post(
        "/users/",
        json=existing_user,
        headers={"X-Token": "secret-token"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


