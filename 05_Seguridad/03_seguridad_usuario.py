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



@app.get("/items")
async def get_items(token: Annotated[str,Depends(oauth2_scheme)]):
    return { " token": token}

