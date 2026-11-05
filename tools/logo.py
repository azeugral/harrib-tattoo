"""Vetoriza o logo HARRIB do post 005: isola o osso do fundo, amplia e traça com potrace."""
import cv2, numpy as np, potrace, os
R=os.path.expanduser('~/Documents/PROJETOS LRGZ/Harrib Tattoo')
im=cv2.imread(R+'/_ref/ig/005_0.jpg')
x0,y0,x1,y1=350,880,892,1160
c=im[y0:y1,x0:x1].astype(np.float32)
sc=6
big=cv2.resize(c,None,fx=sc,fy=sc,interpolation=cv2.INTER_CUBIC)
g=big.min(axis=2)  # min canal: pele (B baixo) cai, osso fica alto
g=cv2.GaussianBlur(g,(0,0),1.6)
m=(g>118).astype(np.uint8)

n,l,s,_=cv2.connectedComponentsWithStats(m,connectivity=8)
keep=np.zeros(n,bool)
for i in range(1,n):
    x,y,w,h,a=s[i]
    if a>6000 or (a>1500 and 120<h and 60<w<260 and y<600): keep[i]=True   # letras + estrela do i, sem TATTOO
m2=keep[l].astype(np.uint8)
print([tuple(s[i]) for i in range(1,n) if keep[i]])
ys,xs=np.where(m2); m2=m2[ys.min():ys.max()+1,xs.min():xs.max()+1]
H,W=m2.shape
bm=potrace.Bitmap(m2==0)
pl=bm.trace(turdsize=30,alphamax=1.0,opttolerance=.4)
d=[]
for c in pl:
    a=c.start_point; d.append(f"M{a.x:.1f} {H-a.y:.1f}" if False else f"M{a.x:.1f} {a.y:.1f}")
    for sg in c.segments:
        if sg.is_corner: d.append(f"L{sg.c.x:.1f} {sg.c.y:.1f}L{sg.end_point.x:.1f} {sg.end_point.y:.1f}")
        else: d.append(f"C{sg.c1.x:.1f} {sg.c1.y:.1f} {sg.c2.x:.1f} {sg.c2.y:.1f} {sg.end_point.x:.1f} {sg.end_point.y:.1f}")
    d.append("Z")
p=''.join(d)
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><path fill="currentColor" fill-rule="evenodd" d="{p}"/></svg>'
open(os.path.dirname(os.path.abspath(__file__))+'/../assets/img/logo.svg','w').write(svg)
print(W,H,len(svg))
import cv2
cv2.imwrite(R+'/_ref/logo-mask.png',m2*255)
