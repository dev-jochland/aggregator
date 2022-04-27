from abc import ABC
from enum import Enum
from typing import Dict, List

import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError

from exceptions import ApiKeyMissing, InvalidApiKey
from settings import NEWSAPI_API_KEY, REQUEST_TIMEOUT
from util import News


class ResponseField(Enum):
    """
    Dynamically gets required fields from news response
    """
    HEADLINE = 'title'
    LINK = 'url'


class NewsApi(News, ABC):  # ABC to indicate the superclass is an abstract class
    BASE_NEWS_URL = 'https://newsapi.org/v2/everything?'

    def __init__(self, api_key=NEWSAPI_API_KEY):
        """
        api-key is required to access new_api endpoints, so I am initializing it with the class here anytime this class
        is instantiated
        :param api_key:
        """
        super().__init__('newsapi')

        if api_key is None:
            raise ApiKeyMissing(self.__class__.__name__)

        self.api_key = api_key

    def get_news_data(self, query_param: str = None) -> List[Dict[str, str]]:
        param = 'general' if query_param is None else query_param
        news_url = f'{self.BASE_NEWS_URL}q={param}&apiKey={self.api_key}'
        try:
            response = requests.get(news_url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except (Timeout, HTTPError, ConnectionError) as err:
            raise err

        if response.status_code != 200 and response.status_code == 401:
            raise InvalidApiKey(self.__class__.__name__)

        return self.resolve_news_data(response.json())

    def resolve_news_data(self, request_data: Dict[str, object]) -> List[Dict[str, str]]:
        news_data = request_data.get('articles', {})  # In case of None, declare and empty dict
        return [
            {
                'headline': news.get(ResponseField.HEADLINE.value),
                'link': news.get(ResponseField.LINK.value),
                'source': self.source
            }
            for news in news_data
        ]
