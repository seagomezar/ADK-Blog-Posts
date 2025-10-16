import re
from urllib.parse import urlparse
from typing import Dict
from google.adk.agents import LlmAgent
from google.adk.tools import google_search, ToolContext


BLOCKED_DOMAINS = [
    "wikipedia.org",
    "reddit.com",
    "youtube.com",
    "medium.com",
    "investopedia.com",
    "quora.com",
]


def filter_news_sources_callback(tool, args, tool_context: ToolContext):
    if tool.name == "google_search":
        query = (args or {}).get("query", "").lower()
        for domain in BLOCKED_DOMAINS:
            if f"site:{domain}" in query or domain.split(".")[0] in query:
                return {
                    "error": "blocked_source",
                    "reason": f"Searches targeting {domain} are not allowed. Use professional news sources.",
                }
    return None


def inject_process_log_after_search(tool, args, tool_context: ToolContext, tool_response):
    if tool.name != "google_search":
        return tool_response

    if isinstance(tool_response, dict):
        raw = tool_response.get("search_results") or tool_response.get("results") or ""
    else:
        raw = tool_response

    if isinstance(raw, str) and raw:
        urls = re.findall(r"https?://[^\s/]+", raw)
        unique_domains = sorted({urlparse(u).netloc for u in urls})
        if unique_domains:
            sourcing_log = f"Action: Sourced news from: {', '.join(unique_domains)}."
            tool_context.state["process_log"] = [sourcing_log] + tool_context.state.get("process_log", [])

    return {
        "search_results": raw if isinstance(raw, str) else str(raw),
        "process_log": tool_context.state.get("process_log", []),
    }


root_agent = LlmAgent(
    name="ai_news_callbacks_l4",
    model="gemini-2.0-flash-live-001",
    description="Agente con guardrails vía callbacks (filtro de dominios + process log)",
    instruction=(
        "Genera un reporte con 5 noticias de IA y explica fuentes en process_log. "
        "No muestres contenido intermedio; confirma al inicio y al final."
    ),
    tools=[google_search],
    before_tool_callback=[filter_news_sources_callback],
    after_tool_callback=[inject_process_log_after_search],
)

