import sqlite3
from datetime import datetime, timezone

DATABASE_PATH = "products.db"

def get_connection():
    return sqlite3 .connect(DATABASE_PATH)

def create_table():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            asin TEXT PRIMARY KEY,
            parent_asin TEXT,
            title TEXT NOT NULL,
            brand TEXT,
            price REAL,
            currency TEXT,
            rating REAL,
            reviews_count INTEGER,
            stock TEXT,
            url TEXT,
            configuration TEXT,
            screen_size TEXT,
            display_resolution TEXT,
            refresh_rate TEXT,
            processor TEXT,
            battery_life TEXT,
            operating_system TEXT,
            included_components TEXT,
            last_scraped_at TEXT
        )
        """
    )

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_table()

def insert_product(product: dict, parent_asin: str = None):
    connection = get_connection()
    scraped_at = datetime.now(timezone.utc).isoformat()

    connection.execute(
        """
        INSERT OR REPLACE INTO products (
            asin,
            parent_asin,
            title,
            brand,
            price,
            currency,
            rating,
            reviews_count,
            stock,
            url,
            configuration,
            screen_size,
            display_resolution,
            refresh_rate,
            processor,
            battery_life,
            operating_system,
            included_components,
            last_scraped_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            product.get("asin"),
            parent_asin,
            product.get("title"),
            product.get("brand"),
            product.get("price"),
            product.get("currency"),
            product.get("rating"),
            product.get("reviews_count"),
            product.get("stock"),
            product.get("url"),
            product.get("configuration"),
            product.get("screen_size"),
            product.get("display_resolution"),
            product.get("refresh_rate"),
            product.get("processor"),
            product.get("battery_life"),
            product.get("operating_system"),
            product.get("included_components"),
            scraped_at
        ),
    )

    connection.commit()
    connection.close()

create_table()

def get_product(asin: str):
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT
            asin,
            parent_asin,
            title,
            brand,
            price,
            currency,
            rating,
            reviews_count,
            stock,
            url,
            configuration,
            screen_size,
            display_resolution,
            refresh_rate,
            processor,
            battery_life,
            operating_system,
            included_components,
            last_scraped_at
        FROM products
        WHERE asin = ?
        """,
        (asin,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "asin": row[0],
        "parent_asin": row[1],
        "title": row[2],
        "brand": row[3],
        "price": row[4],
        "currency": row[5],
        "rating": row[6],
        "reviews_count": row[7],
        "stock": row[8],
        "url": row[9],
        "configuration": row[10],
        "screen_size": row[11],
        "display_resolution": row[12],
        "refresh_rate": row[13],
        "processor": row[14],
        "battery_life": row[15],
        "operating_system": row[16],
        "included_components": row[17],
        "last_scraped_at": row[18],
    }


def get_competitors(parent_asin: str):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            asin,
            parent_asin,
            title,
            brand,
            price,
            currency,
            rating,
            reviews_count,
            stock,
            url,
            configuration,
            screen_size,
            display_resolution,
            refresh_rate,
            processor,
            battery_life,
            operating_system,
            included_components,
            last_scraped_at
        FROM products
        WHERE parent_asin = ?
        """,
        (parent_asin,),
    ).fetchall()

    connection.close()

    competitors = []

    for row in rows:
        competitors.append({
            "asin": row[0],
            "parent_asin": row[1],
            "title": row[2],
            "brand": row[3],
            "price": row[4],
            "currency": row[5],
            "rating": row[6],
            "reviews_count": row[7],
            "stock": row[8],
            "url": row[9],
            "configuration": row[10],
            "screen_size": row[11],
            "display_resolution": row[12],
            "refresh_rate": row[13],
            "processor": row[14],
            "battery_life": row[15],
            "operating_system": row[16],
            "included_components": row[17],
            "last_scraped_at": row[18],
        })

    return competitors


