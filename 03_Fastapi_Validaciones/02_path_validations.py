from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id:Annotated[int, Path(ge=1, title=" ID OF ITEM")],
    q:Annotated[str | None ,
    Query(alias="item-query")] = None):
    ...