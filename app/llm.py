import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openrouter/free"


def call_llm(prompt: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise RuntimeError(
            f"OpenRouter request failed: {error}"
        ) from error

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]

    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError(
            "Unexpected response format from OpenRouter."
        ) from error


def build_analysis_prompt(product: dict, competitors: list) -> str:
    prompt = f"""
        You are an Amazon competitor analysis expert.

        Analyze the following Amazon product against its competitors.

        MAIN PRODUCT:
        Title: {product["title"]}
        Brand: {product["brand"]}
        Price: {product["price"]} {product["currency"]}
        Rating: {product["rating"]}
        Reviews: {product["reviews_count"]}

        COMPETITORS:
        """

    for index, competitor in enumerate(competitors, start=1):
        prompt += f"""
        Competitor {index}:
        Title: {competitor["title"]}
        Brand: {competitor["brand"]}
        Price: {competitor["price"]} {competitor["currency"]}
        Rating: {competitor["rating"]}
        Reviews: {competitor["reviews_count"]}
        """

        prompt += """
        Based only on the information provided:

        1. Summarize the main product's market position.
        2. Identify its strengths compared with competitors.
        3. Identify its weaknesses.
        4. Give practical recommendations for improving its competitive position.

        Keep the analysis clear and concise.
        """

    return prompt


