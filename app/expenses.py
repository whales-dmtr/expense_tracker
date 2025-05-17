from typing import Annotated
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
import psycopg2

from app.authentication import verify_token
from app.constants import DB_CONN_DATA
from app.schemas import UserFullData, ExpenseData

router = APIRouter()


@router.post('/expense')
def create_expense(user: Annotated[UserFullData, Depends(verify_token)], expense: ExpenseData):
    with psycopg2.connect(**DB_CONN_DATA) as connection:
        with connection.cursor() as cursor:
            if expense.time_created == None:
                expense.time_created = str(datetime.now(timezone(timedelta(hours=3))))
            
            if expense.category == None:
                expense.category = 'Others'

            insert_query = """INSERT INTO expenses(id, description, amount, time_created, category, user_id) 
                        VALUES (nextval('expenses_id_seq'), %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(insert_query, (
                    expense.desc, 
                    expense.amount, 
                    expense.time_created, 
                    expense.category, 
                    user.id
                )) 

                select_query = "SELECT id FROM expenses WHERE description = %s AND amount = %s AND time_created = %s AND category = %s"

                cursor.execute(select_query, (
                    expense.desc, 
                    expense.amount, 
                    expense.time_created, 
                    expense.category 
                ))

                expense_id = cursor.fetchone()[0]

                connection.commit()
            except:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Your jwt is invalid.",
                )


    return {'result': expense_id}