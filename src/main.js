(() => {
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];

  // hlavička + mobilní menu
  const hdr = $('#hdr'), burger = $('.burger'), mnav = $('#mnav');
  const onScroll = () => hdr.classList.toggle('is-scrolled', scrollY > 10);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const setHH = () => document.documentElement.style.setProperty('--hh', hdr.getBoundingClientRect().bottom + 'px');
  burger && burger.addEventListener('click', () => {
    const open = burger.getAttribute('aria-expanded') !== 'true';
    setHH();
    burger.setAttribute('aria-expanded', open); mnav.hidden = !open; document.body.classList.toggle('menu-open', open);
  });

  // nadpisy po slovech
  $$('[data-split]').forEach(h => {
    const words = h.textContent.trim().split(/\s+/);
    h.innerHTML = words.map((w, i) => `<span class="w"><span style="--i:${i}">${w.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</span></span>`).join(' ');
  });

  // reveal
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
  $$('.reveal, [data-map]').forEach(el => io.observe(el));

  // vyhledávač služeb v úvodu
  const fq = $('#finder-q'), fr = $('#finder-res');
  if (fq && window.FINDER) {
    const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    const SYN = { dvere: 'dveř zárub oblož', koupelna: 'jádr obklad instal sprch', kuchyn: 'kuchyň', elektrika: 'elektr zásuv', voda: 'instal odpad', zahrada: 'zahrad domk', plot: 'kovář zámeč', brana: 'kovář zámeč', strecha: 'střech klemp', malovani: 'malíř', podlaha: 'podlah', pracka: 'spotřeb', sauna: 'saun', stehovani: 'stěhov vyklíz', zamek: 'zámeč' };
    const data = window.FINDER.map(x => ({ ...x, n: norm(x.t + ' ' + x.d) }));
    let sel = -1;
    const render = () => {
      const q = norm(fq.value.trim());
      if (!q) { fr.hidden = true; return; }
      let terms = [q];
      Object.entries(SYN).forEach(([k, v]) => { if (k.startsWith(q.slice(0, 4)) || q.startsWith(k.slice(0, 4))) terms.push(...norm(v).split(' ')); });
      const hits = data.filter(x => terms.some(t => x.n.includes(t))).slice(0, 6);
      sel = -1;
      fr.innerHTML = hits.length ? hits.map(x => `<li><a href="${window.ROOT}${x.p}/"><b>${x.t}</b><small>${x.d}</small></a></li>`).join('')
        : `<li class="finder__none">Nic jsme nenašli – <a href="${window.ROOT}poptavka/">napište nám</a>, poradíme.</li>`;
      fr.hidden = false;
    };
    fq.addEventListener('input', render);
    fq.addEventListener('focus', render);
    fq.addEventListener('keydown', e => {
      const a = $$('a', fr); if (!a.length) return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + a.length) % a.length; a.forEach((x, i) => x.classList.toggle('is-on', i === sel)); }
      if (e.key === 'Enter') { e.preventDefault(); (a[sel] || a[0]).click(); }
      if (e.key === 'Escape') fr.hidden = true;
    });
    document.addEventListener('click', e => { if (!e.target.closest('[data-finder]')) fr.hidden = true; });
  }

  // filtr služeb
  const grid = $('[data-grid]');
  $$('.chip').forEach(ch => ch.addEventListener('click', () => {
    $$('.chip').forEach(c => { c.classList.toggle('is-on', c === ch); c.setAttribute('aria-selected', c === ch); });
    const f = ch.dataset.filter;
    $$('.card', grid).forEach((c, i) => {
      const show = f === 'vse' || c.dataset.group === f;
      c.classList.toggle('is-hidden', !show);
      c.classList.remove('is-in');
      if (show) { void c.offsetWidth; c.style.animationDelay = (i % 8) * 40 + 'ms'; c.classList.add('is-in'); }
    });
    grid.classList.toggle('is-filtered', f !== 'vse');
    const big = $('.card--big', grid); if (big) big.classList.toggle('card--big-off', f !== 'vse');
  }));

  // mapa poboček
  $$('[data-map]').forEach(map => {
    const tip = $('.cz__tip', map), svg = $('svg', map);
    const show = g => {
      const r = g.getBoundingClientRect(), mr = map.getBoundingClientRect();
      $('b', tip).textContent = 'Montážní servis – ' + g.dataset.n; $('span', tip).textContent = g.dataset.a;
      tip.style.left = (r.left + r.width / 2 - mr.left) + 'px'; tip.style.top = (r.top + r.height / 2 - mr.top) + 'px'; tip.hidden = false;
      $$('.cz__pin', svg).forEach(p => p.classList.toggle('is-on', p === g));
    };
    const hide = () => { tip.hidden = true; $$('.cz__pin', svg).forEach(p => p.classList.remove('is-on')); };
    $$('.cz__pin', svg).forEach(g => { g.addEventListener('mouseenter', () => show(g)); g.addEventListener('focus', () => show(g)); g.addEventListener('click', () => show(g)); g.addEventListener('mouseleave', hide); g.addEventListener('blur', hide); });
    const list = map.parentElement.querySelector('.branches');
    list && $$('li', list).forEach(li => {
      const g = $$('.cz__pin', svg).find(p => p.dataset.n === li.dataset.n);
      const on = () => { $$('li', list).forEach(x => x.classList.toggle('is-on', x === li)); g && show(g); };
      li.addEventListener('mouseenter', on); li.addEventListener('focus', on); li.addEventListener('click', on);
    });
  });

  // ukázkový formulář
  const q = new URLSearchParams(location.search).get('sluzba');
  $$('form[data-demo]').forEach(f => {
    if (q) { const s = $('select[name=sluzba]', f); if (s && [...s.options].some(o => o.value === q)) s.value = q; }
    f.addEventListener('submit', e => { e.preventDefault(); const m = $('.form__msg', f); m.hidden = false; m.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); });
  });

  // lightbox
  $$('[data-lb]').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    const lb = document.createElement('div'); lb.className = 'lb';
    lb.innerHTML = `<img src="${a.getAttribute('href')}" alt=""><button aria-label="Zavřít">×</button>`;
    const close = () => { lb.remove(); removeEventListener('keydown', k); };
    const k = ev => ev.key === 'Escape' && close();
    lb.addEventListener('click', close); addEventListener('keydown', k);
    document.body.appendChild(lb);
  }));
})();
