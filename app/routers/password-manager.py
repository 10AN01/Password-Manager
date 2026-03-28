from app.models.user import InsertPassword
from app.security.encryption import hash_password
from app.security.auth import get_current_user
from app.database.db import insert_data
from auth import payload


from fastapi import APIRouter, HTTPException,Response,Depends
from datetime import datetime,timedelta, timezone

router = APIRouter(prefix="/password-manager")

# Allows user to insert passwords
@router.post("/save-passwords")
def insert_password(data:InsertPassword,current_user = Depends(get_current_user)):
    hashed_password = hash_password(data.password)
    insert_data(current_user[0],data.site_link,data.username,data.email,hashed_password)
    
    
    