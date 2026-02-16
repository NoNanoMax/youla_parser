
import re


async def click_all(page):
    for txt in ["Принять", "Согласен", "Разрешить все"]:
        btn = page.get_by_role("button", name=txt)
        if await btn.count():
            try:
                await btn.first.click(timeout=1500)
                await page.wait_for_timeout(500)
            except:
                pass


async def largest_visible_img_src(page) -> str | None:
    res = await page.evaluate("""
    () => {
      const imgs = Array.from(document.querySelectorAll("img"));
      const links = []; 
      let best = null, bestArea = 0;

      for (const img of imgs) {
        const r = img.getBoundingClientRect();
        const visible = r.width > 50 && r.height > 50;
        if (!visible) continue;

        const area = r.width * r.height;
        if (area > 2000) { 
          const src = img.currentSrc || img.src;
          if (src) links.push(src); }
      }
      return links;
    }
    """)
    return res


async def click_largest_image(page):
    # Кликаем по самой большой видимой картинке
    await page.evaluate("""
    () => {
      const imgs = Array.from(document.querySelectorAll("img"));
      let best = null, bestArea = 0;

      for (const img of imgs) {
        const r = img.getBoundingClientRect();
        const visible = r.width > 50 && r.height > 50 &&
                        r.bottom > 0 && r.right > 0 &&
                        r.top < window.innerHeight && r.left < window.innerWidth;
        if (!visible) continue;

        const area = r.width * r.height;
        if (area > 2500) { img.click(); return;}
      }
    }
    """)


async def get_meta(page, name):

    await page.wait_for_selector('dl[data-test-component="DescriptionList"]')
    dl = (page.locator('dl[data-test-component="DescriptionList"]')
        .filter(has=page.locator('dt', has_text='Описание'))
        .first)
    dl.wait_for()

    specs = await dl.evaluate("""
    (root) => {
    const out = {};
    for (const dt of root.querySelectorAll('dt')) {
        const key = dt.textContent?.trim();
        const dd = dt.nextElementSibling;
        if (!key || !dd || dd.tagName.toLowerCase() !== 'dd') continue;

        const val = (dd.textContent || '').trim();
        if (!val || val === '…') continue;

        out[key] = val;
    }
    return out;
    }
    """)

    return specs


def normalize_youla_image_url(url: str) -> str | None:
    re_pat = re.compile(r'^(https?://cdn\d+\.youla\.io/files/images/)\d+_\d+_out(/.+)$', re.I)
    m = re_pat.match(url)
    if not m:
        return None
    return f"{m.group(1)}720_720_out{m.group(2)}"
