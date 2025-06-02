from typing import Annotated
from datetime import datetime, timezone, timedelta


from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session

from app.authentication import verify_token
from app.schemas import UserData, ExpenseData, Expense
from app.database import get_db_session

router = APIRouter()


@router.get('/expense/{expense_id}')
def get_expense_by_id(user: Annotated[UserData, Depends(verify_token)], 
                      db: Annotated[Session, Depends(get_db_session)], 
                      expense_id: int) -> ExpenseData:
    expense = db.exec(select(Expense).where(Expense.id == expense_id, 
                                            Expense.user_id == user.id)).one()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="You don't have the expense with this id."
        )

    expense_time_created = datetime.fromisoformat(str(expense.time_created))
    expense_time_created_formatted = expense_time_created.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    expense_full_data = ExpenseData(
        id=expense.id,
        desc=expense.description,
        amount=expense.amount,
        time_created=expense_time_created_formatted,
        category=expense.category
    )

    return expense_full_data


@router.get('/expenses')
def get_all_expenses(user: Annotated[UserData, Depends(verify_token)], 
                     db: Annotated[Session, Depends(get_db_session)]):
    expenses = db.exec(select(Expense).where(Expense.user_id == user.id)).all()

    for expense in expenses:
        expense_time_created_formatted = str(datetime.fromisoformat(str(expense.time_created)))
        expense.time_created = expense_time_created_formatted
    
    return expenses


@router.post('/expense')
def create_expense(user: Annotated[UserData, Depends(verify_token)], 
                   db: Annotated[Session, Depends(get_db_session)], 
                   expense: ExpenseData):
    if expense.time_created == None:
        expense.time_created = str(datetime.now(timezone(timedelta(hours=3))))
            
    if expense.category == None:
        expense.category = 'Others'

    expense_for_db = Expense(
        description=expense.desc,
        amount=expense.amount,
        time_created=expense.time_created,
        category=expense.category,
        user_id=user.id
    )
    db.add(expense_for_db)
    db.commit()

    return {'result': expense_for_db.id}


@router.put('/expense/{expense_id}')
def update_expense(user: Annotated[UserData, Depends(verify_token)], 
                   db: Annotated[Session, Depends(get_db_session)], expense_id):
    return


@router.delete('/expense/{expense_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_expense(user: Annotated[UserData, Depends(verify_token)], 
                   db: Annotated[Session, Depends(get_db_session)], expense_id: int):
    check_expense_exist_query = select(Expense).where(Expense.id == expense_id, 
                                                      Expense.user_id == user.id)
    expense = db.exec(check_expense_exist_query).one()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="You don't have the expense with this id."
        )

    db.delete(expense)
    db.commit()

    return 