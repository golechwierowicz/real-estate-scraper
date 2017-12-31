class DatabaseSavePipeline(object):
    def __init__(self, postgres_uri):
        self.postgres_uri = postgres_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            postgres_uri=crawler.settings.get('POSTGRES_URI'),
        )

    def open_spider(self, _):
        self.session = None  # create session here

    def close_spider(self, _):
        self.session.close()

    def process_item(self, item, _):
        # insert to postgres here
        return item
