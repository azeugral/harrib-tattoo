# -*- coding: utf-8 -*-
"""Gera todas as imagens e vídeos do site a partir de _ref. Uso: python tools/processar.py [capas|hero|tinta|retrato|videos|tudo]"""
import sys, subprocess, shutil
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageOps, ImageEnhance
sys.path.insert(0, str(Path(__file__).parent))
from dados import TRABALHOS, ARCO

SITE = Path(__file__).resolve().parent.parent
REF = SITE.parent / '_ref'
IMG = SITE / 'assets/img'
VID = SITE / 'assets/video'
for d in ('p', 'g', 'hero', 'tinta', 'arco'):
    (IMG / d).mkdir(parents=True, exist_ok=True)
VID.mkdir(parents=True, exist_ok=True)


def abre(nome):
    return ImageOps.exif_transpose(Image.open(REF / 'ig' / f'{nome}.jpg')).convert('RGB')


def corta(im, razao, fy=.5, fx=.5, zoom=1.0):
    w, h = im.size
    if w / h > razao:
        ch, cw = h / zoom, h * razao / zoom
    else:
        cw, ch = w / zoom, w / razao / zoom
    x = max(0, min(w - cw, fx * w - cw / 2))
    y = max(0, min(h - ch, fy * h - ch / 2))
    return im.crop((int(x), int(y), int(x + cw), int(y + ch)))


