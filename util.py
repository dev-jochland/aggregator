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
    def __init__(self, news_source: Dict[str, str]):
        """Registers class instance from news_source_dict into this manager class"""
        self.sources = []

        for source, path in news_source.items():

            module = importlib.import_module(path)  # Relative import into path's __init__.py, to allow me define & be
            # in control of the news source class I want registered in this manager. That way, results can be consistent

            Klass = getattr(module, source)  # Get the default class provided in the path's __init__.py, since an
            # attribute error would have been thrown, for the fact that I want to control the class being injected into
            # the manager

            self.sources.append(Klass())  # Register News Source Class Instance here for the manager class

    @lru_cache(maxsize=LRU_MAX_SIZE)
    def aggregate_news(self, news_search_query: str = None):
        """
        Concurrently aggregates news from provided news source while updating LRU cache by the search_news_query
        :param news_search_query:
        :return: aggregated_news
        """
        news = []
        resource_threads = []

        # ThreadPoolExecutor utility: Because it's best for I/O-bound operation (web request/crawler) in a Python Thread
        # Dynamic max_workers to dynamically create the required number of concurrent threads that can process jobs
        # based on news_source_dict injected at server start
        with ThreadPoolExecutor(max_workers=len(self.sources)) as executor:  # with: auto cleans up thread on completion
            for source in self.sources:

                # Saves Future instance created on each submit call into resource_threads list
                resource_threads.append(executor.submit(source.get_news_data, news_search_query))

        for task in as_completed(resource_threads):  # as_completed waits for each Future get_news_data call to complete

            # Aggregates list of all news from the result()-Future instance into a single news list
            news.extend(task.result())
        return news
