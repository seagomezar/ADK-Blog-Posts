from typing import Dict, List
import yfinance as yf
from google.adk.agents import Agent
from google.adk.tools import google_search


def get_financial_context(tickers: List[str]) -> Dict[str, str]:
    """Obtiene precio y variación diaria de cada ticker."""
    financial_data: Dict[str, str] = {}
    for ticker_symbol in tickers:
        try:
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            change_percent = info.get("regularMarketChangePercent")
            if price is not None and change_percent is not None:
                change_str = f"{(change_percent or 0) * 100:+.2f}%"
                financial_data[ticker_symbol] = f"${price:.2f} ({change_str})"
            else:
                financial_data[ticker_symbol] = "Price data not available."
        except Exception:
            financial_data[ticker_symbol] = "Invalid Ticker or Data Error"
    return financial_data


root_agent = Agent(
    name="ai_news_agent_l2",
    model="gemini-2.0-flash-live-001",
    description="Agente que combina búsqueda web y contexto financiero",
    instruction=(
        "Pide cuántas noticias desea la persona. Usa google_search para titulares y luego "
        "get_financial_context para enriquecer cada noticia con precio/variación. Respuestas concisas y cita fuentes."
    ),
    tools=[google_search, get_financial_context],
)

