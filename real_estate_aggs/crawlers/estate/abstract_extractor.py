import datetime


class Extractor(object):
    def _safe_strip(self, entity):
        return entity.strip() if entity else 'Not available'

    def _extract_id(self, response):
        raise NotImplementedError("Extract id")

    def _extract_title(self, response):
        raise NotImplementedError("Extract title")

    def _extract_description(self, response):
        raise NotImplementedError("Extract description")

    def _extract_price(self, response):
        raise NotImplementedError("Extract price")

    def _extract_pictures(self, response):
        raise NotImplementedError("Extract pictures")

    def _extract_meta(self, response):
        raise NotImplementedError("Extract meta")

    def extract(self, response, type):
        yield {
            'id': self._extract_id(response),
            'title': self._extract_title(response),
            'description': self._extract_description(response),
            'price': self._extract_price(response),
            'pictures': self._extract_pictures(response),
            'meta_info': self._extract_meta(response),
            'link': response.meta['link'],
            'type': type,
            'date': datetime.datetime.utcnow()
        }
