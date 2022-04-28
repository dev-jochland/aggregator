import os

# for news api
NEWSAPI_API_KEY = os.getenv('NEWSAPI_API_KEY', 'f86b6890a1354ca3b491ae68b3a850d5')

# for reddit, since there is no direct API for news, mimic a browser agent to make this call
REQUEST_HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 '
                  'Safari/537.36'
}

# To avoid the application waiting for the request forever since request are blocking in nature until there's a response
# from the destination server
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))  # secs

LRU_MAX_SIZE = int(os.getenv('LRU_MAX_SIZE', 10))
