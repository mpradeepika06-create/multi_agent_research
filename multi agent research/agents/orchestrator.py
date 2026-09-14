import requests


class OrchestratorAgent:

    def __init__(self, model="llama3.1"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"

    def ask_llm(self, prompt):
        """
        Send prompt to Ollama.
        """

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

            data = response.json()

            return data.get("response", "")

        except Exception as e:
            return f"ERROR: {str(e)}"

    def create_research_plan(self, topic):

        prompt = f"""
You are the Orchestrator Agent of an autonomous research system.

Research topic:
{topic}

Create a detailed research plan for the topic.

The plan must contain exactly these sections:

1. Background
2. Current developments
3. Important facts and statistics
4. Benefits or positive aspects
5. Risks, limitations or negative aspects
6. Real-world applications
7. Different perspectives
8. Future outlook

For each section, provide 1-2 specific search queries.

Return only the research plan.
"""

        return self.ask_llm(prompt)

    def create_tasks(self, topic):

        plan = self.create_research_plan(topic)

        return {
            "topic": topic,
            "plan": plan
        }