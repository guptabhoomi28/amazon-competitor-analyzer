import os
import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from app.exceptions import LLMError



load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openrouter/free"


class ProductAnalysis(BaseModel):
    summary: str
    market_position: str
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]


def call_llm(prompt: str) -> ProductAnalysis:
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise LLMError("OPENROUTER_API_KEY is not set.")

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
        raise LLMError(
            f"OpenRouter request failed: {error}"
        ) from error

    try:
        data = response.json()

        content = data["choices"][0]["message"]["content"]

        if not isinstance(content, str):
            raise ValueError("LLM content is not a string.")

        content = content.strip()

        # Handle models that return JSON inside Markdown code fences.
        if content.startswith("```json"):
            content = content[7:]

        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        return ProductAnalysis.model_validate_json(content)

    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise LLMError(
            "OpenRouter returned an invalid structured response."
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
        Configuration: {product["configuration"]}
        Screen Size: {product["screen_size"]}
        Display Resolution: {product["display_resolution"]}
        Refresh Rate: {product["refresh_rate"]} Hz
        Processor: {product["processor"]}
        Battery Life: {product["battery_life"]}
        Operating System: {product["operating_system"]}
        Included Components: {product["included_components"]}

COMPETITORS:

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
        Configuration: {competitor["configuration"]}
        Screen Size: {competitor["screen_size"]}
        Display Resolution: {competitor["display_resolution"]}
        Refresh Rate: {competitor["refresh_rate"]} Hz
        Processor: {competitor["processor"]}
        Battery Life: {competitor["battery_life"]}
        Operating System: {competitor["operating_system"]}
        Included Components: {competitor["included_components"]}
"""

    prompt += """
        Analyze the main product using only the information provided.

        Do not invent, assume, or infer product specifications that are not explicitly provided.

        Compare the main product with its competitors based on:
        - Price
        - Rating
        - Review volume
        - Display
        - Processor
        - Battery life
        - Operating system
        - Included components
        - Overall configuration

        Return your response as JSON with exactly these fields:

        {
            "summary": "A concise summary of the product's position.",
            "market_position": "Explain how the product compares with competitors.",
            "strengths": [
                "Strength 1",
                "Strength 2"
            ],
            "weaknesses": [
                "Weakness 1",
                "Weakness 2"
            ],
            "recommendations": [
                "Recommendation 1",
                "Recommendation 2"
            ]
        }

        Do not include any text outside the JSON object.
        """
    return prompt