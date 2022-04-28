from enum import Enum
from typing import Dict, List

import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError

from settings import REQUEST_TIMEOUT, REQUEST_HEADERS
from util import News


class ResponseField(Enum):
    """
    Dynamically gets required fields from news response
    """
    NEWS_HEADLINE = 'title'
    NEWS_LINK = 'url_overridden_by_dest'


class Reddit(News):
    BASE_NEWS_URL = 'https://www.reddit.com/r/news'

    def __init__(self):
        super().__init__('reddit')

    def get_news_data(self, query_param: str = None) -> List[Dict[str, str]]:
        news_url = f'{self.BASE_NEWS_URL}/.json' if query_param is None else f'{self.BASE_NEWS_URL}/search.json?' \
                                                                             f'q={query_param}&restrict_sr=1 '
        try:
            response = requests.get(news_url, timeout=REQUEST_TIMEOUT, headers=REQUEST_HEADERS)  # Request headers to
            # avoid: "429 Client Error: Too Many Requests for url: https://www.reddit.com/r/news/.json"
            response.raise_for_status()
        except (Timeout, HTTPError, ConnectionError) as err:
            raise err

        if response.status_code != 200 and response.status_code == 401:
            raise Exception('Unauthorized or Service Error')

        return self.resolve_news_data(response.json())

    def resolve_news_data(self, request_data: Dict[str, object]) -> List[Dict[str, str]]:
        news_data = request_data.get('data', {}).get('children')  # In case of None, declare and empty dict
        return [
            {
                'headline': news.get('data').get(ResponseField.NEWS_HEADLINE.value),
                'link': news.get('data').get(ResponseField.NEWS_LINK.value),
                'source': self.source
            }
            for news in news_data
        ]
