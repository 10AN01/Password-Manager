from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from dotenv import load_dotenv
import os


from app.database.db import account_check
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Gets JWT Token and finds the UUID of the user.
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload["sub"]
    user = account_check(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user