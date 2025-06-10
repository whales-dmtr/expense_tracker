from typing import Annotated
import re

from sqlmodel import Session, select
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from app.database import get_db_session
from app.schemas import Expense, UserData
from app.authentication import verify_token

router = APIRouter(tags=['Expenses', 'Search'])


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


@router.get('/expenses/search/regex', summary="Search expenses by regex")
def search_expenses_by_regex(
        user: Annotated[UserData, Depends(verify_token)],
        db: Annotated[Session, Depends(get_db_session)],
        pattern: str, flags: str = 'g'):
    expenses = db.exec(
        select(Expense.id, Expense.description).where(Expense.user_id == user.id)).all()
    appropriate_expenses = []

    compiled_flags, is_global = convert_flags(flags)
    try:
        pattern = re.compile(pattern, compiled_flags)
    except re.error as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid regex pattern: {e}")

    if is_global:
        for id, desc in expenses:
            priority = len(re.findall(pattern, desc))
            if priority:
                appropriate_expenses.append((id, priority))
        sorted_expenses_by_priority = sort_expenses_by_priority(
            appropriate_expenses)

        expenses_data = []
        for id, _ in sorted_expenses_by_priority:
            expense = db.exec(
                select(Expense).where(Expense.id == id)).one()
            expenses_data.append(expense)

        return expenses_data
    else:
        for id, desc in expenses:
            if re.search(pattern, desc):
                expense_data = db.exec(
                    select(Expense).where(Expense.id == id)).one()
                appropriate_expenses.append(expense_data)
        return appropriate_expenses
