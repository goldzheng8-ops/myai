from playwright.async_api import async_playwright



async def fetch_news():


    async with async_playwright() as p:


        browser = await p.chromium.launch(
            headless=True,proxy={"server": "socks5://127.0.0.1:1080"}
        )


        page = await browser.new_page()


        await page.goto(
            "https://news.ycombinator.com"
        )


        title = await page.locator(
            ".titleline a"
        ).first.text_content()


        await browser.close()


        return title