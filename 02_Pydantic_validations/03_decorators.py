from pydantic import BaseModel, AfterValidator, field_validator
from typing import Annotated
from fastapi import FastAPI

class Item(BaseModel):
    item_id: int
    price: float

    @field_validator("item_id", mode="after")
    def check_positive(cls,value:int):
        if value < 0:
            raise ValueError("Item ID debe ser positivo")
        return value

banana: Item = Item(item_id = 2, price = 2.6)

