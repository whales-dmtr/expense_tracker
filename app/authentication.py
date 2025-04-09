from types import NoneType
from typing import Annotated
from datetime import timedelta, datetime

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from argon2 import PasswordHasher, exceptions
import psycopg2


from app.schemas import LoginValidation, RegisterValidation, Token
import app.constants as const


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(payload: dict, minutes_expires : int | None = None) -> str:
    if minutes_expires :
        time_available = datetime.now() + timedelta(minutes=minutes_expires)
    else:
        time_available = datetime.now() + timedelta(minutes=15)

    payload.update({'exp': time_available})
    token = jwt.encode(payload, const.SECRET_KEY, const.ALGORITHM)

    return token


def check_user_exist(username) -> bool:
    with psycopg2.connect(
        dbname=const.DB_NAME,
        user=const.DB_USER,
        password=const.DB_PASSWORD,
        host=const.DB_HOST,
        port=const.DB_PORT,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM users WHERE username = %s;", (username,))
            user_exists = bool(cursor.fetchone())

            return user_exists


def verify_user(user: LoginValidation) -> bool:
    with psycopg2.connect(
        dbname=const.DB_NAME,
        user=const.DB_USER,
        password=const.DB_PASSWORD,
        host=const.DB_HOST,
        port=const.DB_PORT,
    ) as connection:
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


@router.post('/login')
def login(user: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    verified_user_id = verify_user(user)

    if not verified_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_token(
        payload={'sub': str(verified_user_id)}  # subject of the token
    )

    return Token(access_token=access_token, token_type='bearer')


@router.post('/register')
def register(user: RegisterValidation) -> dict[str, str]:
    with psycopg2.connect(
        dbname=const.DB_NAME,
        user=const.DB_USER,
        password=const.DB_PASSWORD,
        host=const.DB_HOST,
        port=const.DB_PORT,
    ) as connection:
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
