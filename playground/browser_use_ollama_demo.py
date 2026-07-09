import asyncio
import logging

# logging.basicConfig(level=logging.DEBUG)

from browser_use import Agent, ChatOllama, BrowserProfile


async def main():
    llm = ChatOllama(
        model="qwen2.5vl:7b",
        host="http://127.0.0.1:11434",
        ollama_options={
            "num_ctx": 8192
        }
    )

    profile = BrowserProfile(
        enable_default_extensions=False
    )

    agent = Agent(
        task="Open https://example.com and tell me the page title.",
        llm=llm,
        browser_profile=profile,
    )

    result = await agent.run()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())