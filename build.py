#!/usr/bin/env python3
"""Sestaví návrh webu levneopravy.cz do site/ (obsah v _data/*.json, šablony v src/)."""
import json, os, shutil, hashlib, re
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'site')
D = lambda n: json.load(open(os.path.join(ROOT, '_data', n), encoding='utf-8'))
S, SV, M, LEGAL, MAP = D('site.json'), D('services.json'), D('media.json'), D('legal.json'), D('map.json')
BY = {s['slug']: s for s in SV}
MAIN = [s for s in SV if s['menu'] == 'main']
OTHER = [s for s in SV if s['menu'] == 'other']

if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'assets'))
for n in ('style.css', 'main.js'): shutil.copy(os.path.join(ROOT, 'src', n), os.path.join(OUT, 'assets', n))
shutil.copytree(os.path.join(ROOT, 'img'), os.path.join(OUT, 'img'))
shutil.copy(os.path.join(ROOT, 'src', 'favicon.png'), os.path.join(OUT, 'favicon.png'))
open(os.path.join(OUT, '.nojekyll'), 'w').close()
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /\n')
V = {k: hashlib.md5(open(os.path.join(OUT, 'assets', f), 'rb').read()).hexdigest()[:8] for k, f in (('css', 'style.css'), ('js', 'main.js'))}

# mapa: přepočet poboček do souřadnic SVG
X0, X1, Y0, Y1 = MAP['box']
def xy(lon, lat): return (round((lon - X0) / (X1 - X0) * MAP['w'], 1), round((Y1 - lat) / (Y1 - Y0) * MAP['h'], 1))
PINS = [{'n': n, 'a': a, 'x': xy(lo, la)[0], 'y': xy(lo, la)[1]} for n, a, lo, la in S['branches']]
HUBS = [{'n': n, 'x': xy(lo, la)[0], 'y': xy(lo, la)[1]} for n, lo, la in (('Praha', 14.43, 50.08), ('Brno', 16.61, 49.195), ('Olomouc', 17.25, 49.594))]
FINDER = json.dumps([{'t': s['title'], 'p': s['path'].strip('/'), 'd': s['short']} for s in SV], ensure_ascii=False)

env = Environment(loader=FileSystemLoader(os.path.join(ROOT, 'src')), autoescape=True, trim_blocks=True, lstrip_blocks=True)

def render(path, tpl, **kw):
    depth = len([x for x in path.split('/') if x])
    R = '../' * depth
    def L(h):
        if h.startswith('http') or h.startswith('mailto') or h.startswith('tel') or h.startswith('#'): return h
        return R + h.lstrip('/') if h.strip('/') else (R or './')
    ctx = dict(S=S, M=M, MAIN=MAIN, OTHER=OTHER, BY=BY, SV=SV, R=R, L=L, V=V, path=path, MAP=MAP, PINS=PINS, HUBS=HUBS, FINDER=FINDER)
    ctx.update(kw)
    html = env.get_template(tpl).render(**ctx)
    fp = os.path.join(OUT, path.strip('/'), 'index.html') if path.strip('/') else os.path.join(OUT, 'index.html')
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(html)

render('/', 'home.html', title='Levné opravy Praha – spolehliví řemeslníci po celé ČR', description='Levné opravy & montážní servis: instalatér, elektrikář, truhlář, zedník, obkladač, montáž dveří a kuchyní, bytová jádra a údržba domů. Působíme po celé České republice.', active='/')
render('/o-nas/', 'about.html', title='O nás – Levné opravy Praha', description=S['intro'], active='/o-nas/')
render('/nase-sluzby/', 'list.html', title='Naše služby – Levné opravy Praha', description='Přehled našich hlavních služeb: bytová jádra, instalatérské, elektrikářské, obkladačské, podlahářské a truhlářské práce, montáž kuchyní a další.', active='/nase-sluzby/',
       h1='Přehled našich hlavních služeb', items=MAIN, kicker='Naše služby', other=('Další služby', '/dalsi-sluzby/', OTHER))
render('/dalsi-sluzby/', 'list.html', title='Další služby – Levné opravy Praha', description='Vyklízecí práce, stěhování a doprava, kovářské práce, pravidelná údržba domů, střechy a klempířské, výškové a zahradnické práce.', active='/dalsi-sluzby/',
       h1='Co Vám můžeme nabídnout?', items=OTHER, kicker='Další služby', other=('Naše hlavní služby', '/nase-sluzby/', MAIN))
for s in SV:
    rel = [x for x in SV if x['group'] == s['group'] and x['slug'] != s['slug'] and x['slug'] != 'akce'][:4]
    if s['slug'] == 'akce': rel = [BY[k] for k in ('montaz-dveri-a-oblozek', 'zamecnicke-prace', 'truhlarske-prace', 'zednicke-prace')]
    if len(rel) < 4: rel += [x for x in MAIN if x not in rel and x['slug'] != s['slug']][:4 - len(rel)]
    act = '/nase-sluzby/' if s['menu'] == 'main' else '/dalsi-sluzby/' if s['menu'] == 'other' else s['path']
    render(s['path'], 'service.html', s=s, rel=rel, title=s['seo_title'], description=s['short'], active=act)
render('/cenik/', 'cenik.html', title='Ceník – Levné opravy Praha', description='Doprava po Praze 300 Kč, mimo Prahu 7 Kč/km, výjezd technika na zaměření 500 Kč. Cenovou kalkulaci upřesníme podle Vašich požadavků.', active='/cenik/')
render('/reference/', 'reference.html', title='Reference – Levné opravy Praha', description='Přehled našich realizací – rekonstrukce koupelen, montáže dveří, zahradních domků, kovářské a zámečnické práce.', active='/reference/')
render('/kontakt/', 'kontakt.html', title='Kontakt – Levné opravy Praha', description='Levné opravy – Praha, Na Proseku 35/2, Praha 9. Pobočky v Praze, Brně a Olomouci a montážní servis po celé ČR.', active='/kontakt/')
render('/poptavka/', 'poptavka.html', title='Poptávka – Levné opravy Praha', description='Napište nám, s čím potřebujete pomoct. Cenovou kalkulaci rádi upřesníme podle Vašich požadavků.', active='/poptavka/')
for slug, v in LEGAL.items():
    render('/%s/' % slug, 'legal.html', P=v, title=v['title'] + ' – Levné opravy Praha', description='', active='')
# 404 (absolutní cesta pro GH Pages)
render('/404-tmp/', 'legal.html', P={'title': 'Stránka nenalezena', 'blocks': [{'t': 'p', 'h': 'Tuto stránku jsme nenašli. Zkuste prosím úvodní stránku nebo přehled služeb.'}]}, title='Stránka nenalezena', description='', active='')
h = open(os.path.join(OUT, '404-tmp', 'index.html'), encoding='utf-8').read().replace('href="../', 'href="/levneopravy/').replace('src="../', 'src="/levneopravy/')
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(h); shutil.rmtree(os.path.join(OUT, '404-tmp'))
print('hotovo:', sum(len(f) for _, _, f in os.walk(OUT) if True), 'souborů')
