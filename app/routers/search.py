from typing import Annotated
import re

from sqlmodel import Session, select
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from app.db.database import get_db_session
from app.schemas import UserData
from app.db.models import Expense
from app.routers.authentication import verify_token

router = APIRouter(tags=['Expenses', 'Search'])


def sort_expenses_by_matches(expenses: list) -> list:
    result = []

    matches = []
    for id, priority in expenses:
        matches.append(priority)

    while expenses != []:
        highest_priority_idx = matches.index(max(matches))
        expense_data = {
            'id': expenses[highest_priority_idx][0].id,
            'description': expenses[highest_priority_idx][0].description,
            'matches': expenses[highest_priority_idx][1]
        }
        result.append(expense_data)

        del expenses[highest_priority_idx]
        del matches[highest_priority_idx]

    return result


def convert_flags(flags: str) -> tuple[int, bool]:
    python_flags = 0
    is_global = False
    flags_matches = {
        'i': re.IGNORECASE,
        'm': re.MULTILINE,
        's': re.DOTALL,
        'u': re.UNICODE,
    }

    for flag in flags:
        if flag == 'g':
            is_global = True
        elif flags_matches.get(flag):
            python_flags |= flags_matches.get(flag)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unknown flag."
            )

    return (python_flags, is_global)


@router.get('/expenses/search', summary="Search expenses by description")
def search_expenses(
        user: Annotated[UserData, Depends(verify_token)],
        db: Annotated[Session, Depends(get_db_session)],
        query: str):
    expenses = db.exec(
        select(Expense).where(Expense.user_id == user.id)).all()
    appropriate_expenses = []

    for expense in expenses:
        priority = expense.description.count(query)
        if priority > 0:
            appropriate_expenses.append((expense, priority))

    expenses_data = sort_expenses_by_matches(
        appropriate_expenses)

    return expenses_data


@router.get('/expenses/search/regex', summary="Search expenses by regex")
def search_expenses_by_regex(
        user: Annotated[UserData, Depends(verify_token)],
        db: Annotated[Session, Depends(get_db_session)],
        pattern: str, flags: str = 'g'):
    expenses = db.exec(
        select(Expense).where(Expense.user_id == user.id)).all()
    appropriate_expenses = []

    compiled_flags, is_global = convert_flags(flags)
    try:
        pattern = re.compile(pattern, compiled_flags)
    except re.error as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid regex pattern: {e}")

    if is_global:
        for expense in expenses:
            priority = len(re.findall(pattern, expense.description))
            if priority:
                appropriate_expenses.append((expense, priority))
        expenses_data = sort_expenses_by_matches(
            appropriate_expenses)

        return expenses_data
    else:
        for id, desc in expenses:
            if re.search(pattern, desc):
                expense_data = db.exec(
                    select(Expense).where(Expense.id == id)).one()
                appropriate_expenses.append(expense_data)
        return appropriate_expenses
