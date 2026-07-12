from scrapy.spiders import XMLFeedSpider
from scrapy.selector import Selector

class TestxmlSpider(XMLFeedSpider):
    name = "testxml"
    allowed_domains = ["dushu.com"]
    start_urls = ["file:///E:/my_project/test1/products.xml"]
    iterator = "iternodes"  # you can change this; see the docs
    itertag = "product"  # change it accordinglyE:\my_project\test1\products.xml

    def parse_node(self, response, selector:Selector):
        yield {
        'id': selector.xpath('id/text()').get(),
        'name': selector.xpath('name/text()').get(),
        'price': selector.xpath('price/text()').get(),
        'url': selector.xpath('url/text()').get(),
    }

