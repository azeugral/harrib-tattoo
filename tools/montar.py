# -*- coding: utf-8 -*-
"""Monta index.html a partir de tools/modelo.html e tools/dados.py. Uso: python tools/montar.py"""
import json, re, sys, time
from html import escape as e
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from dados import TRABALHOS, FILTROS, ARCO, FALAS, WHATS

SITE = Path(__file__).resolve().parent.parent
logo = (SITE / 'assets/img/logo.svg').read_text()
vb = re.search(r'viewBox="([^"]+)"', logo).group(1)
caminho = re.search(r'(<path .*?/>)', logo, re.S).group(1)
SIMBOLO = f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="lg" viewBox="{vb}">{caminho}</symbol></svg>'
logo = f'<svg viewBox="{vb}" aria-hidden="true" focusable="false"><use href="#lg"/></svg>'

EST = [('manga', 'Mangá e anime', 'Preto cheio, retícula e composição de página.', 'chrollo'),
       ('cyber', 'Cybertribal', 'Linhas de espinho que acompanham o corpo.', 'autoral'),
       ('floral', 'Floral e traço fino', 'Lírios e folhagens de linha delicada.', 'lirio'),
       ('black', 'Blackwork', 'Máscaras, insetos e arte autoral em preto.', 'hannya')]
ESTILOS = ''.join(f'<button class="est" data-f="{f}" data-rv><span class="art"><i style="-webkit-mask-image:url(assets/img/tinta/{o}-orn.webp);mask-image:url(assets/img/tinta/{o}-orn.webp)"></i></span><span class="tx"><h3>{e(t)}</h3><p>{e(d)}</p></span></button>' for f, t, d, o in EST)

FILT = ''.join(f'<button data-f="{f}" aria-pressed="{"true" if f == "todos" else "false"}">{e(t)}</button>' for f, t in FILTROS)

cards = []
dados = {}
for id_, tit, nota, cats, capa, fy, extras, fala in TRABALHOS:
    ms = []
    vid = None
    for n in [capa] + extras:
        if (SITE / f'assets/video/{n}.mp4').exists():
            ms.append({'a': n, 'v': 1})
            vid = vid or n
        if (SITE / f'assets/img/g/{n}.webp').exists() and not (SITE / f'assets/video/{n}.mp4').exists():
            ms.insert(0 if n == capa else len(ms), {'a': n})
    # foto antes do vídeo
    ms.sort(key=lambda m: m.get('v', 0))
    dados[id_] = {'t': tit, 'n': nota, 'q': fala, 'c': cats[0], 'm': ms}
    dv = f' data-v="{vid}"' if vid else ''
    cards.append(f'<button class="card" data-id="{id_}" data-cat="{" ".join(cats)}"{dv} aria-label="{e(tit)}, abrir"><span class="ft"><img src="assets/img/p/{id_}.webp" alt="Tatuagem {e(tit)}, {e(nota)}" loading="lazy" width="720" height="900" draggable="false"></span><h3>{e(tit)}</h3><small>{e(nota)}</small></button>')

COMP = [('chrollo', 'Chrollo'), ('besouro', 'Besouro'), ('capuz', 'Capuz'), ('hannya', 'Hannya'), ('lirio', 'Lírio')]
ESCOLHE = ''.join(f'<button data-n="{n}" aria-pressed="{"true" if i == 0 else "false"}">{t}</button>' for i, (n, t) in enumerate(COMP))

ARC = ''.join(f'<article class="koma" data-rv><div class="ft"><img src="assets/img/arco/{i}.webp" alt="{e(t)}" loading="lazy" draggable="false"><span class="nar">{m}</span></div><div class="tx"><h3>{e(t)}</h3><p>{e(q)}</p></div></article>' for i, m, t, q, *_ in ARCO)

REELS = ''.join(f'<div class="reel" data-rv><img src="assets/video/{n}.webp" alt="" loading="lazy"><video muted loop playsinline preload="none" data-src="assets/video/{n}.mp4" aria-label="{e(t)}"></video><span>{e(t)}</span></div>' for n, t in (('007_0', 'Mão em andamento'), ('034_0', 'Fine art do Zoro'), ('001_1', 'Anime em vermelho')))

# balões: dois redondos, dois de grito, em espelho
REDONDO_E = '<svg viewBox="0 0 400 220" preserveAspectRatio="none" aria-hidden="true"><path d="M200 8C310 8 392 48 392 104s-82 92-158 94l-52 20 12-20C92 196 8 160 8 104S90 8 200 8Z" fill="#f7f3ea" stroke="#09090a" stroke-width="3" vector-effect="non-scaling-stroke"/></svg>'
REDONDO_D = REDONDO_E.replace('<path ', '<path transform="matrix(-1 0 0 1 400 0)" ')
def grito(sem):
    import numpy as np
    r = np.random.default_rng(sem); pts = []; N = 22
    for k in range(N * 2):
        a = 2 * np.pi * k / (N * 2)
        rx, ry = (196, 106) if k % 2 == 0 else (168, 84)
        j = r.uniform(.95, 1.05)
        pts.append(f'{200 + np.cos(a) * rx * j:.1f},{110 + np.sin(a) * ry * j:.1f}')
    return f'<svg viewBox="0 0 400 220" preserveAspectRatio="none" aria-hidden="true"><polygon points="{" ".join(pts)}" fill="#f7f3ea" stroke="#09090a" stroke-width="3" vector-effect="non-scaling-stroke"/></svg>'
FORMAS = [grito(2), REDONDO_D, REDONDO_E, grito(5)]
FAL = ''.join(f'<figure class="fala" data-rv>{FORMAS[i]}<q>{e(q)}</q><b>{e(q2)}</b></figure>' for i, (q, q2, _) in enumerate(FALAS))

FAIXA = ''.join(f'<span>{t}</span>' for t in ['PERSONAGENS', 'IDEIAS', 'HISTÓRIAS', 'NA PELE', 'TRAÇO', 'ARTE', 'LIBERDADE', 'SEMPRE'] * 6)
CHIPS = ''.join(f'<button type="button" aria-pressed="false">{e(t)}</button>' for t in ['Mangá e anime', 'Cybertribal', 'Floral e traço fino', 'Blackwork', 'Com cor', 'Ainda não sei'])

JS = json.dumps({'whats': WHATS, 't': dados}, ensure_ascii=False, separators=(',', ':'))
h = (SITE / 'tools/modelo.html').read_text(encoding='utf8')
for k, v in {'LOGO': logo, 'SIMBOLO': SIMBOLO, 'ESTILOS': ESTILOS, 'FILTROS': FILT, 'CARDS': ''.join(cards), 'ESCOLHE': ESCOLHE, 'ARCO': ARC, 'REELS': REELS, 'FALAS': FAL, 'FAIXA': FAIXA, 'CHIPS': CHIPS, 'JSON': JS, 'V': str(int(time.time()))}.items():
    h = h.replace('{{' + k + '}}', v)
(SITE / 'index.html').write_text(h, encoding='utf8')
print(len(h) // 1024, 'KB')
