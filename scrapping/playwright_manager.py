import asyncio
from dataclasses import dataclass

from playwright.async_api import async_playwright, Browser, Playwright

@dataclass
class PWResources:
    pw: Playwright
    browser: Browser
    sem: asyncio.Semaphore


async def start_playwright(headless: bool, max_concurrency: int) -> PWResources:
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=headless)
    sem = asyncio.Semaphore(max_concurrency)
    return PWResources(pw=pw, browser=browser, sem=sem)


async def stop_playwright(res: PWResources) -> None:
    await res.browser.close()
    await res.pw.stop()
