import pytest
from unittest.mock import Mock, patch

from app.routers.authentication import register, login, verify_token
from app.schemas import UserData


class UserLoginCreds:
    def __init__(self, username , password):
        self.username = username
        self.password = password


def test_register():
    user = UserData(
        id = 7,
        username="user",
        password="1234",
        email="user@duck.com"
    )

    mocked_db = Mock()
    
    mocked_db.add = lambda user: setattr(user, 'id', 7)

    response = register(user, mocked_db)
    
    assert response["user"] == \
        UserData(id=7, username="user", password=None, email="user@duck.com")


@patch("app.routers.authentication.ph")
def test_login(mocked_password_hasher):
    user = UserLoginCreds("user", "1234")

    def set_id():
        setattr(user, 'id', 7)
        return user

    mocked_db = Mock()
    mocked_db.exec().one = lambda: set_id()
    mocked_password_hasher.verify.return_value = True

    response = login(user, mocked_db)

    assert response.token_type == 'bearer'


def test_token_verify(access_token):
    mocked_db = Mock()

    response = verify_token(access_token, mocked_db)

    assert response