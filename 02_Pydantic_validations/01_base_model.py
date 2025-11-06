from pydantic import BaseModel
from fastapi import FastAPI

class User(BaseModel):
    id: int
    nombre:str
    email:str
    edad:int | None = None
    activo:bool

app = FastAPI()


@app.get("/users/")
async def get_users():
    ... 

@app.post("/users/")
async def create_user(user:User):
    return {
        "mensaje":f"usuario {user.nombre.capitalize()} creado exitosamente",
        "datos": user
    }