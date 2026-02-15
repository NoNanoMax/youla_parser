from playwright.async_api import TimeoutError as PWTimeout
from fastapi import HTTPException
from core.cache import avto_cache
from scrapping.playwright_manager import PWResources
from scrapping.scrap_avto import parse_web
from core.config import settings

class AvtoService:
    async def get_by_url(self, res: PWResources, url: str) -> dict:
        if url in avto_cache:
            return avto_cache[url]

        async with res.sem:
            try:
                data = await parse_web(res.browser, url=url)
            except PWTimeout:
                raise HTTPException(status_code=504, detail="Scraping timeout")
            except Exception:
                raise HTTPException(status_code=502, detail="Scraping failed")

        avto_cache[url] = data
        return data
