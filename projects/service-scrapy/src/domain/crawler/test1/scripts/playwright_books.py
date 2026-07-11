import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("http://books.toscrape.com/catalogue/page-1.html")
        await page.wait_for_selector("article.product_pod")
        content = await page.content()
        with open("page1.html", "w", encoding="utf-8") as f:
            f.write(content)
        await browser.close()

asyncio.run(main())
