from playwright.async_api import TimeoutError as PWTimeout
from fastapi import HTTPException
from core.cache import links_cache
from scrapping.playwright_manager import PWResources
from scrapping.scrap_links import parse_youla
from core.config import settings

class LinksService:
    async def list_links(self, res: PWResources, query: str | None) -> list[dict]:
        key = query or ""
        if key in links_cache:
            return links_cache[key]

        async with res.sem:
            try:
                data = await parse_youla(res.browser, query)
            except PWTimeout:
                raise HTTPException(status_code=504, detail="Scraping timeout")
            except Exception:
                raise HTTPException(status_code=502, detail="Scraping failed")

        links_cache[key] = data
        return data
