from PIL import Image, ImageDraw
import re,json,math,random
from pathlib import Path

ROOT=Path('.')
html=(ROOT/'index.html').read_text()
m=re.search(r'const MANIFEST=(\{.*?\});\s*const A=',html,re.S)
if not m: raise SystemExit('MANIFEST not found')
M=json.loads(m.group(1))
W=max(int(v[0]+v[2]+2) for v in M.values()); H=max(int(v[1]+v[3]+2) for v in M.values())
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im,'RGBA'); random.seed(7)
def C(h,a=255):
 h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(a,)
CY=C('#48ffe0'); LI=C('#9cff4c'); BL=C('#3ea7ff'); RD=C('#ff405d'); OR=C('#ff8a32'); DK=C('#101827'); MT=C('#29364b'); WH=C('#eef7ff')
def line(p,c,w=1): d.line(p,fill=c,width=max(1,int(w)),joint='curve')
def poly(p,c,o=None): d.polygon(p,fill=c); o and d.line(p+[p[0]],fill=o,width=1)
def ell(b,c,o=None,w=1): d.ellipse(b,fill=c,outline=o,width=max(1,int(w)))
def glow(cx,cy,r,c):
 for k in (3,2,1): ell((cx-r*k*.5,cy-r*k*.5,cx+r*k*.5,cy+r*k*.5),c[:-1]+(18*k,))
 ell((cx-r*.35,cy-r*.35,cx+r*.35,cy+r*.35),c)
def kael(n,r):
 x,y,w,h=r; cx=x+w*.5; by=y+h*.42; base=y+h*.92; pose=n.split('_',1)[1]; cr='crouch' in pose; ds='dash' in pose
 if 'death' in pose:
  line([(x+w*.12,base-h*.15),(x+w*.82,base-h*.12)],MT,max(2,w*.12)); ell((x+w*.55,y+h*.64,x+w*.78,y+h*.84),WH); return
 if cr: by=y+h*.58
 tr=.32 if ds else .16; poly([(cx-w*.04,by),(cx-w*tr,by+h*.06),(cx-w*(tr+.08),by+h*.13),(cx-w*.04,by+h*.08)],BL[:-1]+(180,))
 sp=.14 if ('run' in pose or 'jump' in pose) else .08
 line([(cx-w*.08,by+h*.24),(cx-w*sp,base)],MT,max(2,w*.12)); line([(cx+w*.08,by+h*.24),(cx+w*sp,base)],MT,max(2,w*.12))
 d.rounded_rectangle((cx-w*.19,by-h*.05,cx+w*.19,by+h*.28),radius=max(2,int(w*.10)),fill=DK,outline=CY,width=max(1,int(w*.05)))
 d.rectangle((cx-w*.05,by+h*.02,cx+w*.07,by+h*.16),fill=CY); ell((cx-w*.12,by-h*.25,cx+w*.13,by-h*.02),C('#d8e5ef'))
 poly([(cx-w*.14,by-h*.2),(cx-w*.03,by-h*.34),(cx+w*.02,by-h*.23),(cx+w*.10,by-h*.34),(cx+w*.15,by-h*.17)],WH)
 d.rectangle((cx-w*.08,by-h*.15,cx+w*.11,by-h*.10),fill=C('#ffb23c'))
 gy=by+h*(.02 if 'shoot' in pose else .07); d.rounded_rectangle((cx+w*.05,gy,cx+w*.43,gy+h*.08),2,fill=MT,outline=CY); d.rectangle((cx+w*.37,gy+h*.02,cx+w*.5,gy+h*.055),fill=CY)
 if 'hurt' in pose: d.rectangle((x,y,x+w,y+h),fill=RD[:-1]+(55,))
 if ds:
  for q in range(3): line([(x+w*.04,by+h*.08+q*2),(cx-w*.16,by+h*.08+q*2)],CY[:-1]+(100,))
