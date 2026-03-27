from app.models.user import InsertPassword
from app.security.encryption import hash_password
from app.database.db import insert_data


from fastapi import APIRouter, HTTPException,Response,Depends
from datetime import datetime,timedelta, timezone

router = APIRouter(prefix="/password-manager")

@router.post("/insert_password")
def insert_password(data:InsertPassword,current_user = Depends(get_current_user)):
    hashed_password = hash_password(data.password)
    insert_data(current_user.user_id,data.site_link,data.username,data.email,hashed_password)
    
    