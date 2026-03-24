from pydantic import BaseModel
class RegisterAccount(BaseModel):
    email:str
    password:str
    
class LoginAccount(BaseModel):
    email:str
    password:str