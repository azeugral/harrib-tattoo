# -*- coding: utf-8 -*-
"""Imagem de compartilhamento: arte central e logo no meio, porque o WhatsApp recorta em quadrado."""
from pathlib import Path
from playwright.sync_api import sync_playwright
S = Path(__file__).resolve().parent.parent
logo = (S / 'assets/img/logo.svg').read_text()
h = f"""<body style="margin:0;background:#09090a;width:1200px;height:630px;position:relative;overflow:hidden">
<img src="{(S/'assets/img/hero/c0.webp').as_uri()}" style="position:absolute;left:0;top:-160px;width:400px;filter:brightness(.8)">
<img src="{(S/'assets/img/hero/e0.webp').as_uri()}" style="position:absolute;left:400px;top:-120px;width:400px;filter:brightness(.8)">
<img src="{(S/'assets/img/hero/d0.webp').as_uri()}" style="position:absolute;left:800px;top:-150px;width:400px;filter:brightness(.8)">
<div style="position:absolute;inset:0;background:radial-gradient(60% 62% at 50% 54%,rgba(9,9,10,.95) 34%,rgba(9,9,10,.15) 100%)"></div>
<div style="position:absolute;left:330px;top:160px;width:540px;color:#ece6da">{logo}</div>
</body>"""
f = S.parent / '_ref/og.html'
f.write_text(h, encoding='utf8')
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    g = b.new_page(viewport={'width': 1200, 'height': 630})
    g.goto(f.as_uri()); g.wait_for_timeout(800)
    g.screenshot(path=str(S / 'assets/img/og.jpg'), type='jpeg', quality=86)
    b.close()
