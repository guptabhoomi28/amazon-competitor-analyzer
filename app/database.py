import sqlite3

DATABASE_PATH = "products.db"

def get_connection():
    return sqlite3 .connect(DATABASE_PATH)

def create_table():
    connection = get_connection()

    connection.execute('''
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
        url TEXT
     )
''')

    connection.commit()
    connection.close()

def insert_product(product:dict , parent_asin:str = None):
    connection = get_connection()

    connection.execute("""
    INSERT OR REPLACE INTO products (
        asin ,
        parent_asin,
        title ,
        brand ,
        price ,
        currency ,
        rating ,
        reviews_count ,
        stock ,
        url
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? , ?)
""",
   (
    product.get('asin'),
    parent_asin,
    product.get('title'),
    product.get('brand'),
    product.get('price'),
    product.get('currency'),
    product.get('rating'),
    product.get('reviews_count'),
    product.get('stock'),
    product.get('url')
   ),
)

    connection.commit()
    connection.close()

create_table()

def get_product(asin:str):
    connection = get_connection()

    cursor = connection.execute(
    """
    SELECT 
        asin,
        title,
        brand,
        price,
        currency,
        rating,
        reviews_count,
        stock,
        url
    FROM products 
    WHERE asin = ?
    """, (asin,),
    )
    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "asin":row[0],
        "title":row[1],
        "brand":row[2],
        "price":row[3],
        "currency":row[4],
        "rating":row[5],
        "reviews_count":row[6],
        "stock":row[7],
        "url":row[8]
    }

def get_product(asin:str):
    connection =get_connection()

    row = connection.execute(
        """
        SELECT * 
        FROM products
        WHERE asin = ?
        """,
        (asin,)
    ).fetchone()

    connection.close()

    return row


def get_competitors(parent_asin:str):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM products
        WHERE parent_asin = ?
        """,
        (parent_asin,)
    ).fetchall()

    connection.close()

    return rows