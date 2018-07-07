import scrapy
import re

from real_estate_aggs.crawlers.estate.abstract_extractor import Extractor


class OlxSpider(scrapy.Spider):
    name = 'olx'
    start_urls = ['https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page={}'.format(i)
                  for i in range(1, 10)]  # parse first 10 pages

    def parse(self, response):
        for href in response \
                .xpath('//*[@id="offers_table"]/tbody/tr[*]/td/table/tbody/tr[1]/td[2]/div/h3/a/@href') \
                .extract():
            yield response.follow(href, callback=self.parse_post, meta={'link': href})

    def parse_post(self, response):
        is_otodom = 'otodom' in response.meta['link']
        if is_otodom:
            yield from OtodomExtractor().extract(response, 'otodom')
        else:
            yield from OlxExtractor().extract(response, 'olx')


class OlxExtractor(Extractor):
    def _extract_pictures(self, response):
        return [img.css('img::attr(src)').extract_first() for img in response.css('div.img-item img')]

    def _extract_price(self, response):
        return self._safe_strip(response.xpath('//*[@id="offeractions"]/div[1]/strong/text()').extract_first())

    def _extract_description(self, response):
        return self._safe_strip(response.xpath('//*[@id="textContent"]/p/text()').extract_first())

    def _extract_id(self, response):
        result = response.xpath('//*[@id="offerdescription"]/div[2]/div[1]/em/small/text()').extract_first()
        return re.search(r"[0-9]+$", result).group(0)

    def _extract_title(self, response):
        return self._safe_strip(response.xpath('//*[@id="offerdescription"]/div[2]/h1/text()').extract_first())

    def _extract_meta(self, response):
        keys = response.xpath(
            "//*[@id=\"offerdescription\"]/div[3]/table/tr[*]/td[*]/table/tr/th/text()").extract()
        values = [x.strip() for x in
                  response.xpath("/html/body[@class='detailpage t-new_sidebar']/div[@id='innerLayout']/section["
                                 "@id='body-container']/div[@class='wrapper']/div[@id='offer_active']/div[@class='clr "
                                 "offerbody']/div[@class='offercontent fleft rel ']/div[@class='offercontentinner "
                                 "offer__innerbox']/div[@id='offerdescription']/div[@class='clr descriptioncontent "
                                 "marginbott20']/table[@class='details fixed marginbott20 margintop5 full']/tr[*]/td["
                                 "@class='col'][*]/table[@class='item']/tr/td[@class='value']/strong/a/text("
                                 ")").extract()]
        return [(self._safe_strip(x), self._safe_strip(y).strip()) for x, y in zip(keys, values)]


class OtodomExtractor(Extractor):
    def _extract_pictures(self, response):
        return response.xpath('//*[@id="offer-gallery"]/div[2]/a[*]/@href').extract()

    def _extract_description(self, response):
        return response.xpath("/html/body/div[1]/section[6]/div/div/div/div/div/div[1]/p/text()").extract_first()

    def _extract_title(self, response):
        return response.xpath("/html/body/div[1]/section[1]/div/div/header/h1/text()").extract_first()

    def _extract_meta(self, response):
        keys = response.xpath('/html/body/div[1]/section[5]/div/div/div/ul/li[1]/ul[2]/li[*]/strong/text()').extract()
        values = response.xpath('/html/body/div[1]/section[5]/div/div/div/ul/li[1]/ul[2]/li[*]/text()').extract()
        return [(self._safe_strip(x[0]), self._safe_strip(x[1])) for x in zip(keys, values)]

    def _extract_price(self, response):
        result = response.xpath("/html/body/div[1]/section[5]/div/div/div/ul/li[1]/ul[1]/li[1]/span/strong/text()") \
            .extract_first()
        return self._safe_strip(result)

    def _extract_id(self, response):
        result = response.xpath("/html/body/div[1]/section[9]/div/div/div/div/div[1]/p[1]/text()").extract_first()
        return re.search(r"[0-9]+$", result).group(0)
