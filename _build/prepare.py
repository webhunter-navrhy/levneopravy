#!/usr/bin/env python3
"""Z vytěženého obsahu levneopravy.cz (_research/) připraví _data/*.json a img/*.webp."""
import json, os, re
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, '_research')
IMG = os.path.join(ROOT, 'img')
os.makedirs(IMG, exist_ok=True)

def img(name, maxw=1600, q=80):
    src = os.path.join(R, 'img_orig', name)
    base = os.path.splitext(name)[0].lower()
    im = Image.open(src)
    alpha = im.mode in ('RGBA', 'LA', 'P')
    im = im.convert('RGBA' if alpha else 'RGB')
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    out = base + '.webp'
    im.save(os.path.join(IMG, out), 'WEBP', quality=q, method=6)
    return {'src': 'img/' + out, 'w': im.width, 'h': im.height}

def fname(url): return url.rsplit('/', 1)[1]

TYPO = [('Půjčovna mobilních sauny', 'Půjčovna mobilních saun'), ('Kovářské páce', 'Kovářské práce'),
        ('novu kuchyňkou', 'novou kuchyňskou'), ('<strong>i</strong>nstalaci', 'instalaci'), (' i nstalaci', ' instalaci'),
        ('Využijte naši služeb', 'Využijte naše služby'), ('Pro zajišťujeme', 'Proto zajišťujeme'), ('10 990,-Kč', '10 990 Kč'),
        ('práci s kovem', 'prací s kovem'), ('990,-/bm', '990 Kč/bm'), ('190,-/h', '190 Kč/h'), ('obklady,dlažby', 'obklady, dlažby'), ('10 990,- Kč', '10 990 Kč'), ('ve spolupráci s OBI<', 've spolupráci s OBI.<'), ('Zahradnické práce je činnost zabývají', 'Zahradnické práce jsou činnost zabývající se')]
def fix(h):
    for a, b in TYPO: h = h.replace(a, b)
    h = re.sub(r'\s+</strong>', '</strong> ', h); h = re.sub(r'<strong>\s+', ' <strong>', h)
    h = re.sub(r'\s{2,}', ' ', h).strip()
    h = h.replace(' ,', ',').replace(' .', '.')
    if h.endswith('ve spolupráci s OBI'): h += '.'
    return h

SHORT = {
 'bytova-jadra': 'Bydlíte v paneláku a Vaším snem je přestavba bytového jádra?',
 'finske-sauny-a-mobilni-sauny': 'Finské sauny na klíč, mobilní sauny – půjčovna a prodej.',
 'cisteni-odpadu-a-kanalizaci': 'K čištění odpadů a kanalizací používáme profesionální techniku.',
 'elektrikarske-prace': 'Instalace, opravy a údržba elektrických systémů a zařízení.',
 'instalaterske-prace': 'Instalace, opravy a údržba vodovodních systémů, topení a další.',
 'malirske-prace': 'Malířské práce zahrnují přípravu povrchů a následnou aplikaci nátěru.',
 'markyzy-a-rolety': 'Venkovní stínící systémy sloužící k ochraně před slunečním zářením.',
 'montaz-kuchyni': 'Montujeme kuchyňské linky Ikea, Oresi, Jena nábytek, XXXLutz a další.',
 'obkladacske-prace': 'Zaměřujeme se na instalaci obkladů a dlažeb na různé povrchy.',
 'opravy-elektrospotrebicu': 'Zabýváme se opravou a servisem různých domácích spotřebičů.',
 'podlaharske-prace': 'Realizujeme instalaci, opravy a údržbu podlahových povrchů.',
 'truhlarske-prace': 'Výroba, opravy a údržba dřevěných konstrukcí a předmětů.',
 'zahradni-domky': 'Zahradní domky od společností OBI, Weka, Biohort nebo Maone.',
 'zamecnicke-prace': 'Výroba, instalace a údržba kovových konstrukcí a zařízení.',
 'zednicke-prace': 'Naši zkušení zedníci pracují na stavbě nových budov nebo rekonstrukcích.',
 'vyklizeci-prace': 'Nabízíme vyklízení různých prostorů od nepotřebných věcí.',
 'stehovani-a-doprava': 'Stěhujete se a nemáte vhodné auto na odvoz starého nábytku?',
 'kovarske-prace': 'Dejte svému domovu osobitý vzhled, vlastní energii, dejte mu originalitu.',
 'pravidelna-udrzba-domu': 'Hledáte firmu na pravidelnou správu a údržbu nemovitostí? Jsme tu pro Vás!',
 'strechy-a-klempirske-prace': 'Specializujeme se na práci s plechy a různými kovovými materiály.',
 'vyskove-prace': 'Práce prováděné ve výškách, kde je přístup k místům omezený.',
 'zahradnicke-prace': 'Provádíme pravidelnou údržbu zahrad s individuálním přístupem.',
 'montaz-dveri-a-oblozek': 'Jsme odborníky na montáž dveří a obložek, které dodávají funkčnost i estetický vzhled vašeho interiéru.',
 'akce': 'Akční výměna vchodových a bytových dveří bez bourání – 10 990 Kč včetně dopravy, materiálu i práce.',
}
MAIN = ['bytova-jadra', 'finske-sauny-a-mobilni-sauny', 'cisteni-odpadu-a-kanalizaci', 'elektrikarske-prace', 'instalaterske-prace',
        'malirske-prace', 'markyzy-a-rolety', 'montaz-kuchyni', 'obkladacske-prace', 'opravy-elektrospotrebicu', 'podlaharske-prace',
        'truhlarske-prace', 'zahradni-domky', 'zamecnicke-prace', 'zednicke-prace']
