import pytest

from tests.integration.conftest import client
from tests.integration.test_auth import register, login
from app.routers.authentication import create_token

url_user = '/me'


def test_get_username(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.get(url_user, headers=headers)

    assert response.json()['your_username'] == 'user'


def test_remove_user():
    register("user_for_remove", "user_for_remove@example.com")    
    token = login("user_for_remove", "1234")["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.delete(url_user, headers=headers)

    assert response.json()['user_id']

