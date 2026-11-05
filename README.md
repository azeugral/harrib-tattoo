# Harrib Tattoo

Prévia do site do Alisson (Harrib), tatuador de Curitiba: mangá, anime, cybertribal, floral e blackwork.
O site é um tomo de mangá: tríptico em WebGL que acompanha a frequência da tela (MP4 a 60 fps no toque), tinta da pele extraída em traço, arco de evolução lido da direita para a esquerda e orçamento que sai pronto para o WhatsApp ou o Direct.

No ar: https://azeugral.github.io/harrib-tattoo/ (com `noindex` enquanto for prévia).

## CONFIRMAR com o cliente

- [ ] Endereço: a ficha da Black Blood diz Rua Duque de Caxias, 306, casa 03, São Francisco. A bio dele diz "Curitiba, Centro". Qual vale?
- [ ] Ele é residente da Black Blood ou atende como convidado?
- [ ] WhatsApp (41) 99787-5360 é o canal certo para orçamento?
- [ ] Arco de evolução: os meses vêm das legendas de 2026. Conferir a ordem e se quer mostrar todos.
- [ ] FAQ "primeira tatuagem": diz que já teve cliente que escolheu ele para a primeira. Conferir.
- [ ] Falas de clientes: são comentários reais do Instagram, com o @. Pedir autorização, e ver se o "pra caralho" e o "KRLLLL" ficam.
- [ ] Nome real: "Alisson" aparece no site. Tudo bem?
- [ ] Faixa de preços, horários, sinal e política de remarcação: nada disso foi publicado.
- [ ] Quais trabalhos entram e quais saem. A kitsune do post 004 ficou de fora por ser de outro tatuador.
- [ ] Nome do personagem da peça "Anime em traço vermelho".
- [ ] Dados técnicos que queira citar (agulhas, tintas, biossegurança).
- [ ] Fotos com autorização dos clientes.

## Antes de publicar de verdade

Tirar `noindex` do `tools/modelo.html` e o `Disallow` do `robots.txt`, trocar as URLs de `og:` pelo domínio e adicionar `sitemap.xml`.

## Como mexer

Editar `tools/dados.py` (trabalhos, arco, falas) ou `tools/modelo.html`, depois:

```bash
python tools/montar.py
```

Se mudar o shader em `assets/js/hero.js`, regravar os vídeos com `python tools/gerar_video.py`.
Conferência: `python tools/auditar.py [url]` e `python tools/testar.py [url]`.
Os demais scripts (`processar.py`, `tinta.py`, `logo.py`, `fontes.py`) leem o material bruto em `../_ref`, que fica fora do repo.