OTHER = ['vyklizeci-prace', 'stehovani-a-doprava', 'kovarske-prace', 'pravidelna-udrzba-domu', 'strechy-a-klempirske-prace', 'vyskove-prace', 'zahradnicke-prace']
GROUP = {}
for s in ['montaz-dveri-a-oblozek', 'bytova-jadra', 'instalaterske-prace', 'elektrikarske-prace', 'obkladacske-prace', 'podlaharske-prace', 'malirske-prace', 'montaz-kuchyni', 'opravy-elektrospotrebicu', 'cisteni-odpadu-a-kanalizaci']: GROUP[s] = 'byt'
for s in ['zahradni-domky', 'zahradnicke-prace', 'markyzy-a-rolety', 'strechy-a-klempirske-prace', 'zednicke-prace', 'finske-sauny-a-mobilni-sauny', 'vyskove-prace']: GROUP[s] = 'dum'
for s in ['zamecnicke-prace', 'kovarske-prace', 'truhlarske-prace']: GROUP[s] = 'kov'
for s in ['pravidelna-udrzba-domu', 'vyklizeci-prace', 'stehovani-a-doprava']: GROUP[s] = 'udrzba'
SHORTNAME = {'opravy-elektrospotrebicu': 'Opravy spotřebičů', 'finske-sauny-a-mobilni-sauny': 'Finské a mobilní sauny'}

