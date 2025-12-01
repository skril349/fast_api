from fastapi import FastAPI, Depends
import time 
import asyncio 

app = FastAPI()

@app.get("/async-sin-await")
async def async_sin_await():
    print("hola")
    time.sleep(5)  # Simula una operacion bloqueante
    print("adios")

@app.get("/async-con-await")
async def async_endpoint():
    print("hola")
    await asyncio.sleep(5)  # Simula una operacion no bloqueante
    print("adios")

@app.get("/sync-endpoint")
def sync_endpoint():
    print("hola")
    time.sleep(5)  # Simula una operacion bloqueante
    print("adios")