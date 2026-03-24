from fastapi import FastAPI
from .routers import auth
from app.database.db import create_table_users, create_table_passwords

app = FastAPI()

app.include_router(auth.router)