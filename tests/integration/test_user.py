import pytest

from tests.integration.conftest import client, create_expense
from tests.integration.test_auth import register, login

url_user = '/me'


def test_get_username(access_token):
    response = client.get(url_user, headers=access_token)

    assert response.json()['your_username'] == 'user'


def test_remove_user():
    register("user_for_remove", "user_for_remove@example.com")    
    token = login("user_for_remove", "1234")["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    create_expense(headers, {"description": "user_for_remove expense",
                           "amount": "0"})
    response = client.delete(url_user, headers=headers)

    assert response.json()['user_id']