def mech(n,r,k):
 x,y,w,h=r; cx=x+w*.5; cy=y+h*.55; s=min(w,h); ac={'grunt':RD,'hound':RD,'flyer':CY,'turret':OR,'shield':CY,'burrow':LI,'kamikaze':OR,'brute':RD,'sniper':C('#a56bff')}[k]
 if k=='hound':
  poly([(x+w*.08,cy),(x+w*.35,y+h*.28),(x+w*.74,y+h*.34),(x+w*.92,cy),(x+w*.68,y+h*.68),(x+w*.22,y+h*.68)],DK,ac)
  for px in (.25,.68): line([(x+w*px,y+h*.62),(x+w*(px-.12),y+h*.88)],MT,max(2,s*.08))
  glow(x+w*.72,y+h*.43,max(2,s*.08),RD); return
 if k in ('flyer','kamikaze'):
  ell((x+w*.18,y+h*.25,x+w*.82,y+h*.78),DK,ac,max(1,s*.04)); glow(cx,cy,max(2,s*.1),ac)
  if k=='flyer': poly([(x+w*.18,cy),(x,y+h*.38),(x+w*.12,y+h*.62)],MT,ac); poly([(x+w*.82,cy),(x+w,y+h*.38),(x+w*.88,y+h*.62)],MT,ac)
  return
 if k=='turret':
  d.rounded_rectangle((x+w*.18,y+h*.52,x+w*.82,y+h*.88),3,fill=DK,outline=ac,width=2); d.rectangle((x+w*.35,y+h*.32,x+w*.65,y+h*.58),fill=MT,outline=ac); d.rectangle((x+w*.5,y+h*.38,x+w*.98,y+h*.46),fill=ac); return
 bw=.58 if k=='brute' else .42; d.rounded_rectangle((cx-w*bw/2,y+h*.28,cx+w*bw/2,y+h*.72),max(2,int(s*.06)),fill=DK,outline=ac,width=max(1,int(s*.035)))
 ell((cx-w*.15,y+h*.10,cx+w*.15,y+h*.34),MT,ac); glow(cx+w*.04,y+h*.21,max(2,s*.055),ac); line([(cx-w*.12,y+h*.68),(cx-w*.18,y+h*.95)],MT,max(2,s*.08)); line([(cx+w*.12,y+h*.68),(cx+w*.18,y+h*.95)],MT,max(2,s*.08))
 if k=='shield': d.rounded_rectangle((x+w*.03,y+h*.28,x+w*.34,y+h*.78),4,fill=CY[:-1]+(55,),outline=CY,width=2)
 d.rectangle((cx+w*.1,y+h*.42,x+w*.93,y+h*.50),fill=MT,outline=ac)
def boss(n,r):
 x,y,w,h=r; cx=x+w*.5; ac=RD if ('enraged' in n or 'damaged' in n) else LI
 poly([(x+w*.08,y+h*.55),(x+w*.22,y+h*.18),(x+w*.45,y+h*.08),(x+w*.76,y+h*.22),(x+w*.94,y+h*.55),(x+w*.78,y+h*.82),(x+w*.25,y+h*.84)],C('#17261f'),ac)
 for px in (.23,.42,.61,.78): line([(x+w*px,y+h*.64),(x+w*(px-.08 if px<.5 else px+.08),y+h*.96)],C('#334a42'),max(2,h*.06))
 poly([(x+w*.30,y+h*.38),(x+w*.72,y+h*.38),(x+w*.62,y+h*.64),(x+w*.38,y+h*.64)],C('#0b1013'),OR); glow(cx,y+h*.46,max(3,min(w,h)*.1),ac)
 d.rectangle((x+w*.03,y+h*.30,x+w*.32,y+h*.39),fill=MT,outline=ac); d.rectangle((x+w*.70,y+h*.30,x+w*.98,y+h*.39),fill=MT,outline=ac)
 if 'defeat' in n: d.rectangle((x,y,x+w,y+h),fill=C('#ff6b32',60))
def prop(n,r):
 x,y,w,h=r
 if n in ('platform','bridge'): d.rounded_rectangle((x+1,y+1,x+w-1,y+h-1),2,fill=C('#13262a'),outline=CY); line([(x,y+h*.15),(x+w,y+h*.15)],CY,max(1,h*.08))
 elif n in ('crates','barrels','pods'): d.rounded_rectangle((x+2,y+2,x+w-2,y+h-2),3,fill=C('#26343c'),outline=OR if n=='barrels' else LI,width=2); line([(x+w*.2,y+h*.2),(x+w*.8,y+h*.8)],C('#61717a'))
 elif n=='crystals':
  for i in range(4): poly([(x+w*(.15+i*.2),y+h*.85),(x+w*(.24+i*.18),y+h*.12),(x+w*(.35+i*.17),y+h*.85)],C('#36e7ff',180),CY)
 elif n in ('checkpoint','portal'): d.rounded_rectangle((x+2,y+2,x+w-2,y+h-2),4,fill=C('#07151c'),outline=CY,width=2); glow(x+w*.5,y+h*.5,max(3,min(w,h)*.22),LI if n=='checkpoint' else CY)
 elif n in ('roots','decorprops'):
  for i in range(5): line([(x+w*i/5,y+h),(x+w*(.1+i/5),y),(x+w*(.25+i/6),y+h*.55)],C('#285c42'),max(1,min(w,h)*.06))
 else: d.rounded_rectangle((x+2,y+2,x+w-2,y+h-2),3,fill=C('#12232a'),outline=CY); glow(x+w*.55,y+h*.45,max(2,min(w,h)*.08),CY)
