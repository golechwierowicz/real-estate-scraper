import scrapy


class GumtreeSpider(scrapy.Spider):
    name = 'gumtree'
    start_urls = ['http://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/warszawa/v1c9008l3200008p{}'.format(i)
                  for i in range(1, 10)]

    def parse(self, response):
        for href in response.css('div.result-link a'):
            yield response.follow(href, callback=self.parse_whole)

    def _safe_strip(self, entity):
        return entity.strip() if entity else 'Not available'

    def _extract_with_css(self, response, query):
        result = response.css('div.vip-header-and-details ' + query).extract_first()
        return self._safe_strip(result)

    def _extract_metadata(self, response):
        return [[(self._safe_strip(a.css('span.name::text').extract_first()),
                  self._safe_strip(a.css('span.value::text').extract_first()))
                 for a in attr.css('div.attribute')]
                for attr in response.css('div.vip-header-and-details ul.selMenu')]

    def parse_whole(self, response):
        yield {
            'title': self._extract_with_css(response, 'span.myAdTitle::text'),
            'description': self._extract_with_css(response, 'div.description span.pre::text'),
            'price': self._extract_with_css(response, 'div.price span.value span.amount::text'),
            'meta_info': self._extract_metadata(response),
        }
