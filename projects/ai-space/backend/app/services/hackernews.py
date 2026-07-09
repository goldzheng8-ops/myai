from playwright.async_api import async_playwright


async def get_latest_news():

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True,
            proxy={"server": "socks5://127.0.0.1:1080"}
        )

        page = await browser.new_page()

        await page.goto(
            "https://news.ycombinator.com"
        )

        first = page.locator(".titleline a").first

        title = await first.text_content()

        url = await first.get_attribute("href")

        await browser.close()

        return {
            "title": title,
            "url": url,
            "source": "hackernews",
        }