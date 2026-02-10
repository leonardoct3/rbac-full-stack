from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
import jwt
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database.database import get_db
from src.models.user import User

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Decode the JWT token. If invalid or expired, this will raise an exception.
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        # Token has expired
        raise HTTPException(status_code=401, detail="Access token expired")
    except jwt.InvalidTokenError:
        # Token is invalid in general
        raise HTTPException(status_code=401, detail="Invalid token")

    # Token is decoded. Extract user identity.
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    # Find the user in our database
    stmt = select(User).where(User.email == username)
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user