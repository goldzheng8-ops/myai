import scrapy
from scrapy.http import Response

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["www.baidu.com"]
    start_urls = ["http://www.baidu.com"]

    def parse(self, response:Response):
        print(response.css("title::text"))
