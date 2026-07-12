# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import Spider, signals
import random
from scrapy.http import Request
from fake_useragent import UserAgent
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy_playwright.page import PageMethod


class Test1SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class Test1DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider:Spider):
        spider.logger.info("Spider opened: %s" % spider.name)


# middlewares.py


class RandomUAMiddleware:
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request:Request, spider):
        request.headers['User-Agent'] = self.ua.random
        spider.logger.info(f"🛠 当前 UA: {request.headers["User-Agent"]}")  # ✅ 打印到日志

class PlaywrightAutoMiddleware:
    """
    自动为符合条件的请求加上 Playwright 渲染。
    """
    def process_request(self, request, spider):
        # 你可以根据域名、路径、headers等规则来决定哪些请求使用 Playwright
        use_playwright = (
            "books.toscrape.com" in request.url and
            request.meta.get("playwright", None) is None  # 避免重复设置
        )
        if use_playwright:
            request.meta["playwright"] = True
            request.meta["playwright_include_page"] = True
            request.meta["playwright_page_methods"] = [
                # 等待某个元素，避免空白页
                PageMethod("wait_for_selector", "article.product_pod")
            ]
        return None

