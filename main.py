from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import get_connection, initialize_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="ShopGuard QA",
    description="A demo e-commerce application built for QA automation practice.",
    version="0.2.0",
    lifespan=lifespan,
)


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


def row_to_product(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "price": row["price"],
        "stock": row["stock"],
    }


@app.get("/")
def home():
    return {
        "message": "Welcome to ShopGuard QA!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/products")
def get_products():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, name, price, stock FROM products ORDER BY id"
        ).fetchall()

    return [row_to_product(row) for row in rows]


@app.get("/products/{product_id}")
def get_product(product_id: int):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, name, price, stock
            FROM products
            WHERE id = ?
            """,
            (product_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return row_to_product(row)


@app.post("/products", status_code=201)
def create_product(product_data: ProductCreate):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO products (name, price, stock)
            VALUES (?, ?, ?)
            """,
            (
                product_data.name,
                product_data.price,
                product_data.stock,
            ),
        )

        product_id = cursor.lastrowid

        row = connection.execute(
            """
            SELECT id, name, price, stock
            FROM products
            WHERE id = ?
            """,
            (product_id,),
        ).fetchone()

    return row_to_product(row)