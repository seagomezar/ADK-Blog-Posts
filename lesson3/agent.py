import pathlib
from typing import Dict, List
import yfinance as yf
from google.adk.agents import Agent
from google.adk.tools import google_search


def get_financial_context(tickers: List[str]) -> Dict[str, str]:
    """Devuelve precio y variación porcentual por ticker."""
    out: Dict[str, str] = {}
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            change = info.get("regularMarketChangePercent")
            if price is not None and change is not None:
                out[t] = f"${price:.2f} ({(change or 0)*100:+.2f}%)"
            else:
                out[t] = "Price data not available."
        except Exception:
            out[t] = "Invalid Ticker or Data Error"
    return out


def save_news_to_markdown(filename: str, content: str) -> Dict[str, str]:
    """Guarda el reporte de investigación en un archivo Markdown."""
    if not filename.endswith(".md"):
        filename += ".md"
    path = pathlib.Path(filename)
    path.write_text(content, encoding="utf-8")
    return {"status": "success", "message": f"Saved to {path.resolve()}"}


root_agent = Agent(
    name="ai_news_coordinator_l3",
    model="gemini-2.0-flash-live-001",
    description="Coordinador que investiga en silencio y genera reporte Markdown",
    instruction=(
        "Responde solo dos veces: 1) Confirmación de inicio. 2) Confirmación final tras guardar reporte. "
        "Entre medio, usa google_search (5 noticias), extrae tickers, llama get_financial_context y formatea en Markdown. "
        "Guarda con save_news_to_markdown('ai_research_report.md', contenido). No muestres resultados intermedios."
    ),
    tools=[google_search, get_financial_context, save_news_to_markdown],
)

