from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from dotenv import load_dotenv

from exceptions import InvalidApiKey, ApiKeyMissing
from util import NewsManager
load_dotenv()


news_source = {
    'NewsApi': 'sources.news_api',
    'Reddit': 'sources.reddit'
}

news_manager = NewsManager(news_source)

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
