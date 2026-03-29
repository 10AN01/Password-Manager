from pydantic import BaseModel
class RegisterAccount(BaseModel):
    email:str
    password:str
    
class LoginAccount(BaseModel):
    email:str
    password:str

class InsertPassword(BaseModel):
    site_link:str
    username:str
    email:str
    password:str

class DecryptRequest(BaseModel):
    encrypted_password: str