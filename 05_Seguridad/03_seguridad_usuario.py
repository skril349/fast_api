# Oauth 2 --> delegar autenticaciones
# Oauth 1 --> casi obsoleta
# OpenID Connect --> construit sobre Oauth2 (permet login i oauth)
# OpenID --> casi obsoleta
# OpenAPI --> documentació automàtica

###
### Oauth 2 flujo de password + Bearer token
###

from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme : OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl = "token") #  endpoint = /token


class User(BaseModel):
    username: str
    email: str | None = None
    fullname: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str


fake_users_db: dict={
    "johndoe":{
        "username": "johndoe",
        "email":"johndoe@example.com",
        "fullname":"John Doe",
        "disabled":False,
        "hashed_password":"fake_hashed_password"
    },
    "Alice":{
        "username": "Alice",
        "email":"Alice@example.com",
        "fullname":"Alice Smith",
        "disabled":True,
        "hashed_password":"fake_hashed_password2"
    },
    
}


def fake_hash_password(password:str) -> str:
    return "fakehashed" + password

def get_user(db: dict, username: str) -> UserInDB | None:
    if username in db:
        return UserInDB(**db["username"]) # **db... desestructuració per mostrar les dades de User
    return None

def fake_decode_token(token:str) -> UserInDB | None:
    return get_user(fake_users_db, token)


async def get_current_user(token: Annotated[str,Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user




@app.get("/items")
async def get_items(token: Annotated[str,Depends(oauth2_scheme)]):
    return { " token": token}

