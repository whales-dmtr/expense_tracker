from types import NoneType
from typing import Annotated
from datetime import timedelta, datetime, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from argon2 import PasswordHasher, exceptions
import psycopg2


from app.schemas import LoginValidation, RegisterValidation, Token
from app.constants import DB_CONN_DATA
import app.constants as const
from app.constants import SECRET_KEY, ALGORITHM


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_token(payload: dict, minutes_expires : int | None = None) -> str:
    if minutes_expires :
        time_available = datetime.now(timezone(timedelta(hours=3))) + timedelta(minutes=minutes_expires)
    else:
        time_available = datetime.now(timezone(timedelta(hours=3))) + timedelta(minutes=5)

    payload.update({'exp': time_available})
    token = jwt.encode(payload, const.SECRET_KEY, const.ALGORITHM)

    return token


def get_username_by_id(id) -> bool:
    with psycopg2.connect(**DB_CONN_DATA) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username FROM users WHERE id = %s;", (id,))
            username = cursor.fetchone()[0]

            return username


def check_user_existence(id: int) -> bool:
    with psycopg2.connect(**DB_CONN_DATA) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE id = %s;", (id,))
            return bool(cursor.fetchone()[0])


def verify_user(user: LoginValidation) -> int | bool:
    with psycopg2.connect(**DB_CONN_DATA) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM users WHERE username = %s;", (user.username,))
            result = cursor.fetchone()

            if isinstance(result, NoneType):
                return False
            elif isinstance(result, tuple):
                correct_password_hash = result[0]

                ph = PasswordHasher()

                try:
                    ph.verify(correct_password_hash, user.password)
                except exceptions.VerifyMismatchError as e:
                    print(e)
                    return False

                cursor.execute("SELECT id FROM users WHERE username = %s", (user.username,))

                user_id = cursor.fetchone()[0]

                return user_id


def verify_token(token: str) -> int:
    """If token is valid function returns id of user. In other way it raise an error."""
    unauth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Your jwt is invalid.",
    )
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        if not check_user_existence(id):
            return unauth_error
    except jwt.InvalidTokenError:
        raise unauth_error

    return id 


@router.post('/login') 
def login(user: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    verified_user_id = verify_user(user)

    if not verified_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_token(
        payload={'sub': str(verified_user_id)},  # subject is the id of user
    )

    return Token(access_token=access_token, token_type='bearer')


@router.post('/register')
def register(user: RegisterValidation) -> dict[str, str]:
    with psycopg2.connect(**DB_CONN_DATA) as connection:
        with connection.cursor() as cursor:
            ph = PasswordHasher()
            hashed_password = ph.hash(user.password)
            cursor.execute(f"""INSERT INTO users (id, username, password, email) 
                            VALUES (nextval('users_id_seq'), '{user.username}', '{hashed_password}', '{user.email}')""")

            cursor.execute(f"""SELECT * FROM users 
                            WHERE username = '{user.username}'""")
            user_data = str(cursor.fetchone())

            connection.commit()

            return {'user': user_data}
