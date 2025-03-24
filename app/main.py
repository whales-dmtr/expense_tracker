from fastapi import FastAPI
from app.authentication import auth_router

app = FastAPI()

app.include_router(auth_router)