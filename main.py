from fastapi import FastAPI, Path, Query
from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    title: str


class Item(BaseModel):
    title: str = Annotated[
        str, Field(min_length=1, max_length=30, title='name item', description='this is a item in form')]
    description: str
    price: float
    tax: float | None = None
    image: set[Image] = set()


class Items(BaseModel):
    items: list[Item]
    body: str


@app.post("/items")
async def create_item(items: Items):
    return items
