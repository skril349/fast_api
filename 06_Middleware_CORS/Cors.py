# CORS --> Cross-Origin Resource Sharing
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI() 
origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://www.example.com",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}