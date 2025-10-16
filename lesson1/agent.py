from google.adk.agents import Agent
from google.adk.tools import google_search

# root_agent: agente básico con Google Search
root_agent = Agent(
    name="ai_news_agent_l1",
    model="gemini-2.0-flash-live-001",
    description="Asistente de noticias de IA con búsqueda en la web",
    instruction=(
        "Eres un asistente de noticias de IA. Usa Google Search para hallar información reciente, "
        "mantén respuestas claras y cita fuentes cuando corresponda."
    ),
    tools=[google_search],
)

