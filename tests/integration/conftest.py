from dotenv import load_dotenv
import os

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, select
from alembic.config import Config
from alembic import command

from app.main import app
from app.db.database import get_db_session
from app.db.models import User

load_dotenv('.env.test')
TEST_DB_URL = os.getenv("TEST_DB_URL")
engine = create_engine(TEST_DB_URL)


def get_test_db_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_db_session] = get_test_db_session
client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)  
    alembic_cfg.set_main_option("script_location", "migrations")

    command.upgrade(alembic_cfg, revision="head")

    # If you upgraded migrations uncomment these lines, comment "upgrade" line
    #   and downgrade changes
    # After, comment downgrade lines and uncomment upgrade line 

    # command.stamp(alembic_cfg, "head")
    # command.downgrade(alembic_cfg, "-1")


@pytest.fixture(scope="session")
def database():
    yield from get_test_db_session()


@pytest.fixture
def access_token():
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

    return response.json()['access_token']


@pytest.fixture(scope="session", autouse=True)
def cleanup_user(database: Session):
    yield

    user_in_db = database.exec(select(User).where(User.username == \
                                                  'user')).one()
    database.delete(user_in_db)
    database.commit()