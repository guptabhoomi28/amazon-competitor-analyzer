from oxylabs import scrape_product , search_amazon
from database import get_product, insert_product

def search_product(asin:str) -> dict:

    product = get_product(asin)

    if product:
        return product
    
    product = scrape_product(asin)
    insert_product(product)

    return product


def find_competitors(query:str , orginal_asin:str) ->list:
    products = search_amazon(query)

    competitors =[]
    seen_asins=set()

    for product in products:
        asin = product.get("asin")

        if not asin:
            continue

        if asin == orginal_asin:
            continue

        if asin in seen_asins:
            continue

        seen_asins.add(asin)
        competitors.append(product)

    return competitors


def scrape_competitors(competitors:list , parent_asin:str) -> list:
    detailed_competitors=[]

    for competitor in competitors[:5]:
        asin = competitor['asin']

        product = scrape_product(asin)
        
        insert_product(product , parent_asin)

        detailed_competitors.append(product)

    return detailed_competitors