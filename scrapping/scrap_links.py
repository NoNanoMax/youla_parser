import re
from playwright.async_api import TimeoutError as PWTimeout
import asyncio

from scrapping.utils import click_all


AD_RE = re.compile(
    r"^https?://(www\.)?youla\.ru/moskva/auto/.+-[0-9a-f]{24}(\?.*)?$",
    re.IGNORECASE
)


def _canon(url: str) -> str:
    return url.split("?", 1)[0]


async def collect_ad_urls_from_search(page, search_url: str, max_ads: int = 300) -> list[str]:
    await page.goto(search_url, wait_until="domcontentloaded")
    await page.wait_for_timeout(1000)

    await click_all(page)

    seen = set()

    for step in range(20):
        hrefs = await page.eval_on_selector_all("a[href]", "els => els.map(e => e.href).filter(Boolean)")
        for h in hrefs:
            if AD_RE.match(h):
                seen.add(_canon(h))

        print(f"step {step+1}: ads={len(seen)}")
        if len(seen) >= max_ads:
            break

        before = len(seen)

        await page.evaluate(
            """(reStr) => {
                const re = new RegExp(reStr, "i");
                const links = Array.from(document.querySelectorAll('a[href]'))
                  .map(a => a.href)
                  .filter(h => re.test(h));
                if (!links.length) return;

                // найдём последний <a> и проскроллим к нему
                const lastHref = links[links.length - 1];
                const lastA = Array.from(document.querySelectorAll('a[href]'))
                  .find(a => a.href === lastHref);
                if (lastA) lastA.scrollIntoView({block: "end", inline: "nearest"});
            }""",
            AD_RE.pattern
        )

        await page.mouse.wheel(0, 1)

        try:
            await page.wait_for_function(
                """(reStr, prevCount) => {
                    const re = new RegExp(reStr, "i");
                    const count = Array.from(document.querySelectorAll('a[href]'))
                      .map(a => a.href)
                      .filter(h => re.test(h)).length;
                    return count > prevCount;
                }""",
                arg=(AD_RE.pattern, before),
                timeout=8000
            )
        except:
            await page.mouse.wheel(0, 1)
            await page.wait_for_timeout(150)

    return list(seen)[:max_ads]


async def parse_youla(browser, search_url: str):

    context = await browser.new_context(locale="ru-RU")
    page = await context.new_page()

    try:
        ad_urls = await collect_ad_urls_from_search(page, search_url)
        return [{"url": u, "source": "dev"} for u in ad_urls if u]
    except PWTimeout:
        raise
    finally:
        await context.close()


if __name__ == "__main__":
    res = asyncio.run(parse_youla(input()))
    print(res)
