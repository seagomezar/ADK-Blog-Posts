from typing import List, Optional
from pydantic import BaseModel, AnyHttpUrl, conlist, Field
from google.adk.agents import LlmAgent


class NewsItem(BaseModel):
    headline: str = Field(..., min_length=8)
    company: str
    ticker: Optional[str]
    market_data: str
    summary: str
    sources: conlist(AnyHttpUrl, min_items=1)


class ResearchReport(BaseModel):
    title: str
    items: conlist(NewsItem, min_items=3, max_items=10)
    process_log: List[str] = []


# Agente de formateo: fuerza salida JSON (sin tools)
root_agent = LlmAgent(
    name="ai_news_structured_l5",
    model="gemini-2.0-flash",
    description="Agente que devuelve un JSON válido conforme al esquema del reporte",
    instruction=(
        "Devuelve EXCLUSIVAMENTE un JSON válido que siga el esquema. No incluyas texto extra."
    ),
    output_schema=ResearchReport,
    output_key="final_report_json",
)

