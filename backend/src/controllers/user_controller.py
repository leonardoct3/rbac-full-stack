from fastapi import APIRouter, Depends, HTTPException
from database.database import get_db

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@user_router.post("/", response_model=dict)
def create_user(user: dict, dependencies: dict = Depends(get_db)):
    # Here you would typically interact with the database to create a new user
    # For demonstration purposes, we'll just return the input as a response
    return {"message": "User created successfully", "user": user}