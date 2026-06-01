import json
from google import genai
class LLMExtractor:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
    def extract_structured_data(self, text):
        prompt = f"""
Extract university information.
Return ONLY valid JSON.
{{
    "city": null,
    "state": null,
    "country": null,
    "tuition": null,
    "deadline": null
}}
Text:
{text[:10000]}
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        cleaned = (response.text.replace("```json", "").replace("```", "").strip())
        return json.loads(cleaned)