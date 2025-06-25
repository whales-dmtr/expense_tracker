from typing import Annotated
from datetime import timedelta, datetime, timezone

import jwt
from jwt import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from argon2 import PasswordHasher
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, NoResultFound


from app.schemas import UserData, Token
from app.db.models import User
import app.constants as const
from app.db.database import get_db_session


router = APIRouter(tags=['Authentication'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_token(payload: dict, minutes_expires: int | None = None) -> str:
    if minutes_expires:
        time_available = datetime.now(
            timezone(timedelta(hours=3))) + timedelta(minutes=minutes_expires)
    else:
        time_available = datetime.now(timezone(
            timedelta(hours=3))) + timedelta(minutes=const.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({'exp': time_available})
    token = jwt.encode(payload, const.SECRET_KEY, const.ALGORITHM)

    return token


def verify_user(user: OAuth2PasswordRequestForm, db: Session) -> int | bool:
    try:
        user_from_db = db.exec(select(User).where(
            User.username == user.username)).one()
    except Exception:
        return None

    if user_from_db.password is None:
        return None

    ph = PasswordHasher()
    try:
        ph.verify(user_from_db.password, user.password)
    except Exception:
        return None

    return user_from_db.id


def verify_token(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db_session)]) -> UserData:
    """If token is valid function returns user object. In other way it raises an error."""
    unauth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Your jwt is invalid.",
    )
    try:
        payload: dict = jwt.decode(
            token, const.SECRET_KEY, algorithms=[const.ALGORITHM])
        id = payload.get("sub")
        user: User = db.exec(select(User).where(User.id == id)).one()
        if not user:
            return unauth_error
    except InvalidTokenError:
        raise unauth_error
    except NoResultFound:
        raise unauth_error

    user_data = user.convert_to_user_data()

    return user_data


@router.post('/auth/login', summary="Authenticate user")
def login(
        user: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[Session, Depends(get_db_session)]) -> Token:
    verified_user_id = verify_user(user, db)

    if not verified_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_token(
        payload={'sub': str(verified_user_id)},  # subject is the id of user
        minutes_expires=20,
    )

    return Token(access_token=access_token, token_type='bearer')


@router.post('/auth/register', summary='Register a new user')
def register(user: UserData, db: Annotated[Session, Depends(get_db_session)]):
    ph = PasswordHasher()
    hashed_password = ph.hash(user.password)

    try:
        user_for_db = User(
            username=user.username,
            password=hashed_password,
            email=user.email
        )
        db.add(user_for_db)
        db.commit()
    except IntegrityError as e:
        if 'username' in str(e.orig):
            raise HTTPException(
                status_code=400,
                detail="User with this username already exists."
            )
        elif 'email' in str(e.orig):
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists."
            )

    user_data = user_for_db.convert_to_user_data()
    return {'user': user_data}
