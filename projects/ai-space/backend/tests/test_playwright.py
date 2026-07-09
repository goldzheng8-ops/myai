import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False,proxy={"server": "socks5://127.0.0.1:1080"})

        page = await browser.new_page()

        await page.goto("https://news.ycombinator.com")

        print(await page.title())

        await browser.close()


asyncio.run(main())