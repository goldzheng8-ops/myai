import asyncio

from browser_use import Agent
from browser_use import ChatOllama
from browser_use import BrowserProfile


async def main():

    llm = ChatOllama(
        model="qwen2.5:7b",
        host="http://127.0.0.1:11434",
        ollama_options={
            "temperature": 0,
            "num_ctx": 8192,
        },
    )

    profile = BrowserProfile(
        headless=False,
        keep_alive=True,
        enable_default_extensions=False,
        max_steps=5,

        proxy={
            "server": "socks5://127.0.0.1:1080",
        },
    )

    agent = Agent(
        task="""
1. Open https://news.ycombinator.com
2. Do not click anything.
3. Use extract action.
4. Extract ONLY the title text of the first item in the news list.
5. Return only one title string.
""",
        llm=llm,
        browser_profile=profile,
        use_vision=False,
        max_steps=5,
    )

    result = await agent.run()

    print(result)


if __name__ == "__main__":
    asyncio.run(main())