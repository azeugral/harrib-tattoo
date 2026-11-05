# -*- coding: utf-8 -*-
"""Grava o tríptico do hero quadro a quadro: três MP4 (página alta, página curta e tríptico deitado) e os pôsteres. Laço de 15 s a 60 fps = 900 quadros.
Uso: python tools/gerar_video.py [pe curto deitado]"""
import base64, subprocess, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

SITE = Path(__file__).resolve().parent.parent
ffmpeg = shutil.which('ffmpeg')
import sys
FPS = 60
FORMATOS = [f for f in [('pe', 1020, 1500), ('curto', 1020, 1276), ('deitado', 1440, 900)] if len(sys.argv) < 2 or f[0] in sys.argv[1:]]

with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    g = b.new_page(viewport={'width': 500, 'height': 500})
    g.set_content('<body style="margin:0"><canvas id=c></canvas></body>')
    g.add_script_tag(content=(SITE / 'assets/js/hero.js').read_text(encoding='utf8'))
    imgs = {}
    for lado in 'ecd':
        for i in range(3):
            imgs[f'{lado}{i}'] = 'data:image/webp;base64,' + base64.b64encode((SITE / f'assets/img/hero/{lado}{i}.webp').read_bytes()).decode()
    g.evaluate("""async (imgs)=>{const c=document.getElementById('c');c.width=800;c.height=800;window.T=heroGL(c,[],{preserveDrawingBuffer:true});
      const L='ecd';for(let p=0;p<3;p++)for(let a=0;a<3;a++){const i=new Image();i.src=imgs[L[p]+a];await i.decode();T.carrega(p,a,i)}}""", imgs)
    for nome, W, H in FORMATOS:
        mp4 = SITE / f'assets/video/hero-{nome}.mp4'
        enc = subprocess.Popen([ffmpeg, '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                                '-c:v', 'libx264', '-preset', 'slow', '-crf', '23', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', str(FPS), '-movflags', '+faststart', '-an', str(mp4)], stdin=subprocess.PIPE)
        g.evaluate(f"(()=>{{const c=document.getElementById('c');c.width={W};c.height={H}}})()")
        for f in range(15 * FPS):
            d = g.evaluate(f"(T.desenhar({f * 12 / FPS}),document.getElementById('c').toDataURL('image/jpeg',.96))")
            raw = base64.b64decode(d.split(',', 1)[1])
            enc.stdin.write(raw)
            if f == FPS:
                (SITE / f'assets/img/hero-{nome}.jpg').write_bytes(base64.b64decode(g.evaluate("document.getElementById('c').toDataURL('image/jpeg',.84)").split(',', 1)[1]))
            if f % 120 == 0:
                print(nome, f, flush=True)
        enc.stdin.close(); enc.wait()
        print(mp4.name, round(mp4.stat().st_size / 1e6, 2), 'MB', flush=True)
    b.close()
