import cairosvg, math
from PIL import ImageFont

SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

GREEN="#2F5D3A"; GREEN2="#6F9A52"; CREAM="#FBF7EF"; INK="#2C2C2C"; INKL="#555"
RED="#C0392B"; TEAL="#2E7D80"; AMBER="#C58A3A"
W,H=1080,1350; MX=100

def wrap(text,path,size,maxw):
    f=ImageFont.truetype(path,size); out=[]; line=""
    for w in text.split():
        t=(line+" "+w).strip()
        if f.getlength(t)<=maxw: line=t
        else: out.append(line); line=w
    if line: out.append(line)
    return out

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def para(x,y,text,path,fam,size,fill,lh,maxw,anchor="start",weight="normal",style="normal"):
    lines=wrap(text,path,size,maxw); sv=""
    for i,ln in enumerate(lines):
        sv+=f'<text x="{x}" y="{y+i*lh}" font-family="{fam}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" font-style="{style}">{esc(ln)}</text>'
    return sv, y+len(lines)*lh

def leaves(x,y,col_main,scale=1.0):
    gr=["#8FB573","#6F9A52","#A7C48C","#5E8C46"] if col_main=="green" else ["#CFE3BE","#B7D3A0","#A7C48C","#DCEBD0"]
    pts=[(0,0),(13,-5),(25,-1),(9,-15),(21,-13),(33,-8),(17,3)]
    s=f'<g transform="translate({x},{y}) scale({scale})">'
    for i,(dx,dy) in enumerate(pts):
        s+=f'<ellipse cx="{dx}" cy="{dy}" rx="6.5" ry="3" fill="{gr[i%4]}" transform="rotate({i*38} {dx} {dy})"/>'
    return s+"</g>"

def logo(cx,y,dark_on_light=True):
    col=GREEN if dark_on_light else CREAM
    s=f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="DejaVu Serif" font-size="30" fill="{col}">les paillettes vertes</text>'
    s+=leaves(cx+150,y-20,"green" if dark_on_light else "cream",0.9)
    return s

def dots(cx,y,active,dark_on_light=True):
    s=""; base=GREEN if dark_on_light else CREAM
    for i in range(5):
        op="1" if i==active else "0.3"
        s+=f'<circle cx="{cx-80+i*40}" cy="{y}" r="7" fill="{base}" opacity="{op}"/>'
    return s

def pill(x,y,label,color,mark):
    # mark: 'x','check','!'
    w=len(label)*24+150
    s=f'<rect x="{x}" y="{y}" width="{w}" height="76" rx="38" fill="{color}"/>'
    cxm=x+48
    if mark=="x":
        s+=f'<line x1="{cxm-14}" y1="{y+24}" x2="{cxm+14}" y2="{y+52}" stroke="#fff" stroke-width="7" stroke-linecap="round"/><line x1="{cxm+14}" y1="{y+24}" x2="{cxm-14}" y2="{y+52}" stroke="#fff" stroke-width="7" stroke-linecap="round"/>'
    elif mark=="check":
        s+=f'<polyline points="{cxm-16},{y+40} {cxm-4},{y+52} {cxm+18},{y+24}" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    else:
        s+=f'<line x1="{cxm}" y1="{y+20}" x2="{cxm}" y2="{y+46}" stroke="#fff" stroke-width="7" stroke-linecap="round"/><circle cx="{cxm}" cy="{y+58}" r="4.5" fill="#fff"/>'
    s+=f'<text x="{x+90}" y="{y+51}" font-family="DejaVu Sans" font-weight="bold" font-size="34" fill="#fff">{esc(label)}</text>'
    return s

def numbadge(cx,y,n,color):
    return f'<circle cx="{cx}" cy="{y}" r="40" fill="{color}"/><text x="{cx}" y="{y+15}" text-anchor="middle" font-family="DejaVu Serif" font-weight="bold" font-size="44" fill="#fff">{n}</text>'

def save(name,inner,bg):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{bg}"/>{inner}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=name,output_width=1080,output_height=1350)

