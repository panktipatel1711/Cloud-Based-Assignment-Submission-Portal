from pydantic import BaseModel, EmailStr
from typing import Literal

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["student", "teacher"]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
