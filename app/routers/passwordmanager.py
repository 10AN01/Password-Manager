from app.models.user import InsertPassword
from app.security.encryption import encrypt_password
from app.security.auth import get_current_user
from app.database.db import insert_data,get_passwords_by_user
import uuid
from app.models.user import DecryptRequest
from fastapi import APIRouter, HTTPException,Response,Depends
from datetime import datetime,timedelta, timezone

router = APIRouter()

# Allows user to insert passwords
@router.post("/save-passwords")
def insert_password(data: InsertPassword, current_user=Depends(get_current_user)):
    try:
        encrypted_password = encrypt_password(data.password)
        password_id = str(uuid.uuid4())
        created_at = str(datetime.now())
        insert_data(
            password_id,
            current_user[0],
            data.site_link,
            data.username,
            data.email,
            encrypted_password,
            created_at
        )
        return {"message": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Gets password depending on UUID
@router.get("/passwords")
def get_passwords(user = Depends(get_current_user)):
    user_id = user[0]
    
    passwords = get_passwords_by_user(user_id)

    return passwords
# Decrypts password
@router.post("/decrypt-password")
def decrypt_password_endpoint(
    data: DecryptRequest,
    current_user = Depends(get_current_user)
):
    from app.security.encryption import decrypt_password
    try:
        decrypted = decrypt_password(data.encrypted_password)
        return {"password": decrypted}
    except Exception as e:
        print("DECRYPT ERROR:", e)
        raise HTTPException(status_code=400, detail="Could not decrypt password")
    
    
    