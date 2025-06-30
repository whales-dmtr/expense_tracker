import pytest

from tests.integration.conftest import client
from app.routers.authentication import create_token

url_register = '/auth/register'
url_login = '/auth/login'

headers_login = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}
headers_register = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}


def register(username, email):
    data = {
        "id": 0,
        "username": f"{username}",
        "email": f"{email}",
        "password": "1234"
    }
    response = client.post(
        url_register, headers=headers_register, json=data)
    return response.status_code


def login(username, password):
    data = {
        'username': f'{username}',
        'password': f'{password}',
    }
    response = client.post(url_login, headers=headers_login, data=data)
    return {"status_code": response.status_code, 
            "access_token": response.json().get("access_token")}


def authorize(token):
    headers = { "Authorization": f"Bearer {token}" }
    response = client.get('/me', headers=headers)
    return response.status_code


def test_register():
    assert register("user", "user@example.com") == 200


def test_register_already_exist_username():
    assert register("user", "some_email@example.com") == 400


def test_register_already_exist_email():
    assert register("other_user", "user@example.com") == 400


def test_login():
    assert login("user", "1234")["status_code"] == 200


def test_login_with_nonexistent_user(): 
    assert login("nonexistent", "1234")["status_code"] == 401


def test_login_incorrect_password():
    assert login("user", "4321")["status_code"] == 401


def test_authorize_with_invalid_token():
    assert authorize("invalid_token") == 401


def test_authorize_with_fake_token():
    fake_generated_token = create_token({'sub': '0'}, minutes_expires=1)
    assert authorize(fake_generated_token) == 401
