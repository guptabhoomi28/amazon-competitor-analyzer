# import os
# import json
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# api_key = os.getenv('OPENROUTER_API_KEY')

# # openrouter/free automatically routes to a working, active free model
# model_name = "openrouter/free"

# print("🚀 Sending turn 1...")
# response = requests.post(
#     url="https://openrouter.ai/api/v1/chat/completions",
#     headers={
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json",
#     },
#     data=json.dumps({
#         "model": model_name,
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "How many r's are in the word 'strawberry'?"
#             }
#         ],
#         # Removed the reasoning toggle to ensure maximum compatibility with the free pool
#     })
# )

# print("\n--- Network Response Received ---")
# print(f"Status Code: {response.status_code}")

# # Prevent JSONDecodeError by checking text content first
# if not response.text.strip():
#     print("❌ Error: OpenRouter returned a completely empty body.")
# elif response.text.strip().startswith("<!DOCTYPE html>") or "<html>" in response.text:
#     print("❌ Error: Received an HTML page instead of JSON! Raw output snippet:")
#     print(response.text[:500])
# else:
#     try:
#         res_data = response.json()
#         if response.status_code == 200:
#             assistant_msg = res_data['choices'][0]['message']
#             print("\n✨ Turn 1 Success!")
#             print("Answer:", assistant_msg.get('content'))
            
#             # --- NEXT TURN LOGIC ---
#             messages = [
#                 {"role": "user", "content": "Explain Amazon competitor analysis in 2 simple sentences."},
#                 assistant_msg,
#                 {"role": "user", "content": "Are you sure? Think carefully."}
#             ]
            
#             print("\n🧠 Sending turn 2...")
#             response2 = requests.post(
#                 url="https://openrouter.ai/api/v1/chat/completions",
#                 headers={
#                     "Authorization": f"Bearer {api_key}",
#                     "Content-Type": "application/json",
#                 },
#                 data=json.dumps({
#                     "model": model_name,
#                     "messages": messages
#                 })
#             )
            
#             res2_data = response2.json()
#             print("\n✨ Turn 2 Final Answer:")
#             print(res2_data['choices'][0]['message']['content'])
            
#         else:
#             print(f"❌ API Business Error: {res_data}")
#     except Exception as e:
#         print(f"❌ Failed parsing payload structure: {e}")
#         print("Raw Server Text Response was:", response.text)


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



def test_analysis():
    product = {
        "title": "Lenovo Idea Tab",
        "brand": "Lenovo",
        "price": 195.1,
        "currency": "USD",
        "rating": 4.2,
        "reviews_count": 543,
    }

    competitors = [
        {
            "title": "Lenovo Idea Tab 8GB 256GB",
            "brand": "Lenovo",
            "price": 248.4,
            "currency": "USD",
            "rating": 4.6,
            "reviews_count": 800,
        },
        {
            "title": "Lenovo Idea Tab Plus",
            "brand": "Lenovo",
            "price": 269,
            "currency": "USD",
            "rating": 4.6,
            "reviews_count": 306,
        },
    ]

    prompt = build_analysis_prompt(product, competitors)

    analysis = call_llm(prompt)

    print(analysis)
