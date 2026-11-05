"""Bordas de papel rasgado em SVG: uma camada de papel e a fibra clara logo atrás, em ladrilho de 1600 px."""
import numpy as np
from pathlib import Path
A=Path(__file__).resolve().parent.parent/'assets/img'
def linha(sem,base,amp):
    r=np.random.default_rng(sem);N=320;x=np.linspace(0,1600,N+1)
    y=np.zeros(N+1)
    for k,a in ((2,1),(5,.55),(11,.3),(29,.16),(71,.1),(143,.06)):
        y+=a*np.sin(2*np.pi*k*x/1600+r.uniform(0,6.28))
    y=y/2.2*amp+base
    y+=r.normal(0,.9,N+1)
    y[-1]=y[0]
    return x,y
for nome,sem in (('rasgo-a',3),('rasgo-b',8)):
    x,y=linha(sem,34,18); x2,y2=linha(sem+1,28,17)
    p=' '.join(f'{a:.0f},{b:.1f}' for a,b in zip(x,y)); q=' '.join(f'{a:.0f},{b:.1f}' for a,b in zip(x2,y2))
    (A/f'{nome}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="72" viewBox="0 0 1600 72" preserveAspectRatio="none"><polygon fill="#fff" points="0,72 {q} 1600,72"/><polygon fill="#ece6da" points="0,72 {p} 1600,72"/></svg>')
