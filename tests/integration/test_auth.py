import pytest
from sqlmodel import select, Session
from sqlalchemy.exc import NoResultFound

from app.db.models import User
from tests.integration.conftest import client


def test_register():
    url = '/auth/register'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "id": 0,
        "username": "user",
        "email": "user@example.com",
        "password": "1234"
    }

    response = client.post(
        url, headers=headers, json=data)

    assert response.status_code == 200


def test_login():
    url = '/auth/login'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'username': 'user',
        'password': '1234',
    }

    response = client.post(url, headers=headers, data=data)

    assert response.status_code == 200


def test_auth(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = client.delete(
        '/me', headers=headers)

    assert response.status_code == 200


def test_deleted_user(database: Session):
    with pytest.raises(NoResultFound):
        database.exec(select(User).where(User.username == 'user')).one()
