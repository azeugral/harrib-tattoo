"""Recorta só os glifos usados e grava woff2 em assets/fonts."""
import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent; F=R.parent/'_ref/fontes'; O=R/'assets/fonts'; O.mkdir(exist_ok=True)
jp="タトゥーは芸術だ作品画風線成長人物声制作お見積り場所質問ゴドンバキ"
lat="U+0020-007E,U+00A0-00FF,U+2013,U+2014,U+2018,U+2019,U+201C,U+201D,U+2022,U+2026,U+00D7,U+2192,U+2190,U+2197"
for src,dst,extra,var in (('KaiseiTokumin-ExtraBold','kaisei-800',jp,None),('ZenKakuGothicNew-Regular','zen-400',jp,None),('ZenKakuGothicNew-Medium','zen-500',jp,None),('ZenKakuGothicNew-Bold','zen-700',jp,None),('DelaGothicOne-Regular','dela',jp,None),('Cinzel','cinzel',"",None)):
    subprocess.run([sys.executable,'-m','fontTools.subset',str(F/f'{src}.ttf'),f'--unicodes={lat}',f'--text={extra}','--flavor=woff2','--layout-features=*',f'--output-file={O/(dst+".woff2")}'],check=True)
    print(dst,round((O/f'{dst}.woff2').stat().st_size/1024),'KB')
