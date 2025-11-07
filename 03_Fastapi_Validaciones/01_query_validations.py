from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import AfterValidator

app = FastAPI()

# STRINGS VALIDATIONS
# max_length
# min_length
# pattern

# NUMBERS VALIDATIONS
# gt : greater than
# ge : greater than or equal
# lt : less than
# le : less than or equal

# METADATA

# title
# description
# alias
# deprecated

@app.get("/items/")
async def read_items(q: Annotated[
    str | None,
    Query(min_length=3,
           max_length=20,
           title="Query",
           description="lo que se va a buscar",
           alias="item-query")
    ] = None):
    results: dict = {"mensaje": "Acceso a get(read_items)"}
    if q:
        results.update({"q":q})
    return results


@app.get("/objects/")
async def read_objects(q: Annotated[int | None,Query(gt=3)] = None):
    results: dict = {"mensaje": "Acceso a get(read_objects)"}
    if q:
        results.update({"q":q})
    return results


def check_valid_id(id: str):
    if id % 2 != 0:
        raise ValueError("Necesita ser par")
    return id

@app.get("/check-id/")
async def check_id(q: Annotated[
    int | None,
    AfterValidator(check_valid_id)
    ] = None):
    results: dict = {"mensaje": "Acceso a get(check_id)"}
    if q:
        results.update({"q":q})
    return results