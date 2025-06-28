from unittest.mock import Mock, patch
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.authentication import login
from tests.unit.test_auth import UserLoginCreds

client = TestClient(app)

@pytest.fixture
@patch("app.routers.authentication.ph")
def access_token(mocked_password_hasher):
    user = UserLoginCreds("user", "1234")

    def set_id():
        setattr(user, 'id', 7)
        return user

    mocked_db = Mock()
    mocked_db.exec().one = lambda: set_id()
    mocked_password_hasher.verify.return_value = True

    response = login(user, mocked_db)

    return response.access_token

    
