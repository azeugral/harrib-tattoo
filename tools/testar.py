# -*- coding: utf-8 -*-
"""Testa o que o usuário faz de verdade: filtros, lightbox, Quero uma assim, comparador, menu, formulário e o arco fixado.
Uso: python tools/testar.py [url]"""
import sys
from pathlib import Path
from urllib.parse import unquote
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf8')
URL = next((a for a in sys.argv[1:] if a.startswith('http')), 'http://localhost:8877/')
R = []
def ok(n, c, extra=''):
    R.append(bool(c)); print('OK ' if c else 'FALHOU', n, extra)

with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge', args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'])
    c = b.new_context(viewport={'width': 1440, 'height': 900})
    g = c.new_page()
    err = []
    g.on('pageerror', lambda e: err.append(str(e)[:300]))
    g.on('console', lambda m: err.append(m.text[:200]) if m.type == 'error' else None)
    g.goto(URL); g.wait_for_timeout(2500)
    ok('webgl ativo', g.evaluate("!!document.querySelector('#heroCanvas')"))
    n0 = g.evaluate("[...document.querySelectorAll('.card')].filter(c=>!c.hidden).length")
    g.evaluate("document.querySelector('#verMais').scrollIntoView({block:'center',behavior:'instant'})"); g.click('#verMais'); g.wait_for_timeout(200)
    n1 = g.evaluate("[...document.querySelectorAll('.card')].filter(c=>!c.hidden).length")
    ok('ver mais', n1 > n0, f'{n0}->{n1}')
    g.click('.filtros button[data-f=cyber]'); g.wait_for_timeout(150)
    nc = g.evaluate("[...document.querySelectorAll('.card')].filter(c=>!c.hidden).length")
    ok('filtro cyber', 3 < nc < n1, nc)
    g.click('.filtros button[data-f=todos]')
    g.click('.est[data-f=floral]'); g.wait_for_timeout(1000)
    ok('estilo aplica filtro', g.evaluate("document.querySelector('.filtros button[data-f=floral]').getAttribute('aria-pressed')") == 'true')
    g.click('.filtros button[data-f=manga]'); g.wait_for_timeout(200)
    # hover com vídeo
    g.locator('.card[data-id=chrollo]').hover(); g.wait_for_timeout(1800)
    ok('video no hover', g.evaluate("document.querySelector('.card[data-id=chrollo]').classList.contains('tocando')"))
    g.mouse.move(5, 5)
    # lightbox
    g.click('.card[data-id=chrollo]'); g.wait_for_timeout(500)
    ok('lightbox abre', g.evaluate("!document.querySelector('#lb').hidden"))
    ok('lightbox imagem', g.evaluate("(()=>{const i=document.querySelector('#lbM img');return i&&i.complete&&i.naturalWidth>0})()"))
    g.keyboard.press('ArrowRight'); g.wait_for_timeout(300); g.keyboard.press('ArrowRight'); g.wait_for_timeout(600)
    ok('lightbox vídeo', g.evaluate("!!document.querySelector('#lbM video')"))
    g.click('#lbO'); g.wait_for_timeout(1500)
    ok('Quero uma assim', 'Chrollo' in g.input_value('#fIdeia') and g.evaluate("document.querySelector('#lb').hidden"))
    ok('rolou ao orçamento', g.evaluate("Math.abs(document.querySelector('#orcamento').getBoundingClientRect().top)<200"))
    ok('estilo marcado', g.evaluate("document.querySelector('#fEstilo button[aria-pressed=true]').textContent") == 'Mangá e anime')
    # form
    ok('erro sem nome', (g.click('#fWhats'), g.wait_for_timeout(150), g.evaluate("!document.querySelector('#fErro').hidden"))[2])
    g.fill('#fNome', 'Teste'); g.fill('#fTam', '15 cm'); g.select_option('#fLocal', 'Coxa')
    with c.expect_page() as pop:
        g.click('#fWhats')
    u = unquote(pop.value.url); pop.value.close()
    ok('whatsapp', ('5541997875360' in u or 'phone=5541997875360' in u) and 'Coxa' in u and 'Chrollo' in u, u[:120])
    # comparador
    g.evaluate("document.querySelector('#comp').scrollIntoView({block:'center',behavior:'instant'})"); g.wait_for_timeout(400)
    bx = g.locator('#comp').bounding_box()
    g.mouse.move(bx['x'] + bx['width'] * .5, bx['y'] + 100); g.mouse.down(); g.mouse.move(bx['x'] + bx['width'] * .8, bx['y'] + 100, steps=4); g.mouse.up(); g.wait_for_timeout(100)
    p_ = g.evaluate("document.querySelector('#comp').style.getPropertyValue('--p')")
    ok('comparador arrasta', p_.startswith('7') or p_.startswith('8'), p_)
    g.click('.escolhe button[data-n=besouro]'); g.wait_for_timeout(500)
    ok('comparador troca', 'besouro' in g.evaluate("document.querySelector('#compTraco').src"))
    # arco fixado
    t = g.evaluate("(()=>{const a=document.querySelector('#evolucao');return {cls:a.className,top:a.offsetTop,h:a.offsetHeight}})()")
    ok('arco fixado', 'fixo' in t['cls'] and t['h'] > 1500, t)
    g.evaluate(f"window.scrollTo({{top:{t['top'] + (t['h'] - 900) * .5},behavior:'instant'}})"); g.wait_for_timeout(400)
    tr = g.evaluate("getComputedStyle(document.querySelector('#pista')).transform")
    ok('arco anda', tr != 'none', tr)
    g.evaluate(f"window.scrollTo({{top:{t['top'] + t['h'] - 905},behavior:'instant'}})"); g.wait_for_timeout(300)
    # último painel (primeiro do DOM é o mais à direita) e o de outubro dentro da tela no fim
    fim = g.evaluate("(()=>{const k=[...document.querySelectorAll('.koma')].at(-1).getBoundingClientRect();return [k.left,k.right,innerWidth]})()")
    ok('arco termina no último painel', fim[0] >= 0 and fim[1] <= fim[2], fim)
    ok('sem erros de console', not err, err[:3])
    c.close()

    # toque
    c = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True, device_scale_factor=2)
    g = c.new_page(); err = []
    g.on('pageerror', lambda e: err.append(str(e)[:300]))
    g.goto(URL); g.wait_for_timeout(2500)
    ok('celular usa vídeo', g.evaluate("!!document.querySelector('.hero video') && !document.querySelector('#heroCanvas')"))
    ok('vídeo tocando', g.evaluate("(()=>{const v=document.querySelector('.hero video');return v.readyState>=2})()"))
    g.tap('#abrirMenu'); g.wait_for_timeout(300)
    ok('menu abre', g.evaluate("!document.querySelector('#gaveta').hidden"))
    g.tap('#gaveta a[href="#onde"]'); g.wait_for_timeout(1500)
    ok('menu fecha e leva', g.evaluate("document.querySelector('#gaveta').hidden && Math.abs(document.querySelector('#onde').getBoundingClientRect().top)<120"))
    ok('sem rolagem presa', g.evaluate("document.body.style.overflow===''"))
    ok('sem erros mobile', not err, err[:3])
    c.close()
    b.close()
print('RESULTADO', sum(R), '/', len(R))
