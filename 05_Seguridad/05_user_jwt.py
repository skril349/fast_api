from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
import jwt
from fastapi import HTTPException, FastAPI, Depends, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from dotenv import load_dotenv
import os 

# CONFIG (.env)
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", SECRET_KEY)
ALGORITHM = os.getenv("ALGORITHM", ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", ACCESS_TOKEN_EXPIRE_MINUTES))
# Hash password
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

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
        "hashed_password":get_password_hash("password")
    },
    "Alice":{
        "username": "Alice",
        "email":"Alice@example.com",
        "fullname":"Alice Smith",
        "disabled":True,
        "hashed_password":get_password_hash("password2")
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


# FastAPI app
app = FastAPI()

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (ExpiredSignatureError, InvalidTokenError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# FastAPI Endpoints

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    if access_token is None:
        raise HTTPException(status_code=400, detail="Could not create access token")
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user