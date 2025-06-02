from typing import Annotated
from datetime import datetime, timezone, timedelta


from fastapi import APIRouter, Depends, HTTPException, status
import psycopg2

from app.authentication import verify_token
from app.constants import DB_CONN_DATA
from app.schemas import UserFullData, ExpenseData, ExpenseFullData

router = APIRouter()


@router.get('/expense/{expense_id}')
def get_expense_by_id(user: Annotated[UserFullData, Depends(verify_token)], expense_id: int):
    with psycopg2.connect(**DB_CONN_DATA) as connection:
        with connection.cursor() as cursor:
            get_expense_query =  "SELECT * FROM expenses WHERE id = %s AND user_id = %s"
            cursor.execute(get_expense_query, (expense_id, user.id,))
            expense_data = cursor.fetchone()

            if expense_data is None:
                raise HTTPException(
                    status_code=404,
                    detail="You don't have the expense with this id."
                )

            owner_id = expense_data[-1]
            get_username_query = "SELECT username FROM users WHERE id = %s"
            cursor.execute(get_username_query, (owner_id,))
            owner_username = cursor.fetchone()[0]

            expense_time_created = datetime.fromisoformat(str(expense_data[3]))
            expense_time_created_formatted = expense_time_created.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            owner = f"{owner_username}({owner_id})"

            expense_full_data = ExpenseFullData(
                expense_id=expense_data[0],
                desc=expense_data[1],
                amount=expense_data[2],
                time_created=expense_time_created_formatted,
                category=expense_data[4],
                owner=owner
            )

            return expense_full_data


@router.get('/expenses')
def get_all_expenses(user: Annotated[UserFullData, Depends(verify_token)]) -> list[list[int | str]]:
    with psycopg2.connect(**DB_CONN_DATA) as connection:
        with connection.cursor() as cursor:
            find_all_expenses_query = "SELECT id, description, amount, time_created, category FROM expenses WHERE user_id = %s"
            cursor.execute(find_all_expenses_query, (user.id, ))
    
            expenses = cursor.fetchall()
            expense_id = 0

            while expense_id < len(expenses):
                expenses[expense_id] = list(expenses[expense_id])
                expenses[expense_id][3] = str(datetime.fromisoformat(str(expenses[expense_id][3])))
                expense_id += 1

            return expenses


@router.post('/expense')
def create_expense(user: Annotated[UserFullData, Depends(verify_token)], expense: ExpenseData) -> dict[str, int]:
    with psycopg2.connect(**DB_CONN_DATA) as connection:
        with connection.cursor() as cursor:
            if expense.time_created == None:
                expense.time_created = str(datetime.now(timezone(timedelta(hours=3))))
            
            if expense.category == None:
                expense.category = 'Others'

            add_expense_query = """INSERT INTO expenses(id, description, amount, time_created, category, user_id) 
                        VALUES (nextval('expenses_id_seq'), %s, %s, %s, %s, %s)"""
            cursor.execute(add_expense_query, (
                expense.desc, 
                expense.amount, 
                expense.time_created, 
                expense.category, 
                user.id
            )) 

            find_user_id_query = "SELECT id FROM expenses WHERE description = %s AND amount = %s AND time_created = %s AND category = %s"

            cursor.execute(find_user_id_query, (
                expense.desc, 
                expense.amount, 
                expense.time_created, 
                expense.category 
            ))

            expense_id = cursor.fetchone()[0]

            connection.commit()

    return {'result': expense_id}


@router.put('/expense/{expense_id}')
def update_expense(user: Annotated[UserFullData, Depends(verify_token)], expense_id):
    with psycopg2.connect(**DB_CONN_DATA) as connection:
        with connection.cursor() as cursor:
            return


@router.delete('/expense/{expense_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_expense(user: Annotated[UserFullData, Depends(verify_token)], expense_id: int):
    with psycopg2.connect(**DB_CONN_DATA) as connection:
        with connection.cursor() as cursor:
            check_expense_exist_query = "SELECT 1 FROM expenses WHERE id = %s AND user_id = %s"
            cursor.execute(check_expense_exist_query, (expense_id, user.id))
            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="You don't have the expense with this id."
                )

            remove_expense_query = "DELETE FROM expenses WHERE id = %s"
            cursor.execute(remove_expense_query, (expense_id, ))

            connection.commit()

            return 