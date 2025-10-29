from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="Text Analysis Service")

# books = [
#     {
#         "id": 1,
#         "title": "All about Python",
#         "author": "Robert Martin",
#     },
#     {
#         "id": 2,
#         "title": "How to use unit tests  in Python?",
#         "author": "Robert Martin",
#     },
# ]

# @app.get("/books", summary="Отримання всіх книжок", tags=["Книжки"])
# def read_books():
#     return books

# @app.get("/books/{book_id}", summary="Отримання книжки", tags=["Книжки"])
# def get_book(book_id: int):
#     for book in books:
#         if book["id"] == book_id:
#             return book
#     raise HTTPException(status_code=404, detail="Книжка не знайдена")

# class NewBook(BaseModel):
#     title: str
#     author: str

# @app.post("/books", summary="Додавання книжки", tags=["Книжки"])
# def create_book(new_book: NewBook):
#     books.append({
#         "id": len(books) + 1,
#         "title": new_book.title,
#         "author": new_book.author,
#     })
#     return {"success": True, "message": "Книжка успішно додана"}
    
@app.get("/", summary="Отримання базового шляху", tags=["Основні маршрути"])
def home():
    return {"message": "Text Analysis Service is running!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)