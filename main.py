from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List
from pydantic import BaseModel

# Define the Pydantic models
class Item(BaseModel):
    name: str
    description: str

class ItemInDB(Item):
    id: str

# Initialize FastAPI
app = FastAPI()

# MongoDB connection

url = "mongodb+srv://sanjay:dSZmUoxGJCVrrD3F@cluster0.iyvqhox.mongodb.net/sqfeet"
client = MongoClient(url)
db = client.sqfeet
collection = db.items

@app.post("/items/", response_model=ItemInDB)
def create_item(item: Item):
    item_dict = item.dict()
    result = collection.insert_one(item_dict)
    item_dict['id'] = str(result.inserted_id)
    return item_dict

@app.get("/items/{item_id}", response_model=ItemInDB)
def read_item(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item['id'] = str(item['_id'])
    return item

@app.get("/items/", response_model=List[ItemInDB])
def read_items():
    items = []
    for item in collection.find():
        item['id'] = str(item['_id'])
        items.append(item)
    return items

