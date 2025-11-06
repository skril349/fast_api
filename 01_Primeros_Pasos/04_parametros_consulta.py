from fastapi import FastAPI

app = FastAPI()

cars_list : list[dict] = [
    {"car_name":"Elantra"},
    {"car_name":"Civic"},
    {"car_name":"Sentra"},
    {"car_name":"Corola"},
]

# http://localhost:8000/cars/?limit=2&skip=2
@app.get("/cars/")
async def get_cars(skip: int = 0 , limit:int = 10):
    return cars_list[skip:skip+limit]