def fx(n,r):
 x,y,w,h=r; cx=x+w/2; cy=y+h/2; c=OR if ('orange' in n or 'red' in n or 'debris' in n) else (LI if 'green' in n else CY)
 if 'smoke' in n:
  for i in range(6): ell((x+w*.1+i*w*.1,y+h*.3-(i%2)*h*.12,x+w*.35+i*w*.1,y+h*.72),C('#8b7474',80))
 elif 'shockwave' in n:
  for q in range(3): d.ellipse((x+q*2,y+q*2,x+w-q*2,y+h-q*2),outline=c,width=max(1,int(min(w,h)*.05)))
 else:
  for i in range(12): a=i*math.pi/6; rr=min(w,h)*(.45 if i%2==0 else .2); line([(cx,cy),(cx+math.cos(a)*rr,cy+math.sin(a)*rr)],c,max(1,min(w,h)*.06))
  glow(cx,cy,max(2,min(w,h)*.14),c)
for n,r0 in M.items():
 r=[int(round(v)) for v in r0]
 if n.startswith('kael_'): kael(n,r)
 elif n.startswith('boss_'): boss(n,r)
 elif n.startswith(('grunt_','hound_','flyer_','turret_','shield_','burrow_','kamikaze_','brute_','sniper_')): mech(n,r,n.split('_')[0])
 elif n.startswith(('muzzle_','impact_','explosion_','smoke_')) or n in ('boss_orbs','boss_shockwave','boss_debris'): fx(n,r)
 else: prop(n,r)
(ROOT/'assets').mkdir(exist_ok=True); im.save(ROOT/'assets/atlas-safe.png',optimize=True)
BW,BH=1672,941; bg=Image.new('RGB',(BW,BH),'#031018'); b=ImageDraw.Draw(bg,'RGBA')
for y in range(BH):
 t=y/BH; b.line((0,y,BW,y),fill=(3+int(4*t),16+int(20*t),24+int(14*t),255))
for i in range(120):
 x=random.randrange(BW); y=random.randrange(170); q=random.choice([1,1,2]); b.ellipse((x,y,x+q,y+q),fill=(130,255,231,130))
b.ellipse((1250,25,1450,225),fill=(55,112,110,110),outline=(90,255,220,130),width=3)
for i in range(-1,12): x=i*180; p=170+random.randrange(-55,55); b.polygon([(x,300),(x+105,p),(x+220,300)],fill=(12,45,48,255))
for i in range(14): x=i*135+random.randrange(-25,25); h=random.randrange(70,180); b.rectangle((x,300-h,x+45,300),fill=(15,44,50,210)); b.rectangle((x+8,318-h,x+15,365-h),fill=(58,255,211,90))
for i in range(7): x=90+i*250; b.rectangle((x,320,x+25,510),fill=(60,210,255,45)); b.rectangle((x+8,320,x+14,510),fill=(120,255,240,75))
for i in range(45): x=i*42; y=510+random.randrange(-50,35); b.ellipse((x-35,y-25,x+50,y+35),fill=(20,93,60,245))
for i in range(18): x=i*100; b.line((x,600,x+random.randrange(-80,80),820),fill=(35,78,58,255),width=random.randrange(10,22)); b.ellipse((x-45,590,x+65,680),fill=(25,105,66,230))
for y in range(650,820,22): b.rectangle((0,y,BW,y+10),fill=(90,235,205,15))
for i in range(36): x=i*52; b.polygon([(x,BH),(x+random.randrange(10,25),770+random.randrange(-60,80)),(x+35,BH)],fill=(4,31,20,255))
bg.save(ROOT/'assets/neon-jungle-safe.webp','WEBP',quality=88,method=6)
print('generated',len(M),'sprites',W,H)
