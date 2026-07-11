# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
 
import scrapy
 
 
class ScrapyDangdang060Item(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()  # Scrapy 用于下载图片的字段（必须命名为 image_urls）
    images = scrapy.Field()      # 下载结果（ImagesPipeline会自动填充）

class DushuItem(scrapy.Item):
    name=scrapy.Field()
    image_urls=scrapy.Field()
    images=scrapy.Field()
