from app.oxylabs import scrape_product , search_amazon
from app.database import get_product, insert_product , get_competitors
from app.llm import build_analysis_prompt, call_llm
from datetime import datetime, timedelta

def search_product(asin:str) -> dict:

    product = get_product(asin)

    if not product or not is_product_fresh(product):
        product = scrape_product(asin)
        insert_product(product)

    return product


def find_competitors(query: str, original_asin: str) -> list:
    products = search_amazon(query)

    candidates = []
    seen_asins = set()

    for product in products:
        asin = product.get("asin")

        if not asin:
            continue

        if asin == original_asin:
            continue

        if asin in seen_asins:
            continue

        seen_asins.add(asin)

        candidates.append(product)

    candidates.sort(
        key=lambda product: (
            product.get("is_sponsored", False),
            -(product.get("rating") or 0),
            -(product.get("reviews_count") or 0),
        )
    )

    return candidates[:5]


def scrape_competitors(competitors:list , parent_asin:str) -> list:
    detailed_competitors=[]

    for competitor in competitors:
        asin = competitor['asin']

        product = scrape_product(asin)
        
        insert_product(product , parent_asin)

        detailed_competitors.append(product)

    return detailed_competitors



def analyze_product(asin:str):

    asin = asin.strip()

    product = get_product(asin)

    if not product:
        product = scrape_product(asin)
        insert_product(product)

    competitors = get_competitors(asin)

    if not competitors_are_fresh(competitors):
        search_results = find_competitors(
            product["title"],
            asin
        )

        competitors = scrape_competitors(
            search_results,
            asin
        )

    prompt = build_analysis_prompt(
        product,
        competitors
    )

    analysis = call_llm(prompt)

    return {
    "product": product,
    "competitors": competitors,
    "analysis": analysis
    }

from datetime import datetime, timedelta, timezone


def is_product_fresh(product: dict) -> bool:
    if not product.get("last_scraped_at"):
        return False

    scraped_at = datetime.fromisoformat(
        product["last_scraped_at"]
    )

    return datetime.now(timezone.utc) - scraped_at < timedelta(hours=24)


def get_fresh_competitors(parent_asin: str) -> list:
    competitors = get_competitors(parent_asin)

    if not competitors:
        return []

    fresh_competitors = []

    for competitor in competitors:
        if is_product_fresh(competitor):
            fresh_competitors.append(competitor)

    return fresh_competitors


def competitors_are_fresh(competitors: list) -> bool:
    if not competitors:
        return False

    return all(
        is_product_fresh(competitor)
        for competitor in competitors
    )