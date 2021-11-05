import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

class BooksScraperItem(scrapy.Item):
    bk_id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    ws_id = scrapy.Field()
