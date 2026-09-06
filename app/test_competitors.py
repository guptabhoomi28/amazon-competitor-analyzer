# from services import find_competitors , scrape_competitors


# competitors = find_competitors(
#     "Lenovo Idea Tab",
#     "B0FGYCJ7NJ"
# )

# detailed_competitors = scrape_competitors(competitors)

# # print("No. of competitors:",len(competitors))
# print("No.of detailed competitors",len(detailed_competitors))

# # for competitor in competitors:
# #     print("ASIN:",competitor.get('asin')),
#     # print("Title:", competitor.get('title'))
#     # print("Price:", competitor.get('price'))
#     # print("Rating:", competitor.get('rating'))
#     # print("------------------------------------")


# for product in detailed_competitors:
#     print("ASIN:",product['asin'])
#     print("Title:",product['title'])
#     print("Price:",product['price'])
#     print("Rating:",product['rating'])
#     print("-------------------------------")



from services import find_competitors, scrape_competitors


original_asin = "B0FGYCJ7NJ"

competitors = find_competitors(
    "Lenovo Idea Tab",
    original_asin
)

detailed_competitors = scrape_competitors(
    competitors,
    original_asin
)

print("Saved competitors:", len(detailed_competitors))

for product in detailed_competitors:
    print(
        product["asin"],
        "->",
        product["title"]
    )
