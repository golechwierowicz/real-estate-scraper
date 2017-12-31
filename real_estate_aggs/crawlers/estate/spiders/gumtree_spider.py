import scrapy
import re

from real_estate_aggs.crawlers.estate.abstract_extractor import Extractor


class GumtreeSpider(scrapy.Spider):
    name = 'gumtree'
    start_urls = ['http://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/warszawa/v1c9008l3200008p{}'.format(i)
                  for i in range(1, 10)]  # parse first 10 pages

    def parse(self, response):
        for href in response.css('div.result-link a'):
            yield response.follow(href, callback=self.parse_post, meta={'link': response
                                  .urljoin(href.css('a::attr(href)').extract_first())})

    def parse_post(self, response):
        yield from GumtreeExtractor().extract(response, 'gumtree')


class GumtreeExtractor(Extractor):
    def _extract_within_content(self, response, query):
        result = response.css('div.vip-header-and-details ' + query).extract_first()
        return self._safe_strip(result)

    def _preprocess_img_url(self, url):
        result = url
        if 'img.classistatic.com/crop' in url:
            result = re.sub(r"img.classistatic.com/crop/\d+x\d+/", '', url)
        result = result.replace('$_19', '$_20')
        return result

    def _extract_pictures(self, response):
        return [self._preprocess_img_url(img.css('img::attr(src)').extract_first()) for img in
                response.css('div.vip-gallery div.thumbs img')]

    def _extract_description(self, response):
        return self._extract_within_content(response, 'div.description span.pre::text')

    def _extract_title(self, response):
        return response.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/section/div/div[5]/div[7]/ul/li[*]/div/div[2]/div[1]/a/text()').extract_first()

    def _extract_meta(self, response):
        return [[(self._safe_strip(a.css('span.name::text').extract_first()),
                  self._safe_strip(a.css('span.value::text').extract_first()))
                 for a in attr.css('div.attribute')]
                for attr in response.css('div.vip-header-and-details ul.selMenu')]

    def _extract_price(self, response):
        return self._extract_within_content(response, 'div.price span.value span.amount::text')

    def _extract_id(self, response):
        result = response.css('div.breadcrumbs span.title::text').extract_first()
        id = re.search(r"[0-9]+$", result)
        return id.group(0)
