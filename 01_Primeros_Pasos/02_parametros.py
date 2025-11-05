from fastapi import FastAPI

app = FastAPI()

@app.get("/books/favourite")
async def get_favourite():
    return{"favourite book": "game of thrones"}

@app.get("/books/{book_id}")
async def get_book(book_id: str):
    return {"book_id":book_id}