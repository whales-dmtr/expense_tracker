from dotenv import load_dotenv
import os

import pytest
from fastapi.testclient import TestClient
from fastapi import Response
from sqlmodel import Session, create_engine, select, delete
from alembic.config import Config
from alembic import command

from app.main import app
from app.db.database import get_db_session
from app.db.models import User, Expense
from app.schemas import ExpenseData

load_dotenv('.env.test')
TEST_DB_URL = os.getenv("TEST_DB_URL")
engine = create_engine(TEST_DB_URL)


def get_test_db_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_db_session] = get_test_db_session
client = TestClient(app)


def create_expense(access_token, expense_data: ExpenseData) -> Response:
    data = dict(expense_data)
    response = client.post('/expense', headers=access_token, json=data)
    return response



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


@pytest.fixture(scope="session")
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
    token = response.json()['access_token']

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def expense_id(access_token):
    expenses_data = [
        {"description": "lime", "amount": "20"},
        {"description": "lime lime", "amount": "40"},
        {"description": "lime lime lime", "amount": "60"},
        {"description": "LIME LIME LIME", "amount": "60"},
        {"description": "not fruit", "amount": "0"},
        {"description": "banana", "amount": "100.50"}
    ]
    for i  in expenses_data:
        response = create_expense(access_token, i)
    assert response.status_code == 200
    return response.json()['result']


@pytest.fixture(scope="session", autouse=True)
def cleanup_user(database: Session):
    yield

    user_in_db = database.exec(select(User).where(User.username == \
                                                  'user')).one()
    database.exec(delete(Expense).where(Expense.user_id == user_in_db.id))
    database.delete(user_in_db)
    database.commit()