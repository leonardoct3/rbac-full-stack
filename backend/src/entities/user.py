from pydantic import BaseModel

class UserCreate(BaseModel):
    id: int
    name: str
    fullname: str | None = None

    class Config:
        orm_mode = True