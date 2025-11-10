from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

app = FastAPI()

class Logger:
    def log(self,message:str)-> None:
        print(f"logging message:{message}")

def get_logger():
    return Logger()

logger_dependency = Annotated[Logger,Depends(get_logger)]



@app.get("/items/{message}")
async def get_items(message:str, logger:logger_dependency):
    logger.log(message)
    return message

@app.get("/products/{message}")
async def get_products(message:str, logger:logger_dependency):
    logger.log(message)
    return message
