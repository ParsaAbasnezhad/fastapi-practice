from fastapi import FastAPI, Path, Query, HTTPException, Depends, Response, Cookie
from uuid import UUID
from typing import Annotated, List
from pydantic import BaseModel, Field, EmailStr
# from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models

# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()
#
#
app = FastAPI()


#
#
#
# class Book(BaseModel):
#     title: str = Field(min_length=1, max_length=50)
#     author: str = Field(min_length=1, max_length=50)
#     description: str = Field(min_length=1, max_length=500)
#     rating: int = Field(ge=0, le=100)
#
#
# BOOKS = []
#
#
# @app.get("/")
# def read_api(db: Session = Depends(get_db)):
#     return db.query(models.Books).all()
#
#
# @app.post("/")
# def create_api(book: Book, db: Session = Depends(get_db)):
#     book_model = models.Books()
#     book_model.title = book.title
#     book_model.author = book.author
#     book_model.description = book.description
#     book_model.rating = book.rating
#     db.add(book_model)
#     db.commit()
#
#     return book
#
#
# @app.put('/{book_id}')
# def update_api(book_id: int, book: Book, db: Session = Depends(get_db)):
#     book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
#
#     if book_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Book not found"
#         )
#     book_model = models.Books()
#     book_model.title = book.title
#     book_model.author = book.author
#     book_model.description = book.description
#     book_model.rating = book.rating
#     db.add(book_model)
#     db.commit()
#
#     return book
#
#
# @app.delete('/{book_id}')
# def delete_api(book_id: int, db: Session = Depends(get_db)):
#     book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
#
#     if book_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Book not found"
#         )
#     db.query(models.Books).filter(models.Books.id == book_id).delete()
#     db.commit()
#
#
#
#
# # Login User
#
# class UserBase(BaseModel):
#     username: str = Field(min_length=1, max_length=50)
#     email: EmailStr
#     full_name: str | None = None
#
#
# class UserIn(UserBase):
#     password: str
#
#
# class UserOut(UserBase):
#     pass
#
#
# class UserInDB(UserBase):
#     hashed_password: str
#
#
# def fake_password_hasher(raw_password: str):
#     return 'passwordid' + raw_password
#
#
# def fake_save_user(user_in: UserIn):
#     hasher_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.dict(),
#                           hashed_password=hasher_password)
#     print('User saved')
#     return user_in_db
#
#
# @app.post("/user/", response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved
#

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name='parsa', price=42.3),
        Item(name='pedro', price=5.5),
        Item(name='maria', price=5.5),
    ]


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


from typing import Any


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {'name': "laptob", 'price': 1.00, 'tax': 1.00},
        {'name': "laptob", 'price': 1.00, 'tax': 1.00}
    ]


@app.post('/login')
def login(response: Response):
    response.set_cookie(
        key='username',
        value='admin',
        httponly=True,
        samesite='strict',
        secure=True,
        max_age=86400,
        expires=86400,
        path='/',
    )
    return {'message':"login success" }


@app.post('/logout')
def logout(response: Response):
    response.delete_cookie(
        key='username',
    )
    return {'message':"logout success" }

@app.get("/user")
def get_user(session_id: str | None = Cookie(None)):
    if session_id:
        return {"massage": 'login user'}
    else:
        return {"massage": 'no login user'}