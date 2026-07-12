import scrapy
from scrapy.http import HtmlResponse
from pathlib import Path

class MySpider(scrapy.Spider):
    name = "local_spider"

    def start_requests(self):
        html = Path("page1.html").read_text(encoding="utf-8")
        response = HtmlResponse(url="http://dummy.local", body=html, encoding="utf-8")
        yield from self.parse(response)  # ✅ 关键：必须 yield

    def parse(self, response):
        shu_list=response.css("li article.product_pod")
        for node in shu_list:
            # name=node.css("h3 a::text").get()
            # image_urls=[node.css(query="div.img152 img::attr(data-original)").get()]
            # item =DushuItem(name=name,image_urls=image_urls)

            yield {
                "name":node.css("h3 a::text").get(),
                "price":node.css("p.price_color::text").get()
            }

