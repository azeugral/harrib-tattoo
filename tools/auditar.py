# -*- coding: utf-8 -*-
"""Auditoria automática: estouro horizontal, texto cortado, assimetria, erros de console, em todas as larguras.
Uso: python tools/auditar.py [url] [--fotos]"""
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf8')
URL = next((a for a in sys.argv[1:] if a.startswith('http')), 'http://localhost:8877/')
FOTOS = '--fotos' in sys.argv
SAI = Path(sys.argv[0]).resolve().parent.parent.parent / '_ref/auditoria'
SAI.mkdir(exist_ok=True)
VPS = [(320, 640, 1), (360, 740, 1), (390, 844, 1), (430, 932, 1), (600, 900, 1), (768, 1024, 1), (844, 390, 1), (1024, 768, 0), (1280, 720, 0), (1440, 900, 0), (1920, 1080, 0), (2560, 1300, 0)]
JS = r"""
() => {
  const W = document.documentElement.clientWidth, out = [];
  if (document.documentElement.scrollWidth > W) out.push('ESTOURO pagina ' + document.documentElement.scrollWidth + '>' + W);
  const sel = 'h1,h2,h3,p,a,button,span,small,q,b,label,summary,address,blockquote,cite,li,option';
  document.querySelectorAll(sel).forEach(el => {
    if (el.closest('.faixa,[hidden],.sr,.saltar')) return;
    const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
    const nome = el.tagName + '.' + el.className + ' "' + (el.textContent || '').trim().slice(0, 28) + '"';
    if (el.closest('.arco.fixo .pista')) { }
    else if (r.right > W + 1 || r.left < -1) out.push('FORA ' + nome + ' ' + Math.round(r.left) + '-' + Math.round(r.right));
    if (el.scrollWidth > el.clientWidth + 1 && cs.display !== 'inline' && el.clientWidth > 0) out.push('CORTE-X ' + nome + ' ' + el.scrollWidth + '>' + el.clientWidth);
    if (el.scrollHeight > el.clientHeight + 2 && cs.display !== 'inline' && el.clientHeight > 0 && cs.overflow !== 'visible' ) out.push('CORTE-Y ' + nome);
    // antepassado que recorta
    if (el.children.length === 0 && el.textContent.trim()) {
      let p = el.parentElement;
      while (p && p !== document.body) { const c = getComputedStyle(p);
        if (c.overflow !== 'visible' && !p.matches('.hero,.arco-pin,.orc,.faixa,.ret,.lb-t')) { const q = p.getBoundingClientRect(); if (r.bottom > q.bottom + 1 || r.right > q.right + 1 || r.top < q.top - 1) out.push('RECORTADO ' + nome + ' por ' + p.className); }
        p = p.parentElement; }
    }
  });
  // hero cabe na tela?
  const h = document.querySelector('.hero').getBoundingClientRect(), b = document.querySelector('.hero-bts').getBoundingClientRect(), n = document.querySelector('.hero h1').getBoundingClientRect(), t = document.querySelector('.topo-in').getBoundingClientRect();
  if (b.bottom > h.bottom - 4) out.push('HERO botoes cortados');
  if (n.top < t.bottom - 40) out.push('HERO logo sob o topo ' + Math.round(n.top));
  // simetria do miolo do hero
  const mx = (n.left + n.right) / 2; if (Math.abs(mx - W / 2) > 1.5) out.push('HERO logo fora do eixo ' + (mx - W / 2).toFixed(1));
  // grades: colunas com a mesma largura e altura
  document.querySelectorAll('.grade,.estilos,.reels,.falas').forEach(g => {
    const v = [...g.children].filter(c => c.getBoundingClientRect().width > 0 && !c.hidden);
    const w = new Set(v.map(c => Math.round(c.getBoundingClientRect().width))); if (w.size > 1) out.push('GRADE larguras ' + g.className + ' ' + [...w]);
  });
  return [...new Set(out)];
}
"""
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'])
    tot = 0
    for w, h, tq in VPS:
        c = b.new_context(viewport={'width': w, 'height': h}, has_touch=bool(tq), is_mobile=bool(tq), device_scale_factor=1)
        g = c.new_page()
        erros = []
        g.on('pageerror', lambda e: erros.append('JS ' + str(e)[:200]))
        g.on('console', lambda m: erros.append('CON ' + m.text[:200]) if m.type == 'error' else None)
        g.on('requestfailed', lambda r: erros.append('REQ ' + r.url[-60:]) if 'mp4' not in r.url else None)
        g.on('response', lambda r: erros.append(f'{r.status} ' + r.url[-60:]) if r.status >= 400 else None)
        g.goto(URL, wait_until='domcontentloaded')
        g.wait_for_timeout(1800)
        g.evaluate("document.fonts.ready")
        if FOTOS:
            g.wait_for_timeout(1400)
            g.screenshot(path=str(SAI / f'{w}-hero.jpg'), type='jpeg', quality=80)
        r = g.evaluate(JS)
        # rola a página toda para acionar entradas e lazy
        H = g.evaluate("document.documentElement.scrollHeight")
        y = 0
        while y < H:
            g.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})")
            g.wait_for_timeout(50)
            y += int(h * .8)
        g.evaluate("window.scrollTo({top:0,behavior:'instant'})")
        g.wait_for_timeout(200)
        r += [x for x in g.evaluate(JS) if x not in r]
        ok = not r and not erros
        print(f'{w}x{h}', 'OK' if ok else '', 'altura', H)
        for x in r[:25] + erros[:8]:
            print('   ', x)
        tot += len(r) + len(erros)
        if FOTOS and w in (390, 1440):
            for k in range(0, 40):
                top = k * int(h * .92)
                if top > H: break
                g.evaluate(f"window.scrollTo({{top:{top},behavior:'instant'}})")
                g.wait_for_timeout(350)
                g.screenshot(path=str(SAI / f'{w}-{k:02}.jpg'), type='jpeg', quality=72)
        c.close()
    b.close()
print('PROBLEMAS:', tot)
