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

app = FastAPI()

oauth2_scheme : OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl = "token") #  endpoint = /token

@app.get("/items")
async def get_items(token: Annotated[str,Depends(oauth2_scheme)]):
    return { " token": token}