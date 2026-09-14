import requests


class ReportGenerationAgent:

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

    def generate(
        self,
        topic,
        analysis,
        fact_check_results,
        sources,
        progress_callback=None
    ):

        if progress_callback:
            progress_callback(
                "📝 Report Agent: generating final report..."
            )

        source_list = ""

        for source in sources:

            source_list += (
                f"\n[{source['id']}] "
                f"{source['title']} - "
                f"{source['url']}"
            )

        prompt = f"""
You are a professional Research Report Generation Agent.

Topic:
{topic}

Analysis:
{analysis}

Fact checking:
{fact_check_results}

Sources:
{source_list}

Create a professional research report.

Use this exact structure:

# Research Report

## 1. Executive Summary

## 2. Introduction

## 3. Background

## 4. Key Findings

## 5. Benefits and Opportunities

## 6. Risks and Limitations

## 7. Detailed Analysis

## 8. Fact-Checking Summary

## 9. Future Outlook

## 10. Conclusion

## 11. References

Rules:

- Use clear professional language.
- Do not invent information.
- Do not invent references.
- Only use the supplied sources.
- Keep source IDs such as [1], [2], etc. when referring to evidence.
- The References section must contain the supplied URLs.
- Clearly distinguish verified information from uncertain information.
"""

        result = self.ask_llm(prompt)

        # Add a reliable references section ourselves
        references = "\n\n## 11. References\n\n"

        for source in sources:

            references += (
                f"{source['id']}. "
                f"{source['title']}  \n"
                f"{source['url']}\n\n"
            )

        # Remove existing references heading if model generated one
        result = result.replace(
            "## 11. References",
            ""
        )

        final_report = result.strip() + references

        if progress_callback:
            progress_callback(
                "✅ Report Agent: final report generated"
            )

        return final_report