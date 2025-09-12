from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Annotated


class Item(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=50)
    category: Optional[str] = Field(None, min_length=3, max_length=50)
    price: float = Field(..., gt=0)

    @field_validator("price", mode='before')
    @classmethod
    def price_must_be_positive(cls, value) -> int:
        if value <= 0:
            raise ValueError("Price must be positive")
        return value

    @field_validator("category")
    @classmethod
    def category_must_be_string(cls, value) -> str:
        if value is not None and not isinstance(value, str):
            raise ValueError("Category must be a string")
        return value


fake_db = [
    Item(id=1, name="Item 1", category="Category 1", price=10),
    Item(id=2, name="Item 2", category="Category 2", price=20),
    Item(id=3, name="Item 3", category="Category 3", price=30),
]

app = FastAPI()


@app.get("/items/{item_id}",
         response_model=Item,
         status_code=200
    , tags=["Items"],
         summary="Read an item",
         description="Read an item by ID")
def read_item(item_id: int):
    if fake_db[item_id] is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


@app.post("/items/", response_model=Item, status_code=200, tags=["Items"], summary="Post an item",
          description="Post an item by ID")
async def create_item(item: Item):
    fake_db.append(item)
    return item


@app.put("/items/{item_id}", response_model=Item, status_code=200, tags=["Items"], summary="put an item",
         description="put an item by ID")
async def update_item(item_id: int, item: Item):
    if fake_db[item_id] is None:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_db[item_id] = item
    return item


@app.delete("/items/{item_id}", response_model=Item, status_code=200, tags=["Items"], summary="delete an item",
            description="delete an item by ID")
async def delete_item(item_id: int):
    if fake_db[item_id] is None:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_db.pop(item_id)
    return {"message": "Item deleted"}


async def common_parameters(q: str | None = None, skip: int | None = None):
    return {
        "q": q,
        "skip": skip,
    }


@app.get('/products/')
async def read_item(common: Annotated[dict, Depends(common_parameters)])
    return common
