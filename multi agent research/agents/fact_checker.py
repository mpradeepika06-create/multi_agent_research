import requests


class FactCheckingAgent:

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

    def check(self, topic, extracted_information, progress_callback=None):

        if progress_callback:
            progress_callback(
                "🔍 Fact Checker: verifying claims..."
            )

        claims = []

        for item in extracted_information:

            data = item["data"]

            for fact in data.get("facts", []):

                if isinstance(fact, dict):

                    claims.append({
                        "claim": fact.get("claim", ""),
                        "evidence": fact.get("evidence", ""),
                        "source_id": item["source_id"],
                        "source": item["title"]
                    })

        if not claims:

            return []

        # Keep prompt reasonably small
        claims_text = "\n\n".join(
            [
                f"""
Claim ID: {i + 1}
Claim: {claim['claim']}
Evidence: {claim['evidence']}
Source: {claim['source']}
Source ID: {claim['source_id']}
"""
                for i, claim in enumerate(claims[:30])
            ]
        )

        prompt = f"""
You are a professional Fact Checking Agent.

Research topic:
{topic}

Below are claims extracted from research sources.

{claims_text}

Evaluate each claim.

Use these labels:

VERIFIED
PARTIALLY VERIFIED
UNVERIFIED
CONTRADICTED

Be conservative.

A claim should not be considered VERIFIED merely because a source
mentions a similar topic.

Return a numbered fact-checking report.

For each claim provide:

Claim:
Status:
Reason:
Source ID:

Do not invent additional sources.
"""

        result = self.ask_llm(prompt)

        if progress_callback:
            progress_callback(
                "✅ Fact Checker: verification completed"
            )

        return result