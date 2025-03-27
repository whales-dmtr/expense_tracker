from fastapi import APIRouter
from app.schemas import LoginValidation, RegisterValidation
from dotenv import load_dotenv
from argon2 import PasswordHasher
import psycopg2
import os

router = APIRouter()
load_dotenv()


@router.get('/login')
def login(user: LoginValidation) -> dict[str, str]:
    with psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    ) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"""SELECT password FROM users 
                                WHERE username = '{user.username}'""")

                true_user_pass_hash = cursor.fetchone()[0]
                True if true_user_pass_hash is not None else False

                ph = PasswordHasher()
                ph.verify(true_user_pass_hash, user.password)

                return {'logged_in': 'True'}
            except:
                return {'logged_in': 'False'}


@router.post('/register')
def register(user: RegisterValidation) -> dict[str, str]:
    with psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    ) as connection:
        with connection.cursor() as cursor:
            ph = PasswordHasher()
            hashed_password = ph.hash(user.password)
            cursor.execute(f"""INSERT INTO users (id, username, password, email) 
                            VALUES (nextval('users_id_seq'), '{user.username}', '{hashed_password}', '{user.email}')""")

            cursor.execute(f"""SELECT * FROM users 
                            WHERE username = '{user.username}'""")
            user_data = str(cursor.fetchone())

            connection.commit()

            return {'user': user_data}
