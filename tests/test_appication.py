import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.anyio
async def test_get_news_without_query():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/news')
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.anyio
async def test_get_news_with_query():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/news?query=russia')
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.anyio
async def test_get_news_without_query_fields():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/news')
    news_list = response.json()[:5]  # get the first 5 news from the numerous news
    for news in news_list:
        assert ('headline' in news)
        assert ('link' in news)
        assert ('source' in news)


@pytest.mark.anyio
async def test_get_news_with_query_fields():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/news?query=russia')
    news_list = response.json()[:2]  # get the first 2 news from the numerous news
    for news in news_list:
        assert ('headline' in news)
        assert ('link' in news)
        assert ('source' in news)
