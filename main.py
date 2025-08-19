from fastapi import FastAPI, Path, Query, HTTPException
from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


# class Image(BaseModel):
#     url: HttpUrl
#     title: str
#
#
# class Item(BaseModel):
#     title: str = Annotated[
#         str, Field(min_length=1, max_length=30, title='name item', description='this is a item in form')]
#     description: str
#     price: float
#     tax: float | None = None
#     image: set[Image] = set()
#
#
# class Items(BaseModel):
#     items: list[Item]
#     body: str
#
#
# @app.post("/items")
# async def create_item(items: Items):
#     return items
#
#


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=500)
    rating: int = Field(ge=0, le=100)


BOOKS = []


@app.get("/")
def read_api():
    return BOOKS


@app.post("/")
def create_api(book: Book):
    BOOKS.append(book)
    return book


@app.put('/{book_id}')
def update_api(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return book
    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


@app.delete('/{book_id}')
def delete_api(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1

        if x.id == book_id:
            del BOOKS[counter - 1]
            return f"Book {book_id} deleted"
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
