import scrapy


class GumtreeItem(scrapy.Item):
    name = scrapy.Field()
    pictures = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    meta_info = scrapy.Field()
