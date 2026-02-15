from playwright.async_api import TimeoutError as PWTimeout
from scrapping.utils import click_largest_image, largest_visible_img_src, normalize_youla_image_url


async def parse_web(browser, url):

    all_urls = []

    context = await browser.new_context(locale="ru-RU")
    page = await context.new_page()

    try:

        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(600)

        await click_largest_image(page)
        await page.wait_for_timeout(600)

        for _ in range(10):
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(600)
            urls = await largest_visible_img_src(page)
            all_urls.extend(urls)

        all_urls = list(set(all_urls))
        all_urls = [normalize_youla_image_url(url) for url in all_urls]
        all_urls = [url for url in all_urls if url]

        return {
            "url": url,
            "title": None,
            "published_at": None, 
            "photo_urls": all_urls
        }
    
    except PWTimeout:
        raise 

    finally:
        await context.close()


if __name__ == "__main__":
    import asyncio
    res = asyncio.run(parse_web(input()))
    print(res)
