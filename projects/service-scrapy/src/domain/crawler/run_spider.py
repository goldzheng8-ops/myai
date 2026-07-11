import asyncio
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from test1.spiders.quotes import QuotesSpider

def main():
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    process = CrawlerProcess(get_project_settings())
    process.crawl(QuotesSpider)
    process.start()

if __name__ == "__main__":
    main()
