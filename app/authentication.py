from fastapi import APIRouter
from app.schemas import LoginValidation, RegisterValidation
from dotenv import load_dotenv
import psycopg2
import os

auth_router = APIRouter()
load_dotenv()   


@auth_router.get('/login')
def login(user: LoginValidation) -> dict[str, str]:    
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )
    
    cur = conn.cursor()

    cur.execute(f"""SELECT password FROM users 
                    WHERE username = '{user.username}' AND password = '{user.password}'""")

    if cur.fetchone() is not None:
        return {'logged_in': 'True'}
    else:
        return {'logged_in': 'False'}


@auth_router.post('/register')
def register(user: RegisterValidation) -> dict[str, str]:
    connection = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )
    
    cursor = connection.cursor()
    cursor.execute(f"""INSERT INTO users (id, username, password, email) 
                       VALUES (nextval('users_id_seq'), '{user.username}', '{user.password}', '{user.email}')""")

    cursor.execute(f"""SELECT * FROM users 
                    WHERE username = '{user.username}' AND password = '{user.password}'""")
    user_data = str(cursor.fetchone())

    connection.commit()

    cursor.close()
    connection.close()

    return {'user': user_data}