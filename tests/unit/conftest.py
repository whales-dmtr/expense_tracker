import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.authentication import create_token

client = TestClient(app)

@pytest.fixture
def access_token():
    token = create_token(
        payload={'sub': '7'},
        minutes_expires=1
    )
    return token

    
