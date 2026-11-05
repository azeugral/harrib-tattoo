(function () {
  'use strict';
  var D = window.HARRIB, $ = function (s, r) { return (r || document).querySelector(s); }, $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var calmo = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var toque = matchMedia('(hover: none), (pointer: coarse)').matches;

  /* ---------- hero ---------- */
  (function () {
    var hero = $('#inicio'), canvas = $('#heroCanvas'), poster = $('#heroPoster');
    /* em pé há duas páginas: a alta e, com a barra do navegador comendo a altura, a curta */
    function curto() { return innerWidth / innerHeight < 1.05 && innerHeight <= 760; }
    var formato = innerWidth / innerHeight >= 1.05 ? 'deitado' : curto() ? 'curto' : 'pe';
    hero.classList.toggle('curto', curto());
    /* o logo só entra depois de decodificado e com a animação já rodando, para nada disputar o primeiro quadro */
    var entrou = false;
    function entra() {
      if (entrou) return;
      entrou = true;
      var i = $('#heroLogo'), vai = function () { requestAnimationFrame(function () { hero.classList.add('entrou'); }); };
      (i.decode ? i.decode() : Promise.resolve()).then(vai, vai);
    }
    setTimeout(entra, 1800);
    poster.style.backgroundImage = 'url(assets/img/hero-' + formato + '.jpg?v=64)';
    if (calmo) { canvas.remove(); entra(); return; }
    if (toque) {
      canvas.remove();
      var v = document.createElement('video');
      v.muted = true; v.loop = true; v.playsInline = true; v.autoplay = true; v.setAttribute('playsinline', ''); v.setAttribute('aria-hidden', 'true');
      v.poster = 'assets/img/hero-' + formato + '.jpg?v=64';
      v.src = 'assets/video/hero-' + formato + '.mp4?v=64';
      poster.style.backgroundSize = 'contain';
      v.addEventListener('playing', entra);
      poster.after(v);
      v.play().catch(function () {});
      return;
    }
    var T;
    try { T = window.heroGL(canvas, []); } catch (e) { T = null; }
    if (!T) { canvas.remove(); return; }
    var L = 'ecd', prontas = 0, tempo = 0, vis = true, ultimo = 0, pedido = 0, escala = 1, soma = 0, conta = 0;
    function mede() {
      hero.classList.toggle('curto', curto());
      var d = Math.min(devicePixelRatio || 1, 2) * escala, w = Math.round(canvas.clientWidth * d), h = Math.round(canvas.clientHeight * d);
      /* limite de GPU: 4 MP bastam para o painel continuar nítido */
      var k = Math.min(1, Math.sqrt(4e6 / (w * h)));
      canvas.width = Math.round(w * k); canvas.height = Math.round(h * k);
    }
    function quadro(t) {
      pedido = requestAnimationFrame(quadro);
      if (!vis || document.hidden) { ultimo = 0; return; }
      /* tempo real: anda na frequência da tela, sem trava de quadros */
      var dt = ultimo ? Math.min(t - ultimo, 50) : 0;
      ultimo = t; tempo += dt;
      /* se a placa não der conta, baixa a resolução e mantém a fluidez */
      if (dt) { soma += dt; conta++; }
      if (conta === 45) {
        if (soma / conta > 24 && escala > .5) { escala = Math.max(.5, escala - .15); mede(); }
        soma = conta = 0;
      }
      var x = Math.min(1, tempo / 1600), intro = 1 - Math.pow(1 - x, 3);
      T.desenhar((Math.max(0, tempo - 1600) / 1000 * 12) % 180, x < 1 ? intro : undefined);
    }
    function sobe(p, a, depois) {
      var i = new Image(); i.decoding = 'async';
      i.onload = function () { T.carrega(p, a, i); depois && depois(); };
      i.src = 'assets/img/hero/' + L[p] + a + '.webp';
    }
    mede();
    addEventListener('resize', mede);
    new IntersectionObserver(function (e) { vis = e[0].isIntersecting; }).observe(hero);
    [0, 1, 2].forEach(function (p) {
      sobe(p, 0, function () {
        prontas++;
        if (prontas === 3) {
          pedido = requestAnimationFrame(quadro);
          setTimeout(entra, 700);
          for (var q = 0; q < 3; q++) { sobe(q, 1); sobe(q, 2); }
        }
      });
    });
  })();

  /* ---------- topo e menu ---------- */
  var topo = $('#topo'), gav = $('#gaveta');
  function rolou() { topo.classList.toggle('cheio', scrollY > innerHeight * .7); }
  addEventListener('scroll', rolou, { passive: true }); rolou();
  function menu(a) { gav.hidden = !a; document.body.style.overflow = a ? 'hidden' : ''; $('#abrirMenu').setAttribute('aria-expanded', a); }
  $('#abrirMenu').onclick = function () { menu(true); };
  $('#fecharMenu').onclick = function () { menu(false); };
  $$('#gaveta a').forEach(function (a) { a.addEventListener('click', function () { menu(false); }); });

  /* ---------- entradas ---------- */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('visto'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  $$('[data-rv]').forEach(function (e) { io.observe(e); });

  /* ---------- trabalhos ---------- */
  var cards = $$('.card'), filtro = 'todos', tudo = false;
  var LIM = function () { return innerWidth <= 860 ? 8 : 12; };
  function aplica() {
    var n = 0, lim = LIM(), total = 0;
    cards.forEach(function (c) {
      var ok = filtro === 'todos' || c.dataset.cat.split(' ').indexOf(filtro) > -1;
      if (ok) total++;
      var mostra = ok && (tudo || filtro !== 'todos' || n < lim);
      c.hidden = !mostra;
      if (mostra) n++;
    });
    $('#verMais').parentNode.hidden = tudo || filtro !== 'todos' || total <= lim;
    $$('.filtros button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.f === filtro); });
  }
  function setFiltro(f) { filtro = f; aplica(); }
  $$('.filtros button').forEach(function (b) { b.onclick = function () { setFiltro(b.dataset.f); }; });
  $('#verMais').onclick = function () { tudo = true; aplica(); };
  $$('.est').forEach(function (b) {
    b.onclick = function () { setFiltro(b.dataset.f); $('#ancoraGrade').scrollIntoView({ behavior: calmo ? 'auto' : 'smooth', block: 'start' }); };
  });
  aplica();

  /* vídeo no hover (só no computador) */
  if (!toque) $$('.card[data-v]').forEach(function (c) {
    var v;
    c.addEventListener('mouseenter', function () {
      if (!v) { v = document.createElement('video'); v.muted = true; v.loop = true; v.playsInline = true; v.preload = 'auto'; v.src = 'assets/video/' + c.dataset.v + '.mp4'; $('.ft', c).appendChild(v); }
      var p = v.play(); if (p) p.then(function () { if (c.matches(':hover')) c.classList.add('tocando'); else v.pause(); }).catch(function () {});
    });
    c.addEventListener('mouseleave', function () { c.classList.remove('tocando'); if (v) v.pause(); });
  });

  /* ---------- lightbox ---------- */
  var lb = $('#lb'), lbM = $('#lbM'), atual = null, ind = 0, voltar = null;
  function pinta() {
    var m = atual.m[ind];
    lbM.textContent = '';
    var el;
    if (m.v) { el = document.createElement('video'); el.src = 'assets/video/' + m.a + '.mp4'; el.poster = 'assets/video/' + m.a + '.webp'; el.muted = true; el.loop = true; el.controls = true; el.playsInline = true; el.autoplay = true; }
    else { el = document.createElement('img'); el.src = 'assets/img/g/' + m.a + '.webp'; el.alt = atual.t + ', ' + atual.n; el.draggable = false; }
    lbM.appendChild(el);
    if (atual.m.length > 1) {
      [['a', '←', -1], ['b', '→', 1]].forEach(function (s) {
        var b = document.createElement('button'); b.className = 'lb-seta ' + s[0]; b.textContent = s[1]; b.setAttribute('aria-label', s[2] < 0 ? 'Anterior' : 'Próxima');
        b.onclick = function () { ind = (ind + s[2] + atual.m.length) % atual.m.length; pinta(); }; lbM.appendChild(b);
      });
      $('#lbC').textContent = (ind + 1) + ' de ' + atual.m.length;
    } else $('#lbC').textContent = '';
  }
  function abre(id, el) {
    atual = D.t[id]; ind = 0; voltar = el;
    $('#lbT').textContent = atual.t; $('#lbN').textContent = atual.n; $('#lbQ').textContent = atual.q;
    pinta(); lb.hidden = false; document.body.style.overflow = 'hidden'; $('#lbX').focus();
  }
  function fecha() { lb.hidden = true; lbM.textContent = ''; document.body.style.overflow = ''; if (voltar) voltar.focus(); }
  cards.forEach(function (c) { c.onclick = function () { abre(c.dataset.id, c); }; });
  $('#lbX').onclick = fecha;
  lb.addEventListener('click', function (e) { if (e.target === lb || e.target === lbM) fecha(); });
  addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { if (!lb.hidden) fecha(); if (!gav.hidden) menu(false); }
    if (lb.hidden || !atual || atual.m.length < 2) return;
    if (e.key === 'ArrowRight') { ind = (ind + 1) % atual.m.length; pinta(); }
    if (e.key === 'ArrowLeft') { ind = (ind - 1 + atual.m.length) % atual.m.length; pinta(); }
  });
  $('#lbO').onclick = function () {
    var a = atual; fecha();
    $('#fIdeia').value = 'Vi o trabalho "' + a.t + '" no site e quero algo nessa linha: ';
    var est = { manga: 'Mangá e anime', cyber: 'Cybertribal', floral: 'Floral e traço fino', black: 'Blackwork', cor: 'Com cor' }[a.c];
    $$('#fEstilo button').forEach(function (b) { b.setAttribute('aria-pressed', b.textContent === est); });
  };

  /* ---------- comparador ---------- */
  var comp = $('#comp'), cR = $('#compR');
  cR.addEventListener('input', function () { comp.style.setProperty('--p', cR.value + '%'); });
  function compMove(e) {
    var r = comp.getBoundingClientRect(), v = Math.max(0, Math.min(100, (e.clientX - r.left) / r.width * 100));
    comp.style.setProperty('--p', v + '%'); cR.value = v;
  }
  var arr = false, sx = 0, sy = 0;
  comp.addEventListener('pointerdown', function (e) { arr = true; sx = e.clientX; sy = e.clientY; if (e.pointerType === 'mouse') { compMove(e); } try { comp.setPointerCapture(e.pointerId); } catch (x) {} });
  comp.addEventListener('pointermove', function (e) { if (arr) compMove(e); });
  ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(function (n) { comp.addEventListener(n, function () { arr = false; }); });
  $$('.escolhe button').forEach(function (b) {
    b.onclick = function () {
      $$('.escolhe button').forEach(function (o) { o.setAttribute('aria-pressed', o === b); });
      $('#compTraco').src = 'assets/img/tinta/' + b.dataset.n + '-traco.webp';
      $('#compPele').src = 'assets/img/tinta/' + b.dataset.n + '-pele.webp';
      cR.value = 50; comp.style.setProperty('--p', '50%');
    };
  });

  /* ---------- arco: a pista corre para a direita, como virar páginas de mangá ---------- */
  (function () {
    var arco = $('#evolucao'), pista = $('#pista'), max = 0, ativo = false;
    function pode() { return innerWidth >= 1000 && innerHeight >= 640 && !calmo; }
    function mede() {
      ativo = pode();
      arco.classList.toggle('fixo', ativo);
      if (!ativo) { arco.style.height = ''; pista.style.transform = ''; return; }
      pista.style.transform = '';
      max = Math.max(0, pista.scrollWidth - innerWidth);
      arco.style.height = (innerHeight + max * 1.15) + 'px';
      rola();
    }
    function rola() {
      if (!ativo) return;
      var r = arco.getBoundingClientRect(), t = arco.offsetHeight - innerHeight;
      var p = Math.max(0, Math.min(1, -r.top / t));
      pista.style.transform = 'translate3d(' + (p * max).toFixed(1) + 'px,0,0)';
    }
    var fila = false;
    addEventListener('scroll', function () { if (fila) return; fila = true; requestAnimationFrame(function () { fila = false; rola(); }); }, { passive: true });
    addEventListener('resize', mede);
    addEventListener('load', mede);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(mede);
    mede();
  })();

  /* ---------- reels tocam só quando aparecem ---------- */
  var rv = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      var v = e.target;
      if (e.isIntersecting) { if (!v.src) v.src = v.dataset.src; if (!calmo) v.play().catch(function () {}); } else v.pause();
    });
  }, { threshold: .25 });
  $$('.reel video').forEach(function (v) { rv.observe(v); });

  /* ---------- orçamento ---------- */
  $$('#fEstilo button').forEach(function (b) {
    b.onclick = function () { var on = b.getAttribute('aria-pressed') === 'true'; b.setAttribute('aria-pressed', !on); };
  });
  function mensagem() {
    var nome = $('#fNome').value.trim(), ideia = $('#fIdeia').value.trim();
    var err = $('#fErro');
    if (!nome || !ideia) {
      err.textContent = !nome ? 'Escreva seu nome.' : 'Conte sua ideia.';
      err.hidden = false; (!nome ? $('#fNome') : $('#fIdeia')).focus(); return null;
    }
    err.hidden = true;
    var est = $$('#fEstilo button[aria-pressed=true]').map(function (b) { return b.textContent; }).join(', ');
    var l = ['Oi, Alisson! Vim pelo site e quero um orçamento.', '', 'Nome: ' + nome, 'Ideia: ' + ideia];
    if (est) l.push('Estilo: ' + est);
    if ($('#fLocal').value) l.push('Lugar do corpo: ' + $('#fLocal').value);
    if ($('#fTam').value.trim()) l.push('Tamanho: ' + $('#fTam').value.trim());
    if ($('#fPrim').value) l.push('Primeira tatuagem: ' + $('#fPrim').value);
    return l.join('\n');
  }
  $('#form').addEventListener('submit', function (e) {
    e.preventDefault();
    var m = mensagem(); if (!m) return;
    window.open('https://wa.me/' + D.whats + '?text=' + encodeURIComponent(m), '_blank', 'noopener');
  });
  $('#fDirect').onclick = function () {
    var m = mensagem(); if (!m) return;
    var b = this;
    var abrir = function () { b.textContent = 'Mensagem copiada'; window.open('https://ig.me/m/harribtattoo_', '_blank', 'noopener'); setTimeout(function () { b.textContent = 'Copiar e abrir o Direct'; }, 3000); };
    if (navigator.clipboard) navigator.clipboard.writeText(m).then(abrir, abrir); else abrir();
  };
})();
