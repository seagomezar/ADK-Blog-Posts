import asyncio
from google.genai import types
from google.adk.runners import InMemoryRunner
from google.adk.agents import LiveRequestQueue
from google.adk.agents.run_config import RunConfig
from lesson6.agent import root_agent


async def demo_live_text():
    runner = InMemoryRunner(app_name="Lesson6 Streaming Demo", agent=root_agent)
    session = await runner.session_service.create_session(app_name=runner.app_name, user_id="demo-user")
    run_config = RunConfig(response_modalities=["TEXT"], session_resumption=types.SessionResumptionConfig())
    live_request_queue = LiveRequestQueue()
    live_events = runner.run_live(session=session, live_request_queue=live_request_queue, run_config=run_config)

    # Enviar prompt inicial
    live_request_queue.send_content(content=types.Content(role="user", parts=[types.Part(text="Dame 2 titulares recientes de IA")]))

    async for event in live_events:
        if event.turn_complete or event.interrupted:
            break
        if event.content and event.content.parts and getattr(event.content.parts[0], "text", None):
            print(event.content.parts[0].text, end="")


if __name__ == "__main__":
    asyncio.run(demo_live_text())

