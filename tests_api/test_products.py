import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import database

def test_get_existing_product(client):
    response = client.get("/products/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Mechanical Keyboard"
    assert data["price"] == 249.99
    assert data["stock"] == 15


def test_get_nonexistent_product(client):
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_get_product_with_invalid_id(client):
    response = client.get("/products/abc")

    assert response.status_code == 422


def test_create_product_successfully(client):
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


def test_create_product_with_negative_price(client):
    response = client.post(
        "/products",
        json={
            "name": "Invalid Product",
            "price": -10,
            "stock": 5,
        },
    )

    assert response.status_code == 422


def test_create_product_with_negative_stock(client):
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


def test_initialize_database_seeds_empty_database(tmp_path, monkeypatch):
    test_database_path = tmp_path / "new_database.db"
    monkeypatch.setattr(database, "DATABASE_PATH", test_database_path)

    database.initialize_database()

    with database.get_connection() as connection:
        products = connection.execute(
            "SELECT name, price, stock FROM products ORDER BY id"
        ).fetchall()

    assert len(products) == 3
    assert products[0]["name"] == "Mechanical Keyboard"
    assert products[1]["name"] == "Gaming Mouse"
    assert products[2]["name"] == "USB-C Hub"


def test_initialize_database_does_not_duplicate_seeded_products(
    tmp_path, monkeypatch
):
    test_database_path = tmp_path / "existing_database.db"
    monkeypatch.setattr(database, "DATABASE_PATH", test_database_path)

    database.initialize_database()
    database.initialize_database()

    with database.get_connection() as connection:
        product_count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

    assert product_count == 3


def test_get_connection_rolls_back_and_closes_on_error(
    tmp_path, monkeypatch
):
    test_database_path = tmp_path / "rollback_database.db"
    monkeypatch.setattr(database, "DATABASE_PATH", test_database_path)

    with database.get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE test_items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            """
        )

    try:
        with database.get_connection() as connection:
            connection.execute(
                "INSERT INTO test_items (name) VALUES (?)",
                ("Temporary item",),
            )
            raise ValueError("Simulated failure")
    except ValueError as error:
        assert str(error) == "Simulated failure"

    with database.get_connection() as connection:
        item_count = connection.execute(
            "SELECT COUNT(*) FROM test_items"
        ).fetchone()[0]

    assert item_count == 0


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the QA Automation API!",
        "status": "running",
    }


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_product_with_whitespace_only_name(client):
    response = client.post(
        "/products",
        json={
            "name": "   ",
            "price": 49.99,
            "stock": 5,
        },
    )

    assert response.status_code == 422


def test_create_product_trims_whitespace_from_name(client):
    response = client.post(
        "/products",
        json={
            "name": "   Monitor   ",
            "price": 499.99,
            "stock": 10,
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Monitor"


def test_create_product_with_string_price(client):
    response = client.post(
        "/products",
        json={
            "name": "Invalid Price Type",
            "price": "not-a-number",
            "stock": 5,
        },
    )

    assert response.status_code == 422


def test_create_product_without_name(client):
    response = client.post(
        "/products",
        json={
            "price": 10.0,
            "stock": 5,
        },
    )

    assert response.status_code == 422


def test_create_product_with_string_stock(client):
    response = client.post(
        "/products",
        json={
            "name": "Invalid Stock Type",
            "price": 10.0,
            "stock": "not-a-number",
        },
    )

    assert response.status_code == 422


def test_database_script_initializes_database(tmp_path):
    project_root = Path(__file__).resolve().parent.parent
    database_script = project_root / "database.py"
    temporary_database = tmp_path / "script_test.db"

    environment = os.environ.copy()
    environment["QA_DATABASE_PATH"] = str(temporary_database)

    result = subprocess.run(
        [sys.executable, str(database_script)],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert str(temporary_database) in result.stdout
    assert temporary_database.exists()

    connection = sqlite3.connect(temporary_database)

    try:
        products = connection.execute(
            "SELECT name, price, stock FROM products ORDER BY id"
        ).fetchall()
    finally:
        connection.close()

    assert len(products) == 3
    assert products[0] == ("Mechanical Keyboard", 249.99, 15)
    assert products[1] == ("Gaming Mouse", 129.99, 30)
    assert products[2] == ("USB-C Hub", 89.99, 0)