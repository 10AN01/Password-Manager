from fastapi import FastAPI
from .routers import auth
from app.database.db import create_table_users, create_table_passwords
from app.database.db import create_table_passwords
app = FastAPI()

create_table_passwords()
app.include_router(auth.router)