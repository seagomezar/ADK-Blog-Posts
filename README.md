## 🎓 Conclusión: Cierre del curso y próximos pasos

Has completado el recorrido desde un agente básico hasta un sistema multi‑agente listo para producción, con voz en tiempo real, herramientas, callbacks/guardrails, salidas estructuradas, evaluación, despliegue y observabilidad. Aquí resumimos los aprendizajes, te dejamos recursos verificados en la doc local (adk-docs) y una guía de siguientes pasos.

## Panorama general
- Diseñar agentes con propósito claro, instrucciones sólidas y herramientas adecuadas.
- Orquestar flujos: conversacional, coordinador/dispatcher y pipelines en segundo plano.
- Añadir control programático con callbacks y Plugins para guardrails de producción.
- Estandarizar salidas con esquemas (y entender cuándo separar formateo y tooling).
- Evaluar calidad (trayectoria + respuesta) y desplegar con trazabilidad.

## Lo que aprendiste por lección
- Lección 1 — Fundamentos y Web UI
  - Crear un agente, agregar `google_search` y probarlo en `adk web`.
  - Buenas prácticas de instrucciones y configuración declarativa con Agent Config YAML.
  - Blog: Lesson_1_blog.md
- Lección 2 — Herramientas personalizadas
  - Definir Function Tools bien tipadas (docstrings, errores controlados) y combinarlas con `google_search`.
  - Entender Session/State/Memory a nivel conceptual.
  - Blog: Lesson_2_blog.md
- Lección 3 — Coordinador en segundo plano
  - Patrón Coordinator–Dispatcher: ejecutar en silencio, responder solo dos veces y persistir Markdown.
  - Blog: Lesson_3_blog.md
- Lección 4 — Callbacks y guardrails
  - `before_tool_callback` y `after_tool_callback` en `LlmAgent`, process log y políticas; nota sobre Plugins.
  - Blog: Lesson_4_blog.md
- Lección 5 — Salidas estructuradas
  - `output_schema` para JSON estricto (sin tools) y patrón de 2 agentes (tools → formateo). Uso de `output_key`.
  - Blog: Lesson_5_blog.md
- Lección 6 — A producción
  - Streaming en vivo (`run_live` + `LiveRequestQueue`), Vertex AI Memory Bank, `adk eval`, despliegue (Agent Engine/Cloud Run/GKE), seguridad y observabilidad.
  - Blog: Lesson_6_blog.md

## Recursos esenciales (adk-docs locales)
- Quickstart y Python: adk-docs/docs/get-started/quickstart.md, adk-docs/docs/get-started/python.md
- Streaming (voz/video): adk-docs/docs/get-started/streaming/quickstart-streaming.md
- Built‑in tools y Google Search: adk-docs/docs/tools/built-in-tools.md, adk-docs/docs/grounding/google_search_grounding.md
- Function Tools: adk-docs/docs/tools/function-tools.md
- Callbacks y Plugins: adk-docs/docs/callbacks/types-of-callbacks.md, adk-docs/docs/plugins/index.md
- Contextos (ToolContext/CallbackContext): adk-docs/docs/context/index.md
- Memoria: adk-docs/docs/sessions/memory.md
- Evaluación: adk-docs/docs/evaluate/index.md
- Despliegue: adk-docs/docs/deploy/agent-engine.md, adk-docs/docs/deploy/cloud-run.md, adk-docs/docs/deploy/gke.md
- Observabilidad: adk-docs/docs/observability/logging.md, adk-docs/docs/observability/cloud-trace.md
- Seguridad: adk-docs/docs/safety/index.md

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

