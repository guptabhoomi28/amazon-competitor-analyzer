# from database import create_table, get_product

# create_table()

# product = get_product("B0FGYCJ7NJ")

# print(product)

# from database import get_connection


# connection = get_connection()

# rows = connection.execute(
#     """
#     SELECT asin, parent_asin, title, price, rating
#     FROM products
#     """
# ).fetchall()

# for row in rows:
#     print(row)

# connection.close()



from database import get_product, get_competitors


original_asin = "B0FGYCJ7NJ"

product = get_product(original_asin)

print("ORIGINAL PRODUCT")
print(product)

print("\nCOMPETITORS")

competitors = get_competitors(original_asin)

for competitor in competitors:
    print(competitor)