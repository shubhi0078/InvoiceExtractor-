import json
import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

print("Current folder:", os.getcwd())

api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print("✅ API Loaded")
    print("Starts with:", api_key[:5])
    print("Length:", len(api_key))
else:
    print("❌ API Key Not Found")

# Create Groq client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


def extract_with_llm(invoice_text):

    prompt = f"""
You are an expert invoice extraction assistant.

Extract the following information from the invoice.

Return ONLY valid JSON.

{{
    "Invoice Number":"",
    "Invoice Date":"",
    "Vendor Name":"",
    "BL Number":"",
    "PO Number":"",
    "Amount":"",
    "Currency":""
}}

Rules:

- Return ONLY valid JSON.
- Do not explain anything.
- Do not include markdown.
- If a field is missing, return an empty string.
- Preserve invoice numbers exactly.
- Preserve BL numbers exactly.
- Preserve PO numbers exactly.
- Preserve Vendor Name exactly.
- Return the final invoice total as Amount.
- Currency should be a 3-letter code whenever possible.

Invoice:

{invoice_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    # Remove Markdown code fences if present
    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    print(result)

    return json.loads(result)

    print("LLM Response:")
    print(result)

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {
            "Invoice Number": "",
            "Invoice Date": "",
            "Vendor Name": "",
            "BL Number": "",
            "PO Number": "",
            "Amount": "",
            "Currency": ""
        }