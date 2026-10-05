import re, sys, glob, os, json
from bs4 import BeautifulSoup
def main_el(s):
    for t in ('wp-page','wp-post','single-post','single','page'):
        el = s.find(attrs={'data-elementor-type': t})
        if el: return el
    return s.find('main') or s.body
def dump(fn):
    s = BeautifulSoup(open(fn, encoding='utf-8').read(), 'html.parser')
    el = main_el(s)
    out = []
    for n in el.find_all(['h1','h2','h3','h4','h5','h6','p','li','img','a','span','div'], recursive=True):
        if n.name == 'img':
            src = n.get('data-src') or n.get('src') or ''
            if 'data:image' in src: src = n.get('data-lazy-src', src)
            out.append(f"[IMG {src} alt={n.get('alt','')}]")
        elif n.name in ('h1','h2','h3','h4','h5','h6'):
            out.append(f"#{n.name} " + n.get_text(' ', strip=True))
        elif n.name in ('p','li'):
            if n.find_parent(['p','li']) : continue
            t = n.get_text(' ', strip=True)
            if t: out.append(('- ' if n.name=='li' else '') + t)
        elif n.name=='div' and 'elementor-counter' in ' '.join(n.get('class',[])) :
            out.append('[COUNTER] ' + n.get_text(' ', strip=True))
        elif n.name=='div' and any(c in ('elementor-text-editor','pxl-text-editor') for c in n.get('class',[])) and not n.find('p'):
            out.append(n.get_text(' ', strip=True))
    # dedupe consecutive
    res=[]
    for o in out:
        if not res or res[-1]!=o: res.append(o)
    return res
for fn in sys.argv[1:]:
    print('=========', fn)
    print('\n'.join(dump(fn)))
