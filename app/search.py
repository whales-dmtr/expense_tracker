from typing import Annotated

from sqlmodel import Session, select
from fastapi import APIRouter, Depends

from app.database import get_db_session
from app.schemas import Expense, UserData
from app.authentication import verify_token

router = APIRouter()


def sort_expenses_by_priority(expenses: list) -> list:
    result = []

    priorities = []
    for id, priority in expenses:
        priorities.append(priority)

    while expenses != []:
        highest_priority_id = priorities.index(max(priorities))
        result.append(expenses[highest_priority_id])

        del expenses[highest_priority_id]
        del priorities[highest_priority_id]

    return result


@router.get('/expenses/search')
def search_expenses(
        user: Annotated[UserData, Depends(verify_token)],
        db: Annotated[Session, Depends(get_db_session)],
        query: str):
    expenses = db.exec(
        select(Expense.id, Expense.description).where(Expense.user_id == user.id)).all()
    appropriate_expenses = []

    for id, desc in expenses:
        priority = desc.count(query)
        if priority > 0:
            appropriate_expenses.append((id, priority))

    sorted_expenses_by_priority = sort_expenses_by_priority(
        appropriate_expenses)

    expenses_data = []
    for id, _ in sorted_expenses_by_priority:
        expense = db.exec(select(Expense).where(Expense.id == id)).one()
        expenses_data.append(expense)

    return expenses_data
