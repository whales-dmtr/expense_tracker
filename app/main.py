from fastapi import FastAPI

import app.routers.authentication as auth
import app.routers.expenses as exp
import app.routers.search as search
import app.routers.user as routs

app = FastAPI()

app.include_router(auth.router)
app.include_router(exp.router)
app.include_router(search.router)
app.include_router(routs.router)