# ---------- Slide 1 : COVER (green) ----------
i=logo(W/2,150,dark_on_light=False)
i+=f'<text x="{W/2}" y="360" text-anchor="middle" font-family="DejaVu Sans" font-size="30" letter-spacing="8" fill="{GREEN2}">VRAI OU FAUX ?</text>'
t,y=para(W/2,470,"Le déo naturel,",SERIFB,"DejaVu Serif",60,CREAM,74,W-2*MX,"middle",weight="bold")
i+=t
t,y=para(W/2,y+6,"ça ne fonctionne pas ?",SERIFB,"DejaVu Serif",60,CREAM,74,W-2*MX,"middle",weight="bold")
i+=t
i+=f'<text x="{W/2}" y="{y+70}" text-anchor="middle" font-family="DejaVu Serif" font-style="italic" font-size="38" fill="#D8E4CF">On démêle le vrai du faux, ensemble.</text>'
i+=leaves(W/2-16,y+150,"cream",1.6)
i+=f'<text x="{W/2}" y="1230" text-anchor="middle" font-family="DejaVu Sans" font-size="30" fill="#CFE0C4">Faites glisser  →</text>'
i+=dots(W/2,1290,0,dark_on_light=False)
save("deo-1-cover.png",i,GREEN)

# ---------- Myth slides ----------
def myth_slide(name,idx,n,quote,verdict,vcolor,mark,body,extra=None,active=1):
    i=logo(W/2,140,dark_on_light=True)
    i+=numbadge(MX+40,300,n,vcolor)
    t,y=para(MX+110,285,quote,SERIFB,"DejaVu Serif",50,INK,60,W-MX-200,"start",style="italic")
    i+=t
    i+=pill(MX,y+40,verdict,vcolor,mark)
    yy=y+40+76+70
    t,yy=para(MX,yy,body,SANS,"DejaVu Sans",36,INKL,52,W-2*MX,"start")
    i+=t
    if extra:
        t,yy=para(MX,yy+20,extra,SANSB,"DejaVu Sans",36,GREEN,52,W-2*MX,"start",weight="bold")
        i+=t
    i+=dots(W/2,1290,active,dark_on_light=True)
    save(name,i,CREAM)

myth_slide("deo-2-myth1.png",1,"1","« Ça m'empêche de transpirer »","FAUX",RED,"x",
 "La transpiration est naturelle et essentielle pour réguler la température du corps. Les anti-transpirants classiques utilisent des sels d'aluminium pour boucher vos pores. Le déo naturel, lui, laisse votre peau respirer et neutralise seulement les bactéries responsables des mauvaises odeurs.",active=1)

myth_slide("deo-3-myth2.png",2,"2","« Il y a une période d'adaptation »","VRAI",TEAL,"check",
 "Quand vous arrêtez les sels d'aluminium, vos aisselles se libèrent enfin. Pendant 1 à 3 semaines, votre corps élimine les résidus : vous pouvez transpirer un peu plus au début. Pas de panique — c'est le signe que votre peau se régule naturellement.",active=2)

myth_slide("deo-4-myth3.png",3,"3","« Ça pique ou ça irrite »","ÇA DÉPEND",AMBER,"!",
 "Beaucoup de déos naturels contiennent trop de bicarbonate de soude, ce qui peut irriter les peaux sensibles.",
 extra="Chez Les Paillettes Vertes : des formules douces, apaisantes et efficaces, respectueuses de votre peau.",active=3)

# ---------- Slide 5 : CTA (green) ----------
i=logo(W/2,150,dark_on_light=False)
t,y=para(W/2,430,"Prêt·e à sauter le pas ?",SERIFB,"DejaVu Serif",64,CREAM,80,W-2*MX,"middle",weight="bold")
i+=t
i+=f'<text x="{W/2}" y="{y+40}" text-anchor="middle" font-family="DejaVu Serif" font-style="italic" font-size="40" fill="#D8E4CF">Des aisselles fraîches et saines,</text>'
i+=f'<text x="{W/2}" y="{y+96}" text-anchor="middle" font-family="DejaVu Serif" font-style="italic" font-size="40" fill="#D8E4CF">tout l\'été.</text>'
i+=leaves(W/2-16,y+190,"cream",1.5)
t,y2=para(W/2,y+320,"Découvrez nos soins doux et efficaces sur notre e-shop.",SANS,"DejaVu Sans",36,"#EAF1E4",50,W-2*MX-60,"middle")
i+=t
i+=f'<rect x="{W/2-200}" y="{y2+40}" width="400" height="86" rx="43" fill="{CREAM}"/><text x="{W/2}" y="{y2+96}" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="34" fill="{GREEN}">Lien en bio</text>'
i+=dots(W/2,1290,4,dark_on_light=False)
save("deo-5-cta.png",i,GREEN)
print("done")
