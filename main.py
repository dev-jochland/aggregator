from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from dotenv import load_dotenv

from exceptions import InvalidApiKey, ApiKeyMissing
from util import NewsManager
load_dotenv()

"""
Add other news source to this dictionary ({'class_name': 'sources.package_name}) below by properly defining a package
for it in the "sources" folder and implementing the abstract methods from class News(utils.py) in your
added news source module, also don't forget to import the class into your package __init__.py, this way, you are sure 
that the right class is being imported into the program.
"""
news_source = {
    'NewsApi': 'sources.news_api',
    'Reddit': 'sources.reddit'
}

news_manager = NewsManager(news_source)  # The above news source dict is injected via the news manager into the app at
# server start and not when an api call is made.

app = FastAPI()


@app.get('/news', response_class=ORJSONResponse)  # ORJSONResponse provides fast json response
async def news(query: str = None):
    try:
        return news_manager.aggregate_news(query)
    except InvalidApiKey as e:
        source = e.news_source
        raise HTTPException(status_code=401, detail=f'Provided API Key is Invalid for {source}')
    except ApiKeyMissing as e:
        source = e.news_source
        raise HTTPException(status_code=400, detail=f'Provide API Key for {source}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
