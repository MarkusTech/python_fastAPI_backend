from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory database
fake_db = []


# Pydantic models for request and response data validation
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# Routes for CRUD operations
@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10):
    return fake_db[skip : skip + limit]


@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id < len(fake_db):
        return fake_db[item_id]
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items/", response_model=Item)
def create_item(item: Item):
    fake_db.append(item)
    return item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id < len(fake_db):
        fake_db[item_id] = item
        return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    if item_id < len(fake_db):
        deleted_item = fake_db.pop(item_id)
        return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")
