from fastapi import APIRouter, Depends, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from src.database.database import get_db
from sqlalchemy.orm import Session
from src.entities.user import UserCreate
from src.services.auth_service import AuthService
from pydantic import BaseModel
from src.middlewares.get_current_user import get_current_user

user_router = APIRouter(
    prefix="/auth",
    tags=["users"]
)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    hashed_password: str

    class Config:
        from_attributes = True

def init_service(db: Session = Depends(get_db)):
    return AuthService(db)

@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register(user: UserCreate, service: AuthService = Depends(init_service)):
    return service.register_user(user)

@user_router.post("/login", status_code=status.HTTP_200_OK, response_model=dict)
def login(dto: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(init_service)):
    return service.login(dto)

@user_router.get("/me", status_code=status.HTTP_200_OK)
def me(current_user: dict = Depends(get_current_user), response_model=UserResponse):
    return current_user

@user_router.post("/refresh")
def refresh(refresh_token : str = Body(...), service : AuthService = Depends(init_service)):
    return service.refresh(refresh_token)