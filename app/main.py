from fastapi import FastAPI
import app.authentication as auth

app = FastAPI()

app.include_router(auth.router)