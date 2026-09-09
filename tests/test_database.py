import os
import sqlite3

from app import database


TEST_DB = "test_products.db"


def setup_function():
    database.DATABASE_PATH = TEST_DB

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    database.create_table()


def teardown_function():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_create_tables():
    connection = sqlite3.connect(TEST_DB)

    cursor = connection.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='products'"
    )

    result = cursor.fetchone()

    connection.close()

    assert result is not None


def test_insert_and_get_product():
    product = {
        "asin": "TEST123",
        "parent_asin": None,
        "title": "Test Tablet",
        "brand": "Test Brand",
        "price": 199.99,
        "currency": "USD",
        "rating": 4.5,
        "reviews_count": 100,
        "stock": "In Stock",
        "url": "https://example.com",
        "configuration": "10 inch display",
        "screen_size": "10 inches",
        "display_resolution": "1920 x 1200",
        "refresh_rate": "60",
        "processor": "Test Processor",
        "battery_life": "10 hours",
        "operating_system": "Android",
        "included_components": "Tablet, Cable",
        "last_scraped_at": "2026-09-09T10:00:00+00:00",
    }

    database.insert_product(product)

    result = database.get_product("TEST123")

    assert result is not None
    assert result["asin"] == "TEST123"
    assert result["title"] == "Test Tablet"
    assert result["price"] == 199.99
    assert result["rating"] == 4.5
    assert result["reviews_count"] == 100