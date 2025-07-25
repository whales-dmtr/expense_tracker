from typing import Annotated
from datetime import datetime, timezone, timedelta


from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from sqlalchemy.exc import NoResultFound

from app.routers.authentication import verify_token
from app.schemas import UserData, ExpenseData, ExpenseDataModified
from app.db.models import Expense
from app.db.database import get_db_session

router = APIRouter(tags=['Expenses'])


@router.get('/expense/{expense_id}', summary="Get expense by ID")
def get_expense_by_id(
        user: Annotated[UserData, Depends(verify_token)],
        db: Annotated[Session, Depends(get_db_session)],
        expense_id: int) -> ExpenseData:
    try:
        expense = db.exec(select(Expense).where(Expense.id == expense_id,
            Expense.user_id == user.id)).one()
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail="You don't have the expense with this id."
        )

    expense_time_created = datetime.fromisoformat(str(expense.time_created))
    expense_time_created_formatted = expense_time_created.strftime(
        "%Y-%m-%d %H:%M:%S.%f")[:-3]

    expense_full_data = ExpenseData(
        id=expense.id,
        description=expense.description,
        amount=expense.amount,
        time_created=expense_time_created_formatted,
        category=expense.category
    )

    return expense_full_data


@router.get('/expenses', summary="List all expenses")
def get_all_expenses(
        user: Annotated[UserData, Depends(verify_token)],
        db: Annotated[Session, Depends(get_db_session)]) -> list[ExpenseData]:
    expenses = db.exec(select(Expense).where(Expense.user_id == user.id)).all()

    for expense in expenses:
        expense_time_created = datetime.fromisoformat(str(expense.time_created))
        expense_time_created_formatted = expense_time_created.strftime(
            "%Y-%m-%d %H:%M:%S.%f")[:-3]
        expense.time_created = expense_time_created_formatted

    return expenses


@router.post('/expense', summary="Create a new expense")
def create_expense(
        user: Annotated[UserData, Depends(verify_token)],
        db: Annotated[Session, Depends(get_db_session)],
        expense: ExpenseData):
    time_created = expense.time_created or str(
        datetime.now(timezone(timedelta(hours=3))))
    category = expense.category or 'Others'

    expense_for_db = Expense(
        description=expense.description,
        amount=expense.amount,
        time_created=time_created,
        category=category,
        user_id=user.id
    )
    db.add(expense_for_db)
    db.commit()

    return {'result': expense_for_db.id}


@router.put('/expense/{expense_id}', summary="Update an expense")
def update_expense(
        user: Annotated[UserData, Depends(verify_token)],
        db: Annotated[Session, Depends(get_db_session)], expense_id,
        modified_expense_data: ExpenseDataModified):
    try:
        modified_expense = db.exec(
            select(Expense).where(Expense.id == expense_id)).one()
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail="No expense with this id was found."
        )

    fields_to_change = []

    for k in modified_expense.__dict__.keys():
        if not k in ['_sa_instance_state', 'user_id', 'id']:
            fields_to_change.append(k)

    for attr_name in fields_to_change:
        changed_value = getattr(modified_expense_data, attr_name)
        if changed_value is not None:
            setattr(modified_expense, attr_name, changed_value)

    db.add(modified_expense)
    db.commit()
    db.refresh(modified_expense)

    return {"Updated expense id": modified_expense.id}


@router.delete('/expense/{expense_id}', status_code=status.HTTP_204_NO_CONTENT, summary="Delete an expense")
def remove_expense(
        user: Annotated[UserData, Depends(verify_token)],
        db: Annotated[Session, Depends(get_db_session)], expense_id: int):
    check_expense_exist_query = select(Expense).where(Expense.id == expense_id,
                                                      Expense.user_id == user.id)
    try:
        expense = db.exec(check_expense_exist_query).one()
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail="You don't have the expense with this id."
        )

    db.delete(expense)
    db.commit()

    return
