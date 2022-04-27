class InvalidApiKey(Exception):
    def __init__(self, news_source):
        self.news_source = news_source


class ApiKeyMissing(Exception):
    def __init__(self, news_source):
        self.news_source = news_source
