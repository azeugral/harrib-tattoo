/* Tríptico do topo: três painéis de mangá com as tatuagens reais.
   O tempo é contínuo e acompanha a tela (60, 120, 144 Hz): sobre o fundo preto, a arte aproxima devagar
   e cada troca é uma espiral de nanquim. O que oscila anda num círculo de ruído, então o laço de 15 s fecha
   sem emenda, o mesmo do MP4. A unidade de f segue 1/12 s: f vai de 0 a 180. */
(function () {
  var VS = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  var FS = [
    'precision highp float;',
    'uniform vec2 uR,uL,uZ;uniform float uPag,uTopo,uCt,uCb,uOt,uOb,uGut;',
    'uniform vec3 uW;',
    'uniform sampler2D uA0,uB0,uA1,uB1,uA2,uB2;',
    'const vec3 OSSO=vec3(.925,.90,.855);const vec3 NEGRO=vec3(0.);',
    'float h2(vec2 v){return fract(sin(dot(v,vec2(127.1,311.7)))*43758.5453);}',
    'float n2(vec2 v){vec2 i=floor(v),f=fract(v);f=f*f*(3.-2.*f);return mix(mix(h2(i),h2(i+vec2(1,0)),f.x),mix(h2(i+vec2(0,1)),h2(i+vec2(1,1)),f.x),f.y);}',
    /* borda de painel desenhada à mão: o tremor de nanquim ondula devagar */
    'float tremor(float y){return (n2(vec2(y*9.,1.)+uL*.45)-.5)*.0052+(n2(vec2(y*31.,7.)+uL*.7)-.5)*.0026;}',
    /* espiral: 0 mostra a arte, 1 cobre tudo de preto */
    'float espiral(vec2 q,float p,float s){float r=length(q);float a=atan(q.y,q.x)/6.28318;',
    ' float t=a*2.+log(r+.018)*1.55+p*1.4;t+=(n2(q*6.+s)-.5)*.05;',
    ' float b=abs(fract(t)-.5)*2.;',
    ' float frente=smoothstep(0.,.08,p*2.15-r*.82);',
    ' return smoothstep(-.03,.03,p*1.25-b)*frente+smoothstep(.85,1.,p);}',
    'vec3 painel(sampler2D A,sampler2D B,vec2 c,vec2 m,vec2 uv,float w,float s){',
    ' vec2 q=(uv-c)/m.y;',
    ' float bAsp=m.x/m.y;float tAsp=.74;',
    ' vec2 cv=vec2(q.x/bAsp*(bAsp<tAsp?bAsp/tAsp:1.),q.y*(bAsp<tAsp?1.:tAsp/bAsp))*(uPag>.5?.98:.88);',
    ' float oy=uPag>.5?(c.y>0.?.2:.03):-.115;vec2 ta=cv*uZ.x+vec2(0.,oy),tb=cv*uZ.y+vec2(0.,oy);',
    ' vec3 ca=texture2D(A,vec2(ta.x*.5+.5,.5-ta.y*.5)).rgb;vec3 cb=texture2D(B,vec2(tb.x*.5+.5,.5-tb.y*.5)).rgb;',
    ' float cob;vec3 c0;',
    ' if(w<.5){cob=espiral(q,w*2.,s);c0=ca;}else{cob=espiral(q,(1.-w)*2.,s+5.);c0=cb;}',
    ' return mix(c0,NEGRO,clamp(cob,0.,1.));}',
    'void main(){',
    ' vec2 uv=(gl_FragCoord.xy*2.-uR)/uR.y;float A=uR.x/uR.y;',
    ' vec3 cor=NEGRO;',
    /* tríptico (deitado) ou página de mangá (em pé): quadro grande em cima, dois embaixo, os três inteiros */
    ' float dx=abs(uv.x);float tr=tremor(uv.y);float g=uGut;float px=2./uR.y;',
    ' float dCen,dLado,dT;vec2 cC,mC,cL,mL;',
    ' if(uPag<.5){',
    '  float tt=clamp((uTopo-uv.y)/(uTopo+1.),0.,1.);',
    '  float ci=mix(uCt,uCb,tt);float oe=mix(uOt,uOb,tt);',
    '  float topo=uTopo-(dx/uOt)*.055+(n2(vec2(uv.x*7.,4.)+uL*.45)-.5)*.006;',
    '  dCen=ci-g*.5-dx+tr;dLado=min(dx-(ci+g*.5)+tr,oe-dx+tr);dT=topo-uv.y;',
    '  float yc=(uTopo-1.)*.5;float my=(uTopo+1.)*.5;',
    '  cC=vec2(0.,yc);mC=vec2((uCt+uCb)*.5-g*.5,my);',
    '  cL=vec2((uCt+uOt+uCb+uOb)*.25,yc);mL=vec2((uOt+uOb-uCt-uCb)*.25-g*.25,my);',
    ' }else{',
    '  float borda=uOt;float base=-.965+(dx/borda)*.022;',
    '  float topo=.965-(dx/borda)*.022+(n2(vec2(uv.x*7.,4.)+uL*.45)-.5)*.004;',
    '  float corte=uCt-(dx/borda)*.05;',
    '  dT=topo-uv.y;',
    '  dCen=min(borda-dx+tr,uv.y-(corte+g*.5)+tr);',
    '  dLado=min(min(borda-dx+tr,dx-g*.5+tr),min(corte-g*.5-uv.y+tr,uv.y-base));',
    '  dLado=min(dLado,dT);',
    '  cC=vec2(0.,(.965+uCt)*.5);mC=vec2(borda,(.965-uCt)*.5);',
    '  cL=vec2(borda*.5,(uCt-.965)*.5);mL=vec2(borda*.5-g*.25,(uCt+.965)*.5);',
    ' }',
    ' float mCen=smoothstep(0.,px,min(dCen,dT));',
    ' float mLado=smoothstep(0.,px,dLado<dT?dLado:dT);',
    ' vec3 pC=painel(uA1,uB1,cC,mC,uv,uW.y,1.);',
    ' vec3 pL;if(uv.x<0.){pL=painel(uA0,uB0,vec2(-cL.x,cL.y),mL,uv,uW.x,3.);}else{pL=painel(uA2,uB2,cL,mL,uv,uW.z,5.);}',
    ' vec3 dentro=mCen>.5?pC:pL;float m=max(mCen,mLado);',
    ' cor=mix(cor,dentro,m);',
    /* fio de osso em volta de cada painel */
    ' float bC=1.-smoothstep(px*.9,px*2.,abs(min(dCen,dT)));',
    ' float bL=1.-smoothstep(px*.9,px*2.,abs(min(dLado,dT)));',
    ' cor=mix(cor,OSSO,max(bC,bL)*.92);',
    /* no tríptico a base some no preto e o logo ganha uma sombra; na página ele fica fora dos quadros */
    ' if(uPag<.5){',
    '  float fade=smoothstep(-.98,-.3,uv.y);cor=mix(NEGRO,cor,fade);',
    '  vec2 lq=(uv-vec2(0.,-.42))/vec2(min(1.25,A*1.05),.40);float som=1.-smoothstep(.35,1.25,length(lq));cor=mix(cor,NEGRO,som*.9);',
    '  float teto=smoothstep(.72,.98,uv.y);cor=mix(cor,NEGRO,teto*.72);',
    ' }',
    ' gl_FragColor=vec4(cor,1.);}'
  ].join('\n');

  function compila(gl, tipo, src) {
    var s = gl.createShader(tipo); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }

  /* geometria em função da proporção: abaixo de 1.05 vira página, com ct = altura do corte entre os quadros */
  function medidas(A) {
    if (A >= 1.05) {
      var k = Math.min(A / 1.6, 1.22);
      var ot = 1.40 * k;
      return { pag: 0, topo: A > 1.3 ? .80 : .84, ct: .50 * k, cb: .44 * k, ot: ot, ob: ot * .93, gut: .026 };
    }
    return { pag: 1, topo: .965, ct: -.31, cb: 0, ot: A * .955, ob: 0, gut: .024 };
  }

  window.heroGL = function (canvas, urls, op) {
    op = op || {};
    var gl = canvas.getContext('webgl', { antialias: false, alpha: false, preserveDrawingBuffer: !!op.preserveDrawingBuffer, powerPreference: 'high-performance' });
    if (!gl) return null;
    var pr = gl.createProgram();
    gl.attachShader(pr, compila(gl, gl.VERTEX_SHADER, VS));
    gl.attachShader(pr, compila(gl, gl.FRAGMENT_SHADER, FS));
    gl.linkProgram(pr); gl.useProgram(pr);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var lp = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(lp); gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);
    var U = {}; ['uR', 'uL', 'uZ', 'uPag', 'uTopo', 'uCt', 'uCb', 'uOt', 'uOb', 'uGut', 'uW', 'uA0', 'uB0', 'uA1', 'uB1', 'uA2', 'uB2'].forEach(function (n) { U[n] = gl.getUniformLocation(pr, n); });
    ['uA0', 'uB0', 'uA1', 'uB1', 'uA2', 'uB2'].forEach(function (n, i) { gl.uniform1i(U[n], i); });

    var tex = [[null, null, null], [null, null, null], [null, null, null]]; /* [painel][arte] */
    function sobe(img) {
      var t = gl.createTexture();
      gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, img);
      return t;
    }
    function carrega(painel, arte, img) { tex[painel][arte] = sobe(img); }

    function suave(x) { x = Math.max(0, Math.min(1, x)); return x * x * x * (x * (6 * x - 15) + 10); }
    /* idade da arte, de 0 (acabou de entrar) a 1 (saindo): só aproxima, nunca volta */
    function zoom(idade) { return 1 - .075 * idade; }

    /* f = tempo contínuo de 0 a 180; intro = 0..1 abre os painéis na chegada */
    function desenhar(f, intro) {
      gl.viewport(0, 0, canvas.width, canvas.height);
      var A = canvas.width / canvas.height, m = medidas(A);
      gl.uniform2f(U.uR, canvas.width, canvas.height);
      gl.uniform1f(U.uPag, m.pag); gl.uniform1f(U.uTopo, m.topo); gl.uniform1f(U.uCt, m.ct); gl.uniform1f(U.uCb, m.cb); gl.uniform1f(U.uOt, m.ot); gl.uniform1f(U.uOb, m.ob); gl.uniform1f(U.uGut, m.gut);
      var ang = f / 180 * Math.PI * 2;
      gl.uniform2f(U.uL, Math.cos(ang) * 2.4, Math.sin(ang) * 2.4);
      var c = Math.floor(f / 60) % 3, l = f % 60;
      gl.uniform2f(U.uZ, zoom((l / 60 + 1) / 2), zoom(l / 120));
      var w = [0, 1, 2].map(function (i) { return suave((l - 28 - i * 5) / 20); });
      /* ordem de entrada: centro, depois as laterais */
      if (intro !== undefined && intro < 1) {
        gl.uniform2f(U.uZ, zoom(.5), zoom(.5));
        w = [intro * 1.4 - .4, intro * 1.2, intro * 1.4 - .4].map(function (v) { return .5 + .5 * Math.max(0, Math.min(1, v)); });
      }
      gl.uniform3f(U.uW, w[0], w[1], w[2]);
      for (var p = 0; p < 3; p++) {
        var a = c, b = (c + 1) % 3;
        if (intro !== undefined && intro < 1) { a = 0; b = 0; }
        var ta = tex[p][a] || tex[p][0], tb = tex[p][b] || tex[p][0];
        gl.activeTexture(gl.TEXTURE0 + p * 2); gl.bindTexture(gl.TEXTURE_2D, ta);
        gl.activeTexture(gl.TEXTURE0 + p * 2 + 1); gl.bindTexture(gl.TEXTURE_2D, tb);
      }
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
    return { desenhar: desenhar, carrega: carrega, gl: gl };
  };
})();
