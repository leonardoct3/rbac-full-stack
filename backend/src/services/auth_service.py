from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from src.entities.user import UserCreate
from src.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import select
import bcrypt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_create: UserCreate) -> User:
        hashed_password = bcrypt.hashpw(user_create.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(name=user_create.name, email=user_create.email, fullname=user_create.fullname, hashed_password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def login(self, dto: OAuth2PasswordRequestForm) -> dict:
        # Check if user exists
        stmt = select(User).where(User.email == dto.username)
        user = self.db.execute(stmt).scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not bcrypt.checkpw(
            dto.password.encode('utf-8'), 
            user.hashed_password.encode('utf-8')
        ):
            raise HTTPException(status_code=401, detail="Password incorrect")
        
         # Create JWT payloads for tokens
        access_exp = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_payload = {"sub": user.email, "exp": access_exp}
        refresh_exp = datetime.utcnow() + timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))
        refresh_payload = {"sub": user.email, "exp": refresh_exp, "token_type": "refresh"}
    
        # Encode JWT tokens
        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)
        
        # Return tokens to the client
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    
    def refresh(self, refresh_token: str):
            # Decode and validate the refresh token
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Ensure this token is a refresh token
        if payload.get("token_type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        # Get the user identity from token
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Check user existance
        stmt = select(User).where(User.email == username)
        user = self.db.execute(stmt).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User does not exist")

        # Create a new access token for this user
        new_access_exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_payload = {"sub": username, "exp": new_access_exp}
        new_access_token = jwt.encode(new_access_payload, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": new_access_token, "token_type": "bearer"}