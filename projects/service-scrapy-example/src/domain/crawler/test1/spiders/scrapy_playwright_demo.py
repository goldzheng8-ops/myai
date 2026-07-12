import scrapy
from scrapy.http import HtmlResponse
from pathlib import Path
from scrapy_playwright.page import PageMethod
from scrapy.http import Response

class MySpider(scrapy.Spider):
    name = "scrapypw"

    def start_requests(self):
        yield scrapy.Request(
        url="https://books.toscrape.com",
        meta={
            "playwright": True,
            "playwright_include_page": True,
            "playwright_page_methods": [PageMethod("wait_for_selector", "article.product_pod")],
        },
        callback=self.parse
    )

    def parse(self, response:Response):
        shu_list=response.css("li article.product_pod")
        for node in shu_list:
            # name=node.css("h3 a::text").get()
            # image_urls=[node.css(query="div.img152 img::attr(data-original)").get()]
            # item =DushuItem(name=name,image_urls=image_urls)

            yield {
                "name":node.css("h3 a::text").get(),
                "price":node.css("p.price_color::text").get()
            }
        self.logger.info(f"***页面：page****{response.meta.keys()}")
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [PageMethod("wait_for_selector", "article.product_pod")]
                }
            )
