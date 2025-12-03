from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, Optional
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    nombre:str
    email: str
    edad: int | None = None
    activo: Optional[bool]

class AuthService:
    def authenticate(self, token:str):
        if token == "Valid-token":
            return True
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

def get_auth_service():
    return AuthService()

class EmailService:
    def send_email(self, recipient:str, message:str):
        print(f"Sending email to {recipient}: {message}")

def get_email_service():
    return EmailService()


class Logger:
    def log(self,message:str)-> None:
        print(f"logging message:{message}")

def get_logger():
    return Logger()


logger_dependency = Annotated[Logger,Depends(get_logger)]
email_service_dependency = Annotated[EmailService, Depends(get_email_service)]
auth_service_dependency = Annotated[AuthService, Depends(get_auth_service)]

@app.get("/items/{message}")
async def get_items(message:str, logger:logger_dependency):
    logger.log(message)
    return message

@app.get("/products/{message}")
async def get_products(message:str, logger:logger_dependency):
    logger.log(message)
    return message

def send_email(recipient:str, message:str, email_service: email_service_dependency):
    email_service.send_email(recipient, message)

@app.get("/secure-data/")
def get_secure_data(token:str, auth_service: auth_service_dependency):
    if auth_service.authenticate(token):
        return "authenticated"
    else:
        return "unauthenticated"
    

@app.post("/users/")
async def create_user(user:User):
    return {
        "mensaje": f"Usuario {user.nombre.capitalize()} creado exitosamente",
        "datos":user

    }

@app.put("users/{user_id}")
async def edit_user(user_id:int, user:User):
    return {"user_id":user_id,**user.model_dump()}