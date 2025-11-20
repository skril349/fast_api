from fastapi import FastAPI, Request, Response 
import time
from typing import Callable

app = FastAPI()



# Middleware example

@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable) -> Response:
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response




@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/slow")
async def slow_route():
    time.sleep(2)
    return {"message": "Hello slooow"}