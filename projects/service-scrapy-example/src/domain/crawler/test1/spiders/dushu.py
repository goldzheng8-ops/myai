import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Response
from ..items import DushuItem

class DushuSpider(CrawlSpider):
    name = "dushu"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    rules = (Rule(LinkExtractor(allow=r"catalogue/page-\d+.html"), callback="parse_item", follow=True),)

    def parse_item(self, response:Response):
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        shu_list=response.css("li article.product_pod")
        for node in shu_list:
            # name=node.css("h3 a::text").get()
            # image_urls=[node.css(query="div.img152 img::attr(data-original)").get()]
            # item =DushuItem(name=name,image_urls=image_urls)

            return {
                "name":node.css("h3 a::text").get(),
                "price":node.css("p.price_color::text").get()
            }
