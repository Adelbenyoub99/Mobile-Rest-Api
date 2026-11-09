"""
Automated Integration Tests for Mobile REST API
Run with: pytest
"""

from fastapi.testclient import TestClient
from main import app, init_db

client = TestClient(app)


def setup_module(module):
    init_db()


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "version" in data


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_crud_lifecycle():
    # 1. Create a new item
    new_item = {
        "name": "iPad Pro M4",
        "description": "Tablette tactile 11 pouces avec écran OLED",
        "category": "Tablettes",
        "price": 1199.00,
        "in_stock": True
    }
    create_res = client.post("/items", json=new_item)
    assert create_res.status_code == 201
    created = create_res.json()
    item_id = created["id"]
    assert created["name"] == new_item["name"]
    assert created["price"] == new_item["price"]

    # 2. Get item by ID
    get_res = client.get(f"/items/{item_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == item_id

    # 3. Update the item
    update_data = {"price": 1099.00, "in_stock": False}
    update_res = client.put(f"/items/{item_id}", json=update_data)
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["price"] == 1099.00
    assert updated["in_stock"] is False

    # 4. Search item in list
    list_res = client.get("/items?search=iPad")
    assert list_res.status_code == 200
    items = list_res.json()
    assert any(i["id"] == item_id for i in items)

    # 5. Delete the item
    del_res = client.delete(f"/items/{item_id}")
    assert del_res.status_code == 200

    # 6. Verify 404 on deleted item
    get_after_del = client.get(f"/items/{item_id}")
    assert get_after_del.status_code == 404

