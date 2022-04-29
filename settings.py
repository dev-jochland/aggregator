import os

# For news api
NEWSAPI_API_KEY = os.getenv('NEWSAPI_API_KEY', 'f86b6890a1354ca3b491ae68b3a850d5')

# For reddit, mimic a browser agent to make this call and bypass reddit's 429 client error
REQUEST_HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 '
                  'Safari/537.36'
}

# To avoid the application waiting for the request forever since request are blocking in nature until there's a response
# from the destination server
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))  # secs for both read and connection.

LRU_MAX_SIZE = int(os.getenv('LRU_MAX_SIZE', 10))  # Limiting cache to a maximum of entries, so that the decorator can
# evict the least recently used entry when size is reached. This stop the cache from growing indefinitely.
