import scrapy
from scrapy.http import Response
from scrapy_playwright.page import PageMethod

class HybridSpider(scrapy.Spider):
    name = "hybrid"

    def start_requests(self):
        yield scrapy.Request(
            url="https://quotes.toscrape.com/js/",
            meta={
                "playwright": True,
                "playwright_include_page": True,
            },
            callback=self.parse_with_playwright
        )

    async def parse_with_playwright(self, response: Response):
        self.logger.info(f"✅ 当前页面: {response.url}")
        self.logger.debug(f"META keys: {response.meta.keys()}")

        page = response.meta["playwright_page"]

        # 👉 等待初始内容加载
        await page.wait_for_selector("div.quote")

        # 👉 模拟点击“下一页”按钮两次
        for i in range(2):
            try:
                next_btn = await page.query_selector("li.next a")
                if next_btn:
                    await next_btn.click()
                    await page.wait_for_selector("div.quote", timeout=3000)  # 等待新页面内容出现
                    self.logger.info(f"👉 第 {i+2} 页已加载")
                else:
                    break
            except Exception as e:
                self.logger.warning(f"❌ 翻页失败: {e}")
                break

        # 👉 抓取当前页面所有内容（包括点击后加载的）
        content = await page.content()
        await page.close()

        # 👉 用新的 response 重新构造 Scrapy 可解析的 HtmlResponse
        new_response = response.replace(body=content)

        # 👉 用普通 Scrapy CSS 解析处理
        for quote in new_response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get()
            }
