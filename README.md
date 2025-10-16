# Curso: Building Live Voice Agents with Google’s ADK (en español)

Este repositorio acompaña una serie de blogs en español que cubren, paso a paso, cómo construir agentes con el Agent Development Kit (ADK) de Google: desde tu primer agente y herramientas personalizadas, hasta callbacks, salidas estructuradas y preparación para producción (streaming, memoria, evaluación, despliegue y observabilidad).

Cada lección incluye:
- Un blog (contenido pedagógico y enlaces a la doc pública de ADK).
- Un Notebook de apoyo (en GitHub).
- Un directorio `lessonN/` con el agente listo para ejecutar en ADK.
- Una rama git dedicada por lección.

## Mapa de lecciones y materiales
- Lección 1 — Fundamentos: primer agente, Web UI y Google Search
  - Blog: Lesson_1_blog.md
  - Notebook: https://github.com/seagomezar/ADK-Blog-Posts/blob/main/Lesson_1.ipynb
  - Código: `lesson1/`
- Lección 2 — Herramientas personalizadas y flujo conversacional
  - Blog: Lesson_2_blog.md
  - Notebook: https://github.com/seagomezar/ADK-Blog-Posts/blob/main/Lesson_2.ipynb
  - Código: `lesson2/`
- Lección 3 — Coordinador en segundo plano (reportes Markdown)
  - Blog: Lesson_3_blog.md
  - Notebook: https://github.com/seagomezar/ADK-Blog-Posts/blob/main/Lesson_3.ipynb
  - Código: `lesson3/`
- Lección 4 — Callbacks y guardrails
  - Blog: Lesson_4_blog.md
  - Notebook: https://github.com/seagomezar/ADK-Blog-Posts/blob/main/Lesson_4.ipynb
  - Código: `lesson4/`
- Lección 5 — Respuestas estructuradas y validación
  - Blog: Lesson_5_blog.md
  - Notebook: https://github.com/seagomezar/ADK-Blog-Posts/blob/main/Lesson_5.ipynb
  - Código: `lesson5/`
- Lección 6 — A producción (streaming, memoria, evaluación, despliegue, observabilidad)
  - Blog: Lesson_6_blog.md
  - Notebook: https://github.com/seagomezar/ADK-Blog-Posts/blob/main/Lesson_6.ipynb
  - Código: `lesson6/` (incluye ejemplo en `lesson6/streaming/main.py`)
- Conclusión y próximos pasos: Conclusion_blog.md

## Enlaces útiles (doc pública)
- Quickstart: https://google.github.io/adk-docs/get-started/quickstart/
- Python: https://google.github.io/adk-docs/get-started/python/
- Built‑in Tools: https://google.github.io/adk-docs/tools/built-in-tools/
- Function Tools: https://google.github.io/adk-docs/tools/function-tools/
- Callbacks: https://google.github.io/adk-docs/callbacks/types-of-callbacks/
- Plugins: https://google.github.io/adk-docs/plugins/
- Memoria: https://google.github.io/adk-docs/sessions/memory/
- Evaluación: https://google.github.io/adk-docs/evaluate/
- Despliegue: https://google.github.io/adk-docs/deploy/
- Observabilidad: https://google.github.io/adk-docs/observability/

## Instalación y comandos básicos (alineados a docs)
```bash
# Instala ADK
pip install google-adk

# Crea un agente basado en código
adk create my_agent --model gemini-2.0-flash-live-001 --api_key $GOOGLE_API_KEY

# Ejecuta la Web UI (desde carpeta padre o apuntando al agente)
adk web                # luego selecciona "my_agent" en el menú
# o
adk web --port 8000 my_agent
# Windows: si ves _make_subprocess_transport NotImplementedError, usa --no-reload

# Ejecuta en CLI
adk run my_agent

# Servidor de API (opcional)
adk api_server --log_level INFO path/to/agents_dir

# Opcional (memoria persistente en Web/API server)
adk web path/to/agents_dir --memory_service_uri="agentengine://<AGENT_ENGINE_ID>"
```

## Consejos de producción rápidos
- Google Search
  - Compatible con modelos Gemini 2. Si el modelo devuelve "Search suggestions", debes mostrarlas en tu UI (política de Grounding).
- Streaming
  - Usa modelos Live API y configura `SSL_CERT_FILE=$(python -m certifi)` cuando corresponda.
- Callbacks y Plugins
  - Prefiere Plugins para políticas globales; se ejecutan antes que callbacks y pueden retornar temprano.
- Estructurado
  - `output_schema` (sin tools) o separa herramientas y formateo con dos agentes; usa `output_key` para persistir resultados.
- Observabilidad
  - `--log_level` y `--trace_to_cloud` en despliegues gestionados; integra OpenTelemetry cuando personalices runtime.

## Troubleshooting (depurado alineado a docs)
- El agente no responde o responde genérico
  - Revisa `.env` y `GOOGLE_API_KEY` o credenciales Vertex; confirma el `model` (por ejemplo, `gemini-2.0-flash-live-001`).
  - Verifica instrucciones y herramientas registradas en `tools=[...]`.
- Tools fallan
  - Asegura type hints + docstrings claros; valida el tipo/forma del retorno. Prueba la función de forma aislada primero.
- Callbacks no disparan / resultados inesperados
  - Firma correcta: `before_tool(tool, args, tool_context)` y `after_tool(tool, args, tool_context, tool_response)` en `LlmAgent`.
  - Recuerda: si un callback retorna algo distinto de `None`, el framework usa ese valor (salta la ejecución del tool o reemplaza el resultado).
  - Considera Plugins si la política es global.
- Estado (state)
  - Modifica a través de `ToolContext`/`CallbackContext`; ADK persiste cambios vía Runner. Usa `output_key` para guardar salidas finales.
- Voz
  - Usa modelos Live, permisos de micrófono en el navegador y confirma el puerto correcto en `adk web`. Prueba texto y luego voz.
- Logging
  - Sube a `--log_level DEBUG` temporalmente. Inspecciona prompts, llamadas a tools y latencias.

## Reto final 🎯
- Convierte tu agente en un servicio con memoria persistente y trazas Cloud Trace, protegido con Plugins de seguridad (p. ej., redacción PII y Model Armor) y validado con `adk eval` en tu pipeline CI/CD.
- Extiende el patrón de dos agentes para generar: JSON validado → Markdown → audio (podcast), midiendo latencia y costo.

## Cierre
Este curso te deja una base sólida para construir agentes conversacionales, coordinadores e incluso pipelines en segundo plano, con controles de seguridad y observabilidad para producción. Conecta estos bloques con tus datos y procesos, itera con evaluaciones, y comparte lo que construyas. ¡Nos encantará ver tu próximo agente en acción!
