import os
import json
import re
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELS = [
    os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
    os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.5-flash-lite"),
]

RETRIES_PER_MODEL = 3


def parse_json(text: str) -> dict:
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text, strict=False)


def call_llm(prompt: str) -> dict:
    last_error = None

    for model in MODELS:
        for attempt in range(RETRIES_PER_MODEL):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.3,
                    ),
                )
                return parse_json(response.text)
            except Exception as e:
                last_error = e
                print(f"LLM retry: model={model}, attempt={attempt + 1}, error={e}")
                time.sleep(2 * (attempt + 1))

    raise last_error