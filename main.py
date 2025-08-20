from fastapi import FastAPI, Path, Query, HTTPException, Depends
from uuid import UUID
from typing import Annotated
from pydantic import BaseModel, Field

from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app = FastAPI()


class Book(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    author: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=500)
    rating: int = Field(ge=0, le=100)


BOOKS = []


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Books).all()


@app.post("/")
def create_api(book: Book, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating
    db.add(book_model)
    db.commit()

    return book


@app.put('/{book_id}')
def update_api(book_id: int, book: Book, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating
    db.add(book_model)
    db.commit()

    return book


@app.delete('/{book_id}')
def delete_api(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    db.query(models.Books).filter(models.Books.id == book_id).delete()
    db.commit()