def capas():
    for id_, tit, _, _, capa, fy, extras, _ in TRABALHOS:
        im = abre(capa)
        corta(im, .8, fy).resize((720, 900), Image.LANCZOS).save(IMG / 'p' / f'{id_}.webp', quality=80, method=6)
        for i, n in enumerate([capa] + extras):
            g = abre(n)
            g.thumbnail((1400, 1400), Image.LANCZOS)
            g.save(IMG / 'g' / f'{n}.webp', quality=82, method=6)
    # folha de conferência dos recortes
    fs = sorted((IMG / 'p').glob('*.webp'))
    T = 240
    S = Image.new('RGB', (T * 8, 300 * ((len(fs) + 7) // 8)), '#222')
    for i, f in enumerate(fs):
        S.paste(Image.open(f).convert('RGB').resize((T, 300)), ((i % 8) * T, (i // 8) * 300))
    S.save(REF / 'folha-capas.jpg', quality=85)


def pb(im, red=False):
    """Preto e branco de contraste alto, papel levemente quente; com red=True a tinta vermelha fica."""
    a = np.asarray(im, np.float32) / 255
    y = a @ np.array([.3, .59, .11], np.float32)
    lo, hi = np.percentile(y, 1), np.percentile(y, 99)
    y = np.clip((y - lo) / (hi - lo), 0, 1)
    y = y ** .92
    y = y * y * (3 - 2 * y) * .55 + y * .45
    o = np.stack([y * .985, y * .955, y * .90], 2)
    if red:
        hsv = cv2.cvtColor((a * 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
        h, s = hsv[..., 0], hsv[..., 1] / 255
        ver = ((h < 8) | (h > 168)).astype(np.float32) * np.clip((s - .38) / .2, 0, 1)
        ver = cv2.GaussianBlur(ver, (0, 0), 1.2)[..., None]
        cor = np.array([.86, .09, .13], np.float32) * (0.35 + .65 * y[..., None])
        o = o * (1 - ver) + cor * ver
    return Image.fromarray((np.clip(o, 0, 1) * 255).astype(np.uint8))


# painel: (arquivo, foco y, foco x, zoom, manter vermelho)
HERO = {
    'e': [('011_0', .42, .55, 1.0, False), ('019_0', .47, .5, 1.05, False), ('015_1', .50, .50, 1.0, True)],
    'c': [('002_0', .47, .46, 1.0, False), ('001_0', .46, .5, 1.0, True), ('010_1', .50, .55, 1.0, False)],
    'd': [('003_0', .46, .52, 1.25, False), ('018_1', .48, .46, 1.0, False), ('006_1', .46, .62, 1.0, False)],
}


def hero():
    for lado, lista in HERO.items():
        for i, (n, fy, fx, z, red) in enumerate(lista):
            im = corta(abre(n), .74, fy, fx, z).resize((1000, 1351), Image.LANCZOS)
            pb(im, red).save(IMG / 'hero' / f'{lado}{i}.webp', quality=78, method=6)


def tinta_webp():
    # tinta + papel, mesma moldura da foto, para o comparador; e alfa puro para os ornamentos
    for n in ('chrollo', 'besouro', 'capuz', 'hannya', 'lirio'):
        L = Image.open(REF / 'tinta' / f'{n}.png').convert('L')
        f = Image.open(REF / 'tinta' / f'{n}_foto.jpg').convert('RGB')
        w, h = L.size
        s = 1100 / max(w, h)
        t = (int(w * s), int(h * s))
        f.resize(t, Image.LANCZOS).save(IMG / 'tinta' / f'{n}-pele.webp', quality=84, method=6)
        q = np.asarray(L.resize(t, Image.LANCZOS), np.float32)[..., None] / 255
        papel = np.array([247, 243, 234], np.float32); tinta = np.array([9, 9, 10], np.float32)
        Image.fromarray((tinta + (papel - tinta) * q).astype(np.uint8)).save(IMG / 'tinta' / f'{n}-traco.webp', quality=86, method=6)
        print(n, t)
    for n in ('chrollo', 'besouro', 'capuz', 'hannya', 'lirio', 'tomie', 'gohan', 'autoral'):
        p = REF / 'tinta' / f'{n}.png'
        if not p.exists():
            continue
        L = Image.open(p).convert('L')
        a = ImageOps.invert(L)
        box = a.getbbox()
        a = a.crop(box)
        a.thumbnail((900, 900), Image.LANCZOS)
        o = Image.merge('LA', (Image.new('L', a.size, 0), a))
        o.save(IMG / 'tinta' / f'{n}-orn.webp', quality=82, method=6)


def retrato():
    """Alisson como página de mangá: preto chapado, retícula nos meios-tons e branco de papel."""
    im = Image.open(REF / 'perfil.jpg').convert('RGB')
    im = im.crop((110, 40, 1010, 1040)).resize((1500, 1667), Image.LANCZOS)
    a = np.asarray(im, np.float32) / 255
    y = a @ np.array([.42, .46, .12], np.float32)  # luz vermelha da foto vira pele clara
    y = cv2.bilateralFilter(y, 9, .12, 7)
    y = np.clip((y - .012) / .40, 0, 1) ** .62
    from rembg import remove, new_session
    corte = np.array(remove(cv2.resize((a * 255).astype(np.uint8), (1024, 1024)), session=new_session('isnet-general-use'), only_mask=True))
    corte = cv2.GaussianBlur(cv2.resize(corte, (y.shape[1], y.shape[0])).astype(np.float32) / 255, (0, 0), 1.5)
    H, W = y.shape
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ang = np.deg2rad(45)
    u = (xx * np.cos(ang) + yy * np.sin(ang)) / 8.5
    v = (-xx * np.sin(ang) + yy * np.cos(ang)) / 8.5
    tela = .5 + .25 * (np.cos(2 * np.pi * u) + np.cos(2 * np.pi * v))
    tom = np.where(y > .80, 1, np.where(y < .10, 0, np.nan))
    meio = np.clip((y - tela * .62 - .10) * 14 + .5, 0, 1)
    o = np.where(np.isnan(tom), meio, tom)
    # fundo vira linhas de foco, como página de apresentação de personagem
    cx, cy = W * .46, H * .36
    ang2 = np.arctan2(yy - cy, xx - cx)
    rr = np.hypot(xx - cx, yy - cy) / H
    rng = np.random.default_rng(7)
    N = 200
    ids = np.floor((ang2 + np.pi) / (2 * np.pi) * N).astype(int) % N
    lar = rng.uniform(.04, .46, N)
    ini = rng.uniform(.34, .72, N)
    fr = ((ang2 + np.pi) / (2 * np.pi) * N) % 1
    tp = np.clip((rr - ini[ids]) / .5, 0, 1)
    lin = (np.abs(fr - .5) < lar[ids] * tp).astype(np.float32) * (rng.uniform(0, 1, N)[ids] > .2)
    lin = cv2.GaussianBlur(lin, (0, 0), .8)
    fundo = 1 - lin
    o = o.astype(np.float32) * corte + fundo * (1 - corte)
    o = cv2.GaussianBlur(o, (0, 0), .7)
    papel = np.array([.925, .90, .855], np.float32)
    tinta = np.array([.035, .035, .04], np.float32)
    out = tinta + (papel - tinta) * o[..., None]
    Image.fromarray((out * 255).astype(np.uint8)).save(IMG / 'alisson.webp', quality=86, method=6)
    im.resize((900, 1000), Image.LANCZOS).save(IMG / 'alisson-foto.webp', quality=84, method=6)


def arco():
    for id_, _, _, _, arq, *_ in ARCO:
        if arq.endswith('_q'):
            im = Image.open(REF / 'q039.jpg').convert('RGB')
        else:
            im = abre(arq)
        c = corta(im, .72, .46).resize((760, 1056), Image.LANCZOS)
        pb(c, id_ in ()).save(IMG / 'arco' / f'{id_}.webp', quality=80, method=6)


def videos():
    ffmpeg = shutil.which('ffmpeg')
    vistos = set()
    for t in TRABALHOS:
        for n in [t[4]] + t[6]:
            src = REF / 'ig' / f'{n}.mp4'
            if not src.exists() or n in vistos:
                continue
            vistos.add(n)
            dst = VID / f'{n}.mp4'
            subprocess.run([ffmpeg, '-y', '-loglevel', 'error', '-i', str(src), '-vf', "scale='min(620,iw)':-2", '-c:v', 'libx264', '-preset', 'slow', '-crf', '29',
                            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', str(dst)], check=True)
            Image.open(REF / 'ig' / f'{n}.jpg').convert('RGB').resize((620, int(620 * Image.open(REF / 'ig' / f'{n}.jpg').size[1] / Image.open(REF / 'ig' / f'{n}.jpg').size[0])), Image.LANCZOS).save(VID / f'{n}.webp', quality=74, method=6)
            print(n, round(dst.stat().st_size / 1e6, 2))
    # reel da seção Na máquina
    for n in ('007_0', '031_0'):
        src = REF / 'ig' / f'{n}.mp4'
        print(n, src.exists())


alvo = sys.argv[1] if len(sys.argv) > 1 else 'tudo'
fns = {'capas': capas, 'hero': hero, 'tinta': tinta_webp, 'retrato': retrato, 'arco': arco, 'videos': videos}
for k, fn in fns.items():
    if alvo in (k, 'tudo'):
        fn()
print('ok')
