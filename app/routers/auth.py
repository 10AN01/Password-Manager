from fastapi import APIRouter, HTTPException,Response
from app.database.db import insert_account,account_check
from app.security.encryption import hash_password,verify_password
from app.models.user import LoginAccount,RegisterAccount

import uuid
from datetime import datetime,timedelta, timezone
from jose import jwt
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
router = APIRouter(prefix="/auth")

@router.post("/register")
def register(user:RegisterAccount):
# Creates a unique UUID for the user
    user_id = str(uuid.uuid4())
# Hashes password before it gets into the database
    hashed_password = hash_password(user.password)
# Creates a date
    created_at = str(datetime.now())
# Inserts accounts into the database
    insert_account(user_id,user.email,hashed_password,created_at)
    return {"message": "Account created"}

@router.post("/login")
def login(user:LoginAccount,response:Response):
# Gets row where user entered email
    db_user = account_check(user.email)
# Doesn't exist then raise error
    if not db_user:
        raise HTTPException(status_code=401,detail="Invalid credentials")
# Verify password
    stored_password = db_user[2]
    verify = verify_password(user.password,stored_password)
    if not verify:
        raise HTTPException(status_code=401,detail="Invalid credentials")
# Gives user a JWT TOKEN.
    expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    user_id = db_user[0]
    payload = {
    "sub": user_id,
    "exp": expires
    }
    JWT_TOKEN = jwt.encode(
    payload,
    SECRET_KEY,
    algorithm="HS256"
    )
    response.set_cookie(
    key="access_token",
    value=JWT_TOKEN,
    httponly=True,
    secure=True,
    samesite="Strict"
)
    return {"message":"Successfully logged in!"}