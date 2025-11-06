from fastapi import FastAPI, Query
from typing import Annotated

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

@app.get("/items/")
async def read_items(q: Annotated[str | None,Query(min_length=3, max_length=20)] = None):
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

