import scrapy


class GumtreeItem(scrapy.Item):
    name = scrapy.Field()
    pictures = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
