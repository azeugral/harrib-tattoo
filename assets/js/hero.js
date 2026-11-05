/* Tríptico do topo: três painéis de mangá com as tatuagens reais.
   Roda a 12 quadros por segundo, como animação de anime: as linhas de foco "fervem" e cada troca de arte
   é uma espiral de nanquim que fecha e reabre o painel. O laço fecha em 180 quadros (15 s), o mesmo do MP4. */
(function () {
  var VS = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  var FS = [
    'precision highp float;',
    'uniform vec2 uR;uniform float uF,uSeed,uTopo,uCt,uCb,uOt,uOb,uGut,uIntro;',
    'uniform vec3 uW;',
    'uniform sampler2D uA0,uB0,uA1,uB1,uA2,uB2;',
    'const vec3 OSSO=vec3(.925,.90,.855);const vec3 NEGRO=vec3(.035,.035,.04);',
    'float h1(float x){return fract(sin(x*127.1)*43758.5453);}',
    'float h2(vec2 v){return fract(sin(dot(v,vec2(127.1,311.7)))*43758.5453);}',
    'float n1(float x){float i=floor(x),f=fract(x);f=f*f*(3.-2.*f);return mix(h1(i),h1(i+1.),f);}',
    'float n2(vec2 v){vec2 i=floor(v),f=fract(v);f=f*f*(3.-2.*f);return mix(mix(h2(i),h2(i+vec2(1,0)),f.x),mix(h2(i+vec2(0,1)),h2(i+vec2(1,1)),f.x),f.y);}',
    /* linhas de foco: finas perto do centro, abrem para fora */
    'float foco(vec2 q,float s){float a=atan(q.y,q.x),r=length(q);',
    ' float k=a*60.+s*17.3;float id=floor(k);float f=fract(k);',
    ' float largura=.04+.42*h1(id+s*3.1);float ini=.72+1.0*h1(id*1.7+s);',
    ' float taper=smoothstep(ini,ini+.75,r);',
    ' float l=smoothstep(largura*taper,largura*taper-.05-.02/max(r,.1),abs(f-.5));',
    ' return l*taper*step(.28,h1(id*3.3+s*.7));}',
    /* borda de painel desenhada à mão: tremor de nanquim que muda a cada 3 quadros */
    'float tremor(float y,float s){return (n1(y*9.+s*7.)-.5)*.0052+(n1(y*31.+s*3.)-.5)*.0026;}',
    /* espiral: 0 mostra a arte, 1 cobre tudo de preto */
    'float espiral(vec2 q,float p,float s){float r=length(q);float a=atan(q.y,q.x)/6.28318;',
    ' float t=a*2.+log(r+.018)*1.55+p*1.4;t+=(n2(q*6.+s)-.5)*.05;',
    ' float b=abs(fract(t)-.5)*2.;',
    ' float frente=smoothstep(0.,.08,p*2.15-r*.82);',
    ' return smoothstep(-.03,.03,p*1.25-b)*frente+smoothstep(.85,1.,p);}',
    'vec3 painel(sampler2D A,sampler2D B,vec2 c,vec2 m,vec2 uv,float w,float s,float vaiA){',
    ' vec2 q=(uv-c)/m.y;',
    ' float bAsp=m.x/m.y;float tAsp=.74;',
    ' vec2 cv=vec2(q.x/bAsp*(bAsp<tAsp?bAsp/tAsp:1.),q.y*(bAsp<tAsp?1.:tAsp/bAsp))*.88+vec2(0.,-.115);',
    ' vec2 t=vec2(cv.x*.5+.5,.5-cv.y*.5);',
    ' vec3 ca=texture2D(A,t).rgb;vec3 cb=texture2D(B,t).rgb;',
    ' float cob;vec3 c0;',
    ' if(w<.5){cob=espiral(q,w*2.,s);c0=ca;}else{cob=espiral(q,(1.-w)*2.,s+5.);c0=cb;}',
    ' return mix(c0,NEGRO,clamp(cob,0.,1.));}',
    'void main(){',
    ' vec2 uv=(gl_FragCoord.xy*2.-uR)/uR.y;float A=uR.x/uR.y;float s=uSeed;',
    ' vec2 q=uv-vec2(0.,.1);',
    ' float f=foco(q*vec2(1.,1.15),s);',
    ' vec3 cor=NEGRO+(OSSO-NEGRO)*f*.62;',
    /* geometria: gabaritos simétricos, inclinados como requadros */
    ' float tt=clamp((uTopo-uv.y)/(uTopo+1.),0.,1.);',
    ' float ci=mix(uCt,uCb,tt);float oe=mix(uOt,uOb,tt);',
    ' float dx=abs(uv.x);float tr=tremor(uv.y,s);',
    ' float topo=uTopo-(dx/uOt)*.055+(n1(uv.x*7.+s*5.)-.5)*.006;',
    ' float g=uGut;float px=2./uR.y;',
    ' float dCen=ci-g*.5-dx+tr;',
    ' float dLado=min(dx-(ci+g*.5)+tr,oe-dx+tr);',
    ' float dT=topo-uv.y;',
    ' float mCen=smoothstep(0.,px,min(dCen,dT));',
    ' float mLado=smoothstep(0.,px,min(dLado,dT));',
    ' float yc=(uTopo-1.)*.5;float my=(uTopo+1.)*.5;',
    ' vec3 pC=painel(uA1,uB1,vec2(0.,yc),vec2((uCt+uCb)*.5-g*.5,my),uv,uW.y,s,0.);',
    ' float lc=(uCt+uOt+uCb+uOb)*.25;float lw=(uOt+uOb-uCt-uCb)*.25-g*.25;',
    ' vec3 pL;if(uv.x<0.){pL=painel(uA0,uB0,vec2(-lc,yc),vec2(lw,my),uv,uW.x,s+2.,0.);}else{pL=painel(uA2,uB2,vec2(lc,yc),vec2(lw,my),uv,uW.z,s+4.,0.);}',
    ' vec3 dentro=mCen>.5?pC:pL;float m=max(mCen,mLado);',
    /* linhas de foco viram nanquim por cima da arte, só nas bordas externas */
    ' float fi=f*smoothstep(1.05,1.75,length(q));dentro=mix(dentro,NEGRO,fi*.92);',
    ' cor=mix(cor,dentro,m);',
    /* fio de osso em volta de cada painel */
    ' float bC=1.-smoothstep(px*.9,px*2.,abs(min(dCen,dT)));',
    ' float bL=1.-smoothstep(px*.9,px*2.,abs(min(dLado,dT)));',
    ' cor=mix(cor,OSSO,max(bC,bL)*.92);',
    /* base some no preto para o logo respirar */
    ' float fade=smoothstep(-.98,-.3,uv.y);cor=mix(NEGRO,cor,fade);',
    /* sombra elíptica atrás do logo: a arte continua viva nas pontas e o nome fica limpo */
    ' vec2 lq=(uv-vec2(0.,-.42))/vec2(min(1.25,A*1.05),.40);float som=1.-smoothstep(.35,1.25,length(lq));cor=mix(cor,NEGRO,som*.9);',
    ' float teto=smoothstep(.72,.98,uv.y)*(1.-m*0.);cor=mix(cor,NEGRO,teto*.72);',
    ' gl_FragColor=vec4(cor,1.);}'
  ].join('\n');

  function compila(gl, tipo, src) {
    var s = gl.createShader(tipo); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }

  /* geometria em função da proporção da tela */
  function medidas(A) {
    if (A >= 1.05) {
      var k = Math.min(A / 1.6, 1.22);
      var ot = 1.40 * k;
      return { topo: A > 1.3 ? .80 : .84, ct: .50 * k, cb: .44 * k, ot: ot, ob: ot * .93, gut: .026 };
    }
    return { topo: .80, ct: A * .68, cb: A * .60, ot: A * 1.06, ob: A * .99, gut: .022 };
  }

  window.heroGL = function (canvas, urls, op) {
    op = op || {};
    var gl = canvas.getContext('webgl', { antialias: false, alpha: false, preserveDrawingBuffer: !!op.preserveDrawingBuffer, powerPreference: 'low-power' });
    if (!gl) return null;
    var pr = gl.createProgram();
    gl.attachShader(pr, compila(gl, gl.VERTEX_SHADER, VS));
    gl.attachShader(pr, compila(gl, gl.FRAGMENT_SHADER, FS));
    gl.linkProgram(pr); gl.useProgram(pr);
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var lp = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(lp); gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);
    var U = {}; ['uR', 'uF', 'uSeed', 'uTopo', 'uCt', 'uCb', 'uOt', 'uOb', 'uGut', 'uW', 'uA0', 'uB0', 'uA1', 'uB1', 'uA2', 'uB2'].forEach(function (n) { U[n] = gl.getUniformLocation(pr, n); });
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

    /* f = quadro inteiro de 0 a 179; intro = 0..1 abre os painéis na chegada */
    function desenhar(f, intro) {
      gl.viewport(0, 0, canvas.width, canvas.height);
      var A = canvas.width / canvas.height, m = medidas(A);
      gl.uniform2f(U.uR, canvas.width, canvas.height);
      gl.uniform1f(U.uTopo, m.topo); gl.uniform1f(U.uCt, m.ct); gl.uniform1f(U.uCb, m.cb); gl.uniform1f(U.uOt, m.ot); gl.uniform1f(U.uOb, m.ob); gl.uniform1f(U.uGut, m.gut);
      gl.uniform1f(U.uSeed, Math.floor(f / 3) % 12);
      var c = Math.floor(f / 60) % 3, l = f % 60;
      var w = [0, 1, 2].map(function (i) { var ini = 30 + i * 5; return Math.max(0, Math.min(1, (l - ini) / 18)); });
      /* ordem de entrada: centro, depois as laterais */
      if (intro !== undefined && intro < 1) {
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
