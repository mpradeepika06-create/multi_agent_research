import requests
import json


class InformationExtractionAgent:

    def __init__(self, model="llama3.1"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"

    def ask_llm(self, prompt):

        try:

            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=180
            )

            response.raise_for_status()

            return response.json().get(
                "response",
                ""
            )

        except Exception as e:
            return f"ERROR: {str(e)}"

    def extract(self, topic, sources, progress_callback=None):

        if progress_callback:
            progress_callback(
                "📑 Extraction Agent: extracting important information..."
            )

        extracted_information = []

        for source in sources:

            content = source.get("content", "")

            if not content:
                content = source.get(
                    "snippet",
                    ""
                )

            # Limit text sent to model
            content = content[:7000]

            prompt = f"""
You are an Information Extraction Agent.

Research topic:
{topic}

Source:
{source['title']}

URL:
{source['url']}

Source content:
{content}

Extract important information from this source.

Return the result as JSON with this structure:

{{
    "main_points": [
        "point 1",
        "point 2"
    ],
    "facts": [
        {{
            "claim": "fact or claim",
            "evidence": "supporting evidence"
        }}
    ],
    "statistics": [
        "important statistics if available"
    ],
    "limitations": [
        "limitations mentioned by the source"
    ]
}}

Do not invent information.
Only extract information that appears in the source.
"""

            result = self.ask_llm(prompt)

            parsed = self.parse_json(result)

            extracted_information.append({
                "source_id": source["id"],
                "title": source["title"],
                "url": source["url"],
                "data": parsed
            })

        if progress_callback:
            progress_callback(
                "✅ Extraction Agent: information extracted"
            )

        return extracted_information

    def parse_json(self, text):

        try:

            start = text.find("{")
            end = text.rfind("}")

            if start != -1 and end != -1:

                json_text = text[start:end + 1]

                return json.loads(
                    json_text
                )

        except Exception:
            pass

        return {
            "main_points": [text],
            "facts": [],
            "statistics": [],
            "limitations": []
        }