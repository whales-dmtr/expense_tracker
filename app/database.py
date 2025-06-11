from sqlmodel import Session, create_engine

from app.constants import SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_db_session():
    with Session(engine) as session:
        yield session
