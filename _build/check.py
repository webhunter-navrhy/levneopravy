"""Headless kontrola: snímky + rozbité obrázky + přetečení. python3 _build/check.py <base> <out> [stránky…]"""
import sys, asyncio, os, json
from playwright.async_api import async_playwright
BASE, OUT = sys.argv[1], sys.argv[2]; PAGES = sys.argv[3:] or ['']
os.makedirs(OUT, exist_ok=True)
async def run():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        for w, h, tag in ((1440, 900, 'd'), (390, 844, 'm')):
            ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
            pg = await ctx.new_page()
            errs = []
            pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
            pg.on('pageerror', lambda e: errs.append(str(e)))
            for path in PAGES:
                errs.clear()
                r = await pg.goto(BASE + path, wait_until='networkidle')
                H = await pg.evaluate('document.body.scrollHeight')
                for y in range(0, H, 500):
                    await pg.evaluate(f'window.scrollTo({{top:{y},behavior:"instant"}})'); await pg.wait_for_timeout(60)
                await pg.evaluate('window.scrollTo({top:0,behavior:"instant"})'); await pg.wait_for_timeout(1200)
                info = await pg.evaluate('''() => ({broken:[...document.images].filter(i=>i.complete && i.naturalWidth===0).map(i=>i.src),
                  over:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+1 && getComputedStyle(e).position!=='fixed' && !e.closest('.marquee,.mega,.akce,.cta,.cz')}).slice(0,5).map(e=>e.className||e.tagName),
                  sw:document.documentElement.scrollWidth, iw:innerWidth})''')
                name = (path.strip('/').replace('/', '_') or 'home') + '_' + tag
                await pg.screenshot(path=f'{OUT}/{name}.png', full_page=True)
                print(tag, path or '/', r.status, 'broken', info['broken'], 'over', info['over'], 'sw', info['sw'], info['iw'], 'errs', errs[:3])
            await ctx.close()
        await b.close()
asyncio.run(run())
