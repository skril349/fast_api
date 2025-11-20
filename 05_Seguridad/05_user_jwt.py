from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import HTTPException, FastAPI, Depends, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext

# CONFIG (.env)
SECRET_KEY = "99841f84c2055e0f75249901d6cd9639"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

# FAKE DB
fake_users_db: dict={
    "johndoe":{
        "username": "johndoe",
        "email":"johndoe@example.com",
        "fullname":"John Doe",
        "disabled":False,
        "hashed_password":get_password_hash("secret")
    },
    "Alice":{
        "username": "Alice",
        "email":"Alice@example.com",
        "fullname":"Alice Smith",
        "disabled":True,
        "hashed_password":get_password_hash("secret2")
    },
}

# Models

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None
    email: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

# Auth Helpers
def get_user(db:dict,username:str) -> UserInDB | None:
    user_data = db.get(username)
    if user_data:
        return UserInDB(**user_data)
    return None

def authenticate_user(fake_db:dict, username:str, password:str) -> UserInDB | bool:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

