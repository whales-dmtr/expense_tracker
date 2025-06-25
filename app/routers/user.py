from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlalchemy.exc import NoResultFound

from app.schemas import UserData
from app.db.models import User, Expense
from app.routers.authentication import verify_token
from app.db.database import get_db_session, Session

router = APIRouter()


@router.get('/me', tags=['User'], summary="Get your username")
def get_username(user: Annotated[UserData, Depends(verify_token)]):
    return {'your_username': user.username}


@router.delete('/me', tags=['User'], summary="Remove your account")
def remove_user(
        user: Annotated[UserData, Depends(verify_token)],
        db: Annotated[Session, Depends(get_db_session)]):
    user_id = db.exec(select(User.id).where(
        User.username == user.username)).one()
    try:
        user_expenses = db.exec(select(Expense).where(
            Expense.user_id == user_id)).all()
        for exp in user_expenses:
            db.delete(exp)
    except NoResultFound:
        pass

    user_in_db = db.exec(select(User).where(User.id == user_id)).one()
    db.delete(user_in_db)

    db.commit()

    return {'user ID': user_id, 'expenses_quantity': len(user_expenses)}
