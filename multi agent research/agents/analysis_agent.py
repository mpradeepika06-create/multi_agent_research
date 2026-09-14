import requests


class AnalysisAgent:

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

    def analyze(
        self,
        topic,
        extracted_information,
        fact_check_results,
        progress_callback=None
    ):

        if progress_callback:
            progress_callback(
                "🧠 Analysis Agent: analyzing research..."
            )

        information_text = ""

        for item in extracted_information:

            information_text += f"""

SOURCE {item['source_id']}
Title: {item['title']}
URL: {item['url']}

Extracted information:
{item['data']}
"""

        prompt = f"""
You are an Analysis Agent.

Research topic:
{topic}

Collected information:
{information_text}

Fact-checking results:
{fact_check_results}

Analyze the research.

Discuss:

1. Major findings
2. Important trends
3. Benefits
4. Risks and limitations
5. Areas where sources agree
6. Areas where sources disagree
7. Important evidence
8. Overall conclusion

Do not invent facts.

When discussing a fact, mention its Source ID when possible.
"""

        result = self.ask_llm(prompt)

        if progress_callback:
            progress_callback(
                "✅ Analysis Agent: analysis completed"
            )

        return result