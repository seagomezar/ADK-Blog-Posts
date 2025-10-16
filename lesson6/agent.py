from google.adk.agents import Agent
from google.adk.tools import google_search

# root_agent básico para ADK Web; ver streaming en streaming/main.py
root_agent = Agent(
    name="ai_news_agent_l6",
    model="gemini-2.0-flash-live-001",
    description="Asistente base para pruebas; ver ejemplo de streaming separado",
    instruction="Responde preguntas de IA y usa google_search para información reciente.",
    tools=[google_search],
)

