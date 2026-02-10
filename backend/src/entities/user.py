from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    password: str
    email: EmailStr
    fullname: Optional[str] = None

    class Config:
        from_attributes = True
