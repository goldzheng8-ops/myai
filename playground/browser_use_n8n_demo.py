import asyncio
import logging
import os
import socket
from aiohttp import web
from browser_use import Agent, ChatOllama, BrowserProfile

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.5:9b")
DEMO_PORT = int(os.environ.get("DEMO_PORT", "8000"))


def make_llm() -> ChatOllama:
    return ChatOllama(
        model=OLLAMA_MODEL,
        host=OLLAMA_HOST,
        ollama_options={"num_ctx": 8192},
    )


def make_browser_profile() -> BrowserProfile:
    return BrowserProfile(
        headless=False,           # 先打开浏览器窗口，方便观察
        enable_default_extensions=False,
        keep_alive=True,
        extra_chromium_args=[
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ],
    )


async def build_agent(task: str) -> Agent:
    llm = make_llm()
    browser_profile = make_browser_profile()
    return Agent(task=task, llm=llm, browser_profile=browser_profile)


async def handle_run_task(request: web.Request) -> web.Response:
    data = await request.json()
    task = data.get("task")
    if not task:
        return web.json_response({"success": False, "error": "Missing task in request body."}, status=400)

    logging.info("Run task request: %s", task)
    agent = await build_agent(task)
    try:
        result = await agent.run()
        return web.json_response({"success": True, "task": task, "result": str(result)})
    except Exception as exc:
        logging.exception("Agent execution failed")
        return web.json_response({"success": False, "error": str(exc)}, status=500)


async def run_local_example() -> None:
    task = "Open https://example.com and tell me the page title."
    agent = await build_agent(task)
    result = await agent.run()
    print("Result:\n", result)


async def app_factory() -> web.Application:
    app = web.Application()
    app.router.add_post("/run-task", handle_run_task)
    return app


def find_available_port(start_port: int, max_tries: int = 10) -> int:
    for port in [start_port, *range(start_port + 1, start_port + max_tries + 1)]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise OSError(f"No available port found in range {start_port}-{start_port + max_tries}")


def main() -> None:
    if os.environ.get("RUN_LOCAL", "false").lower() in {"1", "true", "yes"}:
        asyncio.run(run_local_example())
        return

    port = find_available_port(DEMO_PORT)
    app = asyncio.run(app_factory())
    print(f"Starting browser_use+n8n demo server at http://127.0.0.1:{port}")
    web.run_app(app, host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
