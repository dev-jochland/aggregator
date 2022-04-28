import importlib
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from typing import List, Dict

from settings import LRU_MAX_SIZE


class News(ABC):
    """
    Super class for all the source of news
    """

    @abstractmethod
    def __init__(self, source: str):
        self.source = source

    @abstractmethod
    def get_news_data(self, query_param: str = None) -> List[Dict[str, str]]:
        """
        :param query_param:
        :return: json news response data
        """
        raise NotImplementedError  # redundant

    @abstractmethod
    def resolve_news_data(self, request_data: Dict[str, object]) -> List[Dict[str, str]]:  # Generic JSON structure
        """
        :param request_data:
        :return: Array of news object with defined key:value
        """
        raise NotImplementedError  # redundant


class NewsManager:
    """
    This class aggregates news from all new source and also creates provided news source instance from the provided
    path name and news source class in the new_sources_dict
    """
    def __init__(self, news_source: Dict[str, str]):
        self.sources = []

        for source, path in news_source.items():
            module = importlib.import_module(path)
            Klass = getattr(module, source)

            self.sources.append(Klass())  # Register and get News Source Instance here

    @lru_cache(maxsize=LRU_MAX_SIZE)
    def aggregate_news(self, news_search_query: str = None):
        """
        Concurrently aggregates news from provided news source while updating LRU cache by the search_news_query
        :param news_search_query:
        :return: aggregated_news
        """
        news = []
        resource_threads = []

        with ThreadPoolExecutor(max_workers=len(self.sources)) as executor:
            for source in self.sources:
                resource_threads.append(executor.submit(source.get_news_data, news_search_query))

        for task in as_completed(resource_threads):
            news.extend(task.result())
        return news
