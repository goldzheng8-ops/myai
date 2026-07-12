import scrapy
# 这里报错是编译器的问题，但是并不影响下面的代码
from scrapy.http import Response
 
from domain.crawler.test1.items import ScrapyDangdang060Item


class DangSpider(scrapy.Spider):
    name = "dang"
    allowed_domains = ["category.dangdang.com","ddimg.cn"]
    start_urls = ["https://category.dangdang.com/cid4002429.html"]
 
    def parse(self, response:Response):
        print("===============成功================")
        request = response.request
        if request is not None:
            ua=request.headers.get('User-Agent')
        if ua is not None:
            ua=ua.decode()
        self.logger.info(f"🎯 请求 UA 为：{ua}")
        # pipelines 管道用于下载数据
        # items     定义数据结构的
        # src = //ul[@id="component_47"]/li//img/@src
        # alt = //ul[@id="component_47"]/li//img/@alt
        # price = //ul[@id="component_47"]/li//p/span/text()
        # 所有的seletor的对象都可以再次调用xpath
        li_list = response.css("ul.cloth_shoplist>li")
        for li in li_list:
            # 这里页面使用了懒加载，所以不能使用src了
          

            image_urls =[ "https:"+str(li.css('img::attr(data-original)').extract_first())]
 
            name = li.css('p.name >a::text').extract_first()
            # /span/text()
            price = li.css('p.price >span.price_n::text').extract_first()
            # print(src, name, price)
 
            book = ScrapyDangdang060Item(image_urls=image_urls, name=name, price=price)
 
            # 获取一个book就将book交给pipelines
            yield book
 
 
 