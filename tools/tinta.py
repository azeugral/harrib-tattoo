"""Tira a tinta da pele: acha o braço pela cor da pele, compara cada ponto com a pele vizinha e sobra só o traço.
Saída em _ref/tinta/<nome>.png (L = traço, fundo branco), duas vezes maior que a foto de origem quando ela é pequena.
Uso: python tools/tinta.py"""
import cv2, numpy as np, os, sys
from pathlib import Path
R = Path.home() / 'Documents/PROJETOS LRGZ/Harrib Tattoo/_ref'
(R / 'tinta').mkdir(exist_ok=True)

# nome: (arquivo, recorte x0,y0,x1,y1 em fração, limiar, rotação)
PECAS = {
    'chrollo': ('002_0', (.13, .03, .74, .98), .62, 0),
    'besouro': ('003_1', (.10, .12, .90, .80), .60, 0),
    'hannya':  ('018_1', (.22, .06, .78, .96), .60, 0),
    'uzumaki': ('011_1', (.08, .10, .98, .86), .60, 0),
    'capuz':   ('019_0', (.16, .08, .84, .90), .60, 0),
    'tomie':   ('013_0', (.10, .02, .90, .98), .60, 0),
    'lirio':   ('015_1', (.04, .02, .96, .98), .55, 0),
    'caveira': ('006_1', (.08, .02, .92, .98), .60, 0),
    'gohan':   ('010_1', (.00, .00, 1.0, 1.0), .62, 0),
    'jester':  ('022_0', (.10, .02, .90, .98), .60, 0),
    'autoral': ('016_1', (.20, .00, .95, 1.0), .60, 0),
}


from rembg import remove, new_session
SESSAO = new_session('isnet-general-use')


def arm_mask(bgr):
    """Braço/pessoa por rembg; a tinta preta nunca fica de fora porque o recorte é da silhueta."""
    h, w = bgr.shape[:2]
    p = cv2.resize(bgr, (1024, 1024), interpolation=cv2.INTER_AREA)
    m = remove(p, session=SESSAO, only_mask=True)
    m = np.array(m)
    m = cv2.resize(m, (w, h), interpolation=cv2.INTER_LINEAR)
    m = (m > 110).astype(np.uint8)
    n, l, s, _ = cv2.connectedComponentsWithStats(m)
    m = (l == 1 + np.argmax(s[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    return m, None


def tinta(nome, arq, caixa, lim):
    im = cv2.imread(str(R / 'ig' / f'{arq}.jpg'))
    h, w = im.shape[:2]
    x0, y0, x1, y1 = [int(v * d) for v, d in zip(caixa, (w, h, w, h))]
    # toda peça sai em 4:5 para a moldura do comparador nunca sobrar
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    cw, ch = x1 - x0, y1 - y0
    if cw / ch < .8: cw = ch * .8
    else: ch = cw / .8
    if cw > w: cw, ch = w, w / .8
    if ch > h: cw, ch = h * .8, h
    x0 = int(max(0, min(w - cw, cx - cw / 2))); y0 = int(max(0, min(h - ch, cy - ch / 2)))
    x1, y1 = int(x0 + cw), int(y0 + ch)
    c = im[y0:y1, x0:x1]
    alvo = 2600
    esc = alvo / max(c.shape[:2])
    c = cv2.resize(c, None, fx=esc, fy=esc, interpolation=cv2.INTER_CUBIC if esc > 1 else cv2.INTER_AREA)
    c = cv2.fastNlMeansDenoisingColored(c, None, 4, 4, 5, 15) if esc > 1 else c
    m, med = arm_mask(c)
    L = cv2.cvtColor(c, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32)
    # pele local: fechamento + borrão apaga o traço e mantém a luz do braço
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))
    fundo = cv2.GaussianBlur(cv2.morphologyEx(L, cv2.MORPH_CLOSE, k), (0, 0), 30)
    r = L / np.maximum(fundo, 1)
    a = np.clip((lim + .08 - r) / .16, 0, 1)   # borda suave do traço
    # preto sólido (cabelo) maior que o fechamento: pega pelo escuro absoluto em relação à pele
    pele = np.percentile(L[m > 0], 70)
    a = np.maximum(a, np.clip((pele * .42 + 10 - L) / 20, 0, 1))
    a = a * cv2.GaussianBlur(cv2.erode(m, np.ones((15, 15), np.uint8)).astype(np.float32), (0, 0), 3)
    a = cv2.GaussianBlur(a, (0, 0), .8)
    a = np.clip((a - .35) / .3, 0, 1)
    # tira pontinhos soltos (poros, pelos)
    b = (a > .5).astype(np.uint8)
    n, l, s, _ = cv2.connectedComponentsWithStats(b, connectivity=8)
    ok = np.zeros(n, bool)
    ok[1:] = s[1:, cv2.CC_STAT_AREA] > 60
    a = a * cv2.dilate(ok[l].astype(np.uint8), np.ones((3, 3), np.uint8))
    out = (255 * (1 - a)).astype(np.uint8)
    cv2.imwrite(str(R / 'tinta' / f'{nome}.png'), out)
    cv2.imwrite(str(R / 'tinta' / f'{nome}_foto.jpg'), c, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(nome, out.shape, round(float(a.mean()), 3))


alvo = sys.argv[1:] or PECAS
for n in alvo:
    arq, cx, lim, _ = PECAS[n]
    tinta(n, arq, cx, lim)

# folha de conferência
nomes = sorted(p.stem for p in (R / 'tinta').glob('*.png'))
T = 360
f = np.full((T, T * 5, 3), 255, np.uint8)
L = []
for n in nomes:
    i = cv2.imread(str(R / 'tinta' / f'{n}.png'))
    s = T / max(i.shape[:2])
    i = cv2.resize(i, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    t = np.full((T, T, 3), 255, np.uint8)
    t[:i.shape[0], :i.shape[1]] = i
    L.append(t)
linhas = [np.hstack(L[j:j + 5] + [np.full((T, T, 3), 255, np.uint8)] * (5 - len(L[j:j + 5]))) for j in range(0, len(L), 5)]
cv2.imwrite(str(R / 'tinta-folha.jpg'), np.vstack(linhas))
