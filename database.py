import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "shopguard.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL CHECK (price > 0),
                stock INTEGER NOT NULL CHECK (stock >= 0)
            )
            """
        )

        product_count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        if product_count == 0:
            connection.executemany(
                """
                INSERT INTO products (name, price, stock)
                VALUES (?, ?, ?)
                """,
                [
                    ("Mechanical Keyboard", 249.99, 15),
                    ("Gaming Mouse", 129.99, 30),
                    ("USB-C Hub", 89.99, 0),
                ],
            )


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at: {DATABASE_PATH}")