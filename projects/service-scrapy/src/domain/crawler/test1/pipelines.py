# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
 
 
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from test1.items import ScrapyDangdang060Item
 
# 如果想使用管道的话，就要在setting中开启
class ScrapyDangdang060Pipeline:
    flag_first=True
    def open_spider(self, spider):
        print("++++++++++=========")
        self.fp = open('book.json', 'w', encoding='utf-8')
        self.fp.write("[")
 
    def process_item(self, item:ScrapyDangdang060Item, spider):
        if self.flag_first:
            self.fp.write(str(dict(item)))
            self.flag_first=False
        else:
            self.fp.write(",\n"+str(dict(item)))
        return item
    def close_spider(self, spider):
        print("------------------==========")
        self.fp.write("]")
        self.fp.close()