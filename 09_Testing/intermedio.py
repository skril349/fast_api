from fastapi import FastAPI, Header , HTTPException
from typing import Annotated
from pydantic import BaseModel

fake_secret_token = "secret-token"

class User(BaseModel):
    id: str
    username: str | None = None
    email: str | None = None

fake_user_db : dict[str, User] = {
    "1": User(id="1", username="userone", email="user1@gmail.com"),
    "2": User(id="2", username="usertwo", email="user2@gmail.com"),
}

app = FastAPI()

@app.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    x_token: Annotated[str | None, Header()] = None
):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    if user_id not in fake_user_db:
        raise HTTPException(status_code=400, detail="User not found")
    return fake_user_db[user_id]

@app.post("/users/", response_model=User)
async def create_user(user: User, x_token: Annotated[str | None, Header()] = None):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    if user.id in fake_user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_user_db[user.id] = user
    return user
