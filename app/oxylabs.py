import os 

import requests
from dotenv import load_dotenv

load_dotenv()

OXYLABS_URL = 'https://realtime.oxylabs.io/v1/queries'

def normalize_product(content :dict) ->dict:
    return {
        "asin" :content["asin"],
        "title" :content["title"],
        "brand" :content["brand"], 
        "price" :content["price"],
        "currency" :content["currency"],
        "rating" :content["rating"],
        "reviews_count":content["reviews_count"],
        "stock":content["stock"],
        "url":content["url"],
        "images":content["images"]
    }

def scrape_product(asin :str) -> dict:

    asin = asin.strip()

    if not asin:
        raise ValueError("ASIN cannot be empty or whitespace.")
    
    username = os.getenv("OXYLABS_USERNAME")
    password = os.getenv("OXYLABS_PASSWORD")

    payload ={
        "source" : "amazon_product",
        "query" : asin,
        "domain" :"com",
        "parse" :True
    }

    try:
        response = requests.post(
            OXYLABS_URL,
            auth=(username , password),
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        
    except requests.RequestException as error:
        raise RuntimeError(
            f"Oxylabs request failed :{error}"
    )from error

    data = response.json()

    if not data.get('results'):
        raise RuntimeError(
            f"No product data returned for ASIN: {asin}"
        )

    content = data['results'][0].get('content')

    if not content:
        raise RuntimeError(
            f"No product content found for ASIN: {asin}"
        )

    return normalize_product(content)


def normalize_search_product(product:dict)-> dict:
    return{
        "asin":product.get("asin"),
        "title":product.get("title"),
        "price": product.get("price"),
        "currency": product.get("currency"),
        "rating": product.get("rating"),
        "reviews_count": product.get("reviews_count"),
        "url": product.get("url"),
        "image": product.get("url_image"),
        "is_sponsored": product.get("is_sponsored", False)
    }


def search_amazon( query:str) -> list:

    username = os.getenv("OXYLABS_USERNAME")
    password = os.getenv("OXYLABS_PASSWORD")

    payload ={
        "source" :"amazon_search",
        "query" :query,
        "domain" :"com",
        "parse" :True
    }
    try:
        response = requests.post(
            OXYLABS_URL,
            auth = (username , password),
            json = payload,
            timeout =60
        )
        
        response.raise_for_status()

    except requests.RequestException as error:
        raise RuntimeError(
            f"No competitors found for product: {query}"
        )from error

    data = response.json()

    if not data.get('results'):
        raise RuntimeError(
                    f"No competitor data returned for query: {query}"
        )

    content = data["results"][0]["content"]

    if not content:
        raise RuntimeError(
                    f"No competitor content found for query: {query}"
        )

    organic_products = content['results']['organic']

    if not organic_products:
        return RuntimeError(
            f"No  organic product found for content:{content}"
        )

    return [
        normalize_search_product(product)
        for product in organic_products
    ]