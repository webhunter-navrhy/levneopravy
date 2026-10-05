import sys, asyncio
from playwright.async_api import async_playwright
async def main(url,out,w=1440,h=900,full=False):
    async with async_playwright() as p:
        b=await p.chromium.launch(headless=True)
        pg=await b.new_page(viewport={'width':w,'height':h})
        await pg.goto(url); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=out,full_page=full)
        await b.close()
a=sys.argv; asyncio.run(main(a[1],a[2],int(a[3]) if len(a)>3 else 1440,int(a[4]) if len(a)>4 else 900, len(a)>5))
