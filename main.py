"""
Mobile REST API - Production-Ready Backend Showcase
FastAPI REST API with SQLite persistence, CORS support, and comprehensive CRUD operations.
Author: Adel BENYOUB (https://github.com/Adelbenyoub99)
"""

import sqlite3
from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Database Initialization (SQLite)
# ---------------------------------------------------------------------------
DB_FILE = "mobile_store.db"


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'Général',
                price REAL NOT NULL,
                in_stock INTEGER NOT NULL DEFAULT 1
            )
        """)
        # Seed initial sample data if empty
        cursor = conn.execute("SELECT COUNT(*) AS count FROM items")
        if cursor.fetchone()["count"] == 0:
            sample_items = [
                ("iPhone 15 Pro", "Smartphone Apple 128 Go Titane Naturel", "Smartphones", 1299.99, 1),
                ("Samsung Galaxy S24 Ultra", "Smartphone Android 256 Go Gris Titane", "Smartphones", 1349.00, 1),
                ("MacBook Air M3", "Ordinateur portable 13 pouces 16 Go RAM", "Informatique", 1499.00, 1),
                ("AirPods Pro 2", "Écouteurs sans fil avec réduction active du bruit", "Audio", 279.00, 1),
                ("Sony WH-1000XM5", "Casque audio Bluetooth à réduction de bruit", "Audio", 349.90, 1)
            ]
            conn.executemany(
                "INSERT INTO items (name, description, category, price, in_stock) VALUES (?, ?, ?, ?, ?)",
                sample_items
            )
        conn.commit()


# ---------------------------------------------------------------------------
# Lifecycle Manager
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


# ---------------------------------------------------------------------------
# FastAPI App Definition & CORS
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Mobile Product Catalog REST API",
    description="API RESTful haute performance conçue pour les applications mobiles et web modernes. "
                "Inclut persistance SQLite, validation des données avec Pydantic v2, documentation interactive Swagger et support CORS.",
    version="1.2.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------
class ItemBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120, description="Nom du produit")
    description: str = Field(..., min_length=5, description="Description détaillée")
    category: str = Field(default="Général", description="Catégorie du produit")
    price: float = Field(..., gt=0, description="Prix unitaire positif")
    in_stock: bool = Field(default=True, description="Disponibilité en stock")


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    description: Optional[str] = Field(None, min_length=5)
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    in_stock: Optional[bool] = None


class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health & Info"])
def root():
    return {
        "status": "online",
        "service": "Mobile Product Catalog REST API",
        "version": "1.2.0",
        "docs_url": "/docs",
        "author": "Adel BENYOUB"
    }


@app.get("/health", tags=["Health & Info"])
def health_check():
    return {"status": "healthy", "database": "connected"}


@app.get("/items", response_model=List[ItemResponse], tags=["Products"])
def get_items(
    search: Optional[str] = Query(None, description="Recherche par nom ou description"),
    category: Optional[str] = Query(None, description="Filtrer par catégorie"),
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter (pagination)"),
    limit: int = Query(50, ge=1, le=100, description="Nombre maximum d'éléments retournés")
):
    query = "SELECT * FROM items WHERE 1=1"
    params = []

    if search:
        query += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, skip])

    with get_db_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [
            ItemResponse(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                category=row["category"],
                price=row["price"],
                in_stock=bool(row["in_stock"])
            )
            for row in rows
        ]


@app.get("/items/{item_id}", response_model=ItemResponse, tags=["Products"])
def get_item(item_id: int):
    with get_db_connection() as conn:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produit avec l'identifiant #{item_id} introuvable."
            )
        return ItemResponse(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            category=row["category"],
            price=row["price"],
            in_stock=bool(row["in_stock"])
        )


@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_item(payload: ItemCreate):
    with get_db_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO items (name, description, category, price, in_stock) VALUES (?, ?, ?, ?, ?)",
            (payload.name, payload.description, payload.category, payload.price, int(payload.in_stock))
        )
        conn.commit()
        new_id = cursor.lastrowid
        return ItemResponse(id=new_id, **payload.model_dump())


@app.put("/items/{item_id}", response_model=ItemResponse, tags=["Products"])
def update_item(item_id: int, payload: ItemUpdate):
    with get_db_connection() as conn:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Impossible de mettre à jour : produit #{item_id} introuvable."
            )

        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aucun champ valide fourni pour la mise à jour."
            )

        fields = []
        values = []
        for key, val in update_data.items():
            fields.append(f"{key} = ?")
            values.append(int(val) if isinstance(val, bool) else val)

        values.append(item_id)
        conn.execute(f"UPDATE items SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()

        updated_row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        return ItemResponse(
            id=updated_row["id"],
            name=updated_row["name"],
            description=updated_row["description"],
            category=updated_row["category"],
            price=updated_row["price"],
            in_stock=bool(updated_row["in_stock"])
        )


@app.delete("/items/{item_id}", status_code=status.HTTP_200_OK, tags=["Products"])
def delete_item(item_id: int):
    with get_db_connection() as conn:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Impossible de supprimer : produit #{item_id} introuvable."
            )
        conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        return {"message": f"Produit #{item_id} supprimé avec succès."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
