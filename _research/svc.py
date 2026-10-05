import re, json, glob, os
from bs4 import BeautifulSoup, NavigableString
def clean_html(el):
    # keep only strong/b/em/br/a(text)
    out=[]
    for c in el.descendants:
        pass
    h=str(el)
    h=re.sub(r'<a [^>]*href="([^"]+)"[^>]*>',lambda m:'<a href="%s">'%m.group(1),h)
    h=re.sub(r'<(?!/?(strong|b|em|br|a)\b)[^>]+>','',h)
    h=re.sub(r'<(/?)b>',r'<\1strong>',h)
    h=re.sub(r'<(strong|em)[^>]*>',r'<\1>',h)
    h=h.replace('\xa0',' ')
    h=re.sub(r'\s+',' ',h).strip()
    h=re.sub(r'\s+([.,!?;:])',r'\1',h)
    h=re.sub(r'<strong>\s*</strong>','',h)
    return h
def blocks_of(root, stop='Oblast působení'):
    B=[]
    for w in root.select('.elementor-widget'):
        t=w.get('data-widget_type','')
        txt=w.get_text(' ',strip=True)
        if txt.startswith(stop): break
        if t.startswith('image'):
            im=w.find('img')
            if im: B.append({'t':'img','src':im.get('src')})
        elif t.startswith('pxl_heading'):
            if txt: B.append({'t':'h','h':txt})
        elif 'text_editor' in t:
            ps=w.find_all('p') or [w.select_one('.elementor-widget-container') or w]
            for p in ps:
                h=clean_html(p)
                if re.sub('<[^>]+>','',h).strip(): B.append({'t':'p','h':h})
        elif 'icon-list' in t or 'list' in t:
            items=[]
            for li in w.find_all('li'):
                for ic in li.select('.elementor-icon-list-icon'): ic.decompose()
                h=clean_html(li)
                h=re.sub(r'^\s*steel\s*','',h)
                if h: items.append(h)
            if items: B.append({'t':'ul','items':items})
        elif t.startswith('pxl_button'):
            pass
        else:
            if txt: B.append({'t':'?','w':t,'txt':txt[:300]})
    return B
res={}
for f in sorted(glob.glob('html/sluzba_*.html')):
    s=BeautifulSoup(open(f,encoding='utf-8').read(),'html.parser')
    roots=s.find_all(attrs={'data-elementor-type':'wp-post'}); root=max(roots,key=lambda r:len(r.select('.elementor-widget'))) if roots else None
    slug=os.path.basename(f)[7:-5]
    title=s.select_one('.pxl-page-title, h1')
    title=title.get_text(' ',strip=True) if title else ''
    md=s.find('meta',attrs={'name':'description'})
    tt=s.find('title').get_text()
    res[slug]={'slug':slug,'title':title,'seo_title':tt,'description':md.get('content') if md else '','blocks':blocks_of(root) if root else []}
json.dump(res,open('services_raw.json','w'),ensure_ascii=False,indent=1)
for k,v in res.items(): print(k,'|',v['title'],'|',v['seo_title'],'|',len(v['blocks']),'|',v['description'][:80])
