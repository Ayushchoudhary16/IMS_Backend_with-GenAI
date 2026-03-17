from pydantic import BaseModel, EmailStr 
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class loginUserSchema(BaseModel):
    email: EmailStr
    password: str

class UpdateUserSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None