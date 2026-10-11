from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_existing_product():
    response = client.get("/products/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Mechanical Keyboard"
    assert data["price"] == 249.99
    assert data["stock"] == 15



def test_get_nonexistent_product():
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_get_product_with_invalid_id():
    response = client.get("/products/abc")

    assert response.status_code == 422


def test_create_product_successfully():
    response = client.post(
        "/products",
        json={
            "name": "Test Monitor",
            "price": 599.99,
            "stock": 8,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Monitor"
    assert data["price"] == 599.99
    assert data["stock"] == 8
    assert "id" in data


def test_create_product_with_negative_price():
    response = client.post(
        "/products",
        json={
            "name": "Invalid Product",
            "price": -10,
            "stock": 5,
        },
    )

    assert response.status_code == 422


def test_create_product_with_negative_stock():
    response = client.post(
        "/products",
        json={
            "name": "Invalid Stock Product",
            "price": 49.99,
            "stock": -3,
        },
    )

    assert response.status_code == 422


def test_get_products_returns_seeded_products(client):
    response = client.get("/products")

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 3
    assert products[0]["name"] == "Mechanical Keyboard"
    assert products[1]["name"] == "Gaming Mouse"
    assert products[2]["name"] == "USB-C Hub"


def test_create_product_with_empty_name(client):
    response = client.post(
        "/products",
        json={
            "name": "",
            "price": 49.99,
            "stock": 5,
        },
    )

    assert response.status_code == 422


def test_create_product_with_zero_stock(client):
    response = client.post(
        "/products",
        json={
            "name": "Out of Stock Product",
            "price": 49.99,
            "stock": 0,
        },
    )

    assert response.status_code == 201

    product = response.json()
    assert product["stock"] == 0


def test_create_product_with_zero_price(client):
    response = client.post(
        "/products",
        json={
            "name": "Free Product",
            "price": 0,
            "stock": 5,
        },
    )

    assert response.status_code == 422


def test_create_product_with_name_too_long(client):
    response = client.post(
        "/products",
        json={
            "name": "A" * 101,
            "price": 49.99,
            "stock": 5,
        },
    )

    assert response.status_code == 422