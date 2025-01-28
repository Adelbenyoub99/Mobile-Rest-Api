from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="API Mobile", description="API REST pour application mobile")

# Modèle de données
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float

# Simulation d'une base de données
items_db = []
item_id_counter = 1

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Mobile"}

@app.get("/items", response_model=List[Item])
def get_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item non trouvé")
    return item

@app.post("/items", response_model=Item)
def create_item(item: Item):
    global item_id_counter
    new_item = item.dict()
    new_item["id"] = item_id_counter
    item_id_counter += 1
    items_db.append(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    existing_item = next((item for item in items_db if item.id == item_id), None)
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item non trouvé")
    
    item_idx = items_db.index(existing_item)
    update_data = item.dict(exclude_unset=True)
    update_data["id"] = item_id
    items_db[item_idx] = update_data
    return update_data

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item non trouvé")
    
    items_db.remove(item)
    return {"message": "Item supprimé"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)