raw = json.load(open(os.path.join(R, 'services_raw.json'), encoding='utf-8'))
services = []
for slug in ['montaz-dveri-a-oblozek'] + MAIN + OTHER + ['akce']:
    v = raw[slug]
    blocks, cover, lead = [], None, None
    for b in v['blocks']:
        if b['t'] == 'img':
            if not cover: cover = img(fname(b['src']))
            continue
        if b['t'] == 'h' and lead is None: lead = fix(b['h']); continue
        if b['t'] == 'p':
            h = fix(b['h']); t = re.sub('<[^>]+>', '', h).strip()
            if '<a' not in h and ((len(t) < 95 and (t.endswith(':') or t.endswith('?') or re.fullmatch(r'<strong>[^<]*</strong>[?!.]?', h))) or (len(t) < 70 and not t.endswith('.'))):
                blocks.append({'t': 'sub', 'h': t[0].upper() + t[1:]})
            else:
                blocks.append({'t': 'p', 'h': h})
        elif b['t'] == 'ul':
            items = [fix(x) for x in b['items']]
            if blocks and blocks[-1]['t'] == 'ul': blocks[-1]['items'] += items
            else: blocks.append({'t': 'ul', 'items': items, 'rich': all('<a' not in x for x in items) and sum((' – ' in x or ': ' in x) for x in items) >= max(2, len(items) // 2)})
    # u položek „Název – popis“ rozdělit na titulek a text
    for b in blocks:
        if b['t'] == 'ul' and b['rich']:
            its = []
            for x in b['items']:
                m = re.match(r'^(.{3,60}?)\s*[–:]\s+(.*)$', re.sub('<[^>]+>', '', x))
                its.append({'t': m.group(1), 'd': m.group(2)} if m else {'t': '', 'd': x})
            b['items'] = its
    gallery = []
    if slug == 'zahradni-domky':
        gallery = [img(f, 900) for f in ['zahradni-domky-vybaveni15.webp', 'zahradni-domky-vybaveni16.webp', 'zahradni-domky-vybaveni17.webp', 'zahradni_domek.webp', 'zahradni_domky.webp', 'montovanydum2.webp']]
    if slug == 'kovarske-prace':
        gallery = [img(f, 900) for f in ['Kovany-plot-s-listy.webp', 'Samonosna-brana-zdobna-s-patinou.webp', 'schodite_tocene_kovar.webp', 'Litinove-zabradli-zdobne.webp', 'brana_vjezdova_kovar.webp', 'Zabradli-zdobne-s-patinou.webp']]
    if slug == 'zamecnicke-prace':
        gallery = [img(f, 900) for f in ['Branka-s-vyplni-tahokov.webp', 'Dvoukridla-branka-plechy.webp', 'mrize_brna_zabradli.webp', 'oploceni-plny-plech.webp']]
    if slug == 'akce':
        gallery = [img(f, 600) for f in ['dvere3-lo-26.webp', 'dvere-lo-26.webp', 'dvere2-lo-26.webp', 'kukatko-lo-26.webp', 'kovani-lo-26.webp', 'fab-lo-26.webp']]
        lead = 'Nabízíme akční výměnu vchodových a bytových dveří bez bourání.'
        blocks = [b for b in blocks if not (b['t'] in ('p', 'sub') and ('Nabízíme akční výměnu' in b['h'] or 'Uvedená cena' in b['h']))]
    if slug == 'zahradni-domky':
        cover = img('zahradni-domek-zahrada-2026.png')
    services.append({'slug': slug, 'path': '/sluzba/%s/' % slug, 'title': v['title'] if slug != 'akce' else 'Akce: výměna dveří',
        'short_title': SHORTNAME.get(slug, v['title']),
        'seo_title': v['seo_title'], 'short': SHORT[slug], 'lead': lead, 'cover': cover, 'blocks': blocks, 'gallery': gallery,
        'menu': 'main' if slug in MAIN else 'other' if slug in OTHER else 'top', 'group': GROUP.get(slug, 'akce')})
json.dump(services, open(os.path.join(ROOT, '_data', 'services.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

legal = json.load(open(os.path.join(R, 'legal_raw.json'), encoding='utf-8'))
for k, v in legal.items():
    for b in v['blocks']:
        if 'h' in b: b['h'] = fix(b['h'])
        if 'items' in b: b['items'] = [fix(x) for x in b['items']]
json.dump(legal, open(os.path.join(ROOT, '_data', 'legal.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# obrázky pro úvod, reference, loga
media = {}
for f, w in [('levne-opravy-title.webp', 2000), ('firemni-auto-levne-opravy.webp', 900), ('kontakty.webp', 1400), ('slide1.webp', 1600),
             ('slide2.webp', 1600), ('slide3.webp', 1600), ('kuchyne_na_miru.webp', 1000), ('rekonstrukce_bytoveho_jadra1.webp', 1000)]:
    media[os.path.splitext(f)[0].lower()] = img(f, w)
for f in ['logo-opravy.webp', 'logo-opravy-white.webp', 'logo-ikona.webp', 'obi_partner.png', 'rsd_partner.png', 'letiste_partner.png',
          'benzina_partner.png', 'prodoma_partner.png', 'obi-logo.webp', 'obi_partner-akce-e1782287303359.png']:
    media[os.path.splitext(f)[0].lower()] = img(f, 800, 95)
REF = ['rekonstrukce_bytoveho_jadra1.webp', 'zahradni_domky.webp', 'schodite_tocene_kovar.webp', 'Zabradli-zdobne-s-patinou.webp', 'kuchyne_na_miru.webp',
       'zahradni_domek.webp', 'Branka-s-vyplni-tahokov.webp', 'vystavba_domu.webp', 'oprava_domu.webp', 'firemni-auto-levne-opravy.webp',
       'Dvoukridla-brana-Repy.webp', 'zabadli_zdobene.webp', 'mrize_brna_zabradli.webp', 'zabradli-derovane-na-balkony.webp',
       'Dvoukridla-branka-plechy.webp', 'pojezdova-brana-kovane-oploceni.webp', 'montovanydum2.webp', 'Litinove-zabradli-zdobne.webp',
       'Samonosna-brana-zdobna-s-patinou.webp', 'oploceni-plny-plech.webp', 'samonosna-zdobna-brana.webp', 'stavba_domu.webp',
       'zabradli_kvalitni.webp', 'Kovany-plot-s-listy.webp']
media['reference'] = [img(f, 1000) for f in REF]
json.dump(media, open(os.path.join(ROOT, '_data', 'media.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# obrys ČR pro mapu poboček (SVG path, rovnoběžkové zkreslení cos(49,8°))
import math
g = json.load(open(os.path.join(R, 'cze50.json')))
ring = g['coordinates'][0]
k = math.cos(math.radians(49.8))
X0, X1, Y0, Y1 = 12.09, 18.86, 48.55, 51.06
W = 1000; H = round(W * (Y1 - Y0) / ((X1 - X0) * k))
def P(lon, lat): return (round((lon - X0) / (X1 - X0) * W, 1), round((Y1 - lat) / (Y1 - Y0) * H, 1))
d = 'M' + ' L'.join('%s %s' % P(*c) for c in ring) + ' Z'
json.dump({'path': d, 'w': W, 'h': H, 'box': [X0, X1, Y0, Y1]}, open(os.path.join(ROOT, '_data', 'map.json'), 'w'), ensure_ascii=False)
print('ok', len(services), 'služeb; mapa', W, 'x', H)
