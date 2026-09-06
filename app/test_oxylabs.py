from oxylabs import scrape_product , search_amazon

# product = scrape_product("B0FGYCJ7NJ")

# print("ASIN:" , product['asin'])
# print("Title:" , product['title'])
# print("Brand:" , product['brand'])
# print("Price:" , product['price'])
# print("Rating:" , product['rating'])
# print("Review Count:" , product['reviews_count'])

products = search_amazon("Lenovo Idea Tab")

print("Numbers of product:" , len(products))

for product in products[:5]:
    print(product)
    print("-------------------------------------")









