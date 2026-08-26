import cairosvg

G="#3F5E3A"; G2="#6F9A52"; CREAM="#FCFBF6"; BOXBG="#EEF3E9"; BORD="#CBD9C0"; INK="#3A3A3A"; SUN="#E2A53C"
W=1000; H=820
def sun(cx,cy,r,col):
    s=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>'
    import math
    for i in range(8):
        a=math.radians(i*45)
        x1=cx+math.cos(a)*(r+5); y1=cy+math.sin(a)*(r+5)
        x2=cx+math.cos(a)*(r+12); y2=cy+math.sin(a)*(r+12)
        s+=f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
    return s

# step icons (white stroke inside green badge), drawn centered at (0,0) scale ~ for 26px box
def bag():
    return '<g stroke="#fff" stroke-width="2.4" fill="none"><rect x="-9" y="-6" width="18" height="16" rx="2.5"/><path d="M-4 -6 a4 5 0 0 1 8 0"/></g>'
def umbrella():
    return '<g stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round"><path d="M-11 0 a11 11 0 0 1 22 0 q-5.5 -4 -11 0 q-5.5 -4 -11 0 Z" fill="#fff" stroke="none"/><line x1="0" y1="0" x2="0" y2="11"/><path d="M0 11 a3 3 0 0 0 5 0"/></g>'
def truck():
    return '<g stroke="#fff" stroke-width="2.2" fill="none"><rect x="-11" y="-6" width="13" height="11" rx="1"/><path d="M2 -2 h6 l4 4 v3 h-10 Z"/><circle cx="-5" cy="7" r="2.4" fill="#fff" stroke="none"/><circle cx="7" cy="7" r="2.4" fill="#fff" stroke="none"/></g>'

def step(y, icon, date, label):
    return f'''
  <circle cx="120" cy="{y}" r="26" fill="{G}"/>
  <g transform="translate(120,{y})">{icon}</g>
  <text x="178" y="{y-6}" font-family="DejaVu Sans" font-weight="bold" font-size="27" fill="{G}">{date}</text>
  <text x="178" y="{y+24}" font-family="DejaVu Sans" font-size="22" fill="{INK}">{label}</text>'''

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{CREAM}"/>
<rect x="10" y="10" width="{W-20}" height="{H-20}" rx="22" fill="#ffffff" stroke="#E4E7DE" stroke-width="2"/>

{sun(92,92,20,SUN)}
<text x="140" y="86" font-family="DejaVu Serif" font-size="40" font-weight="bold" fill="{G}">Notre atelier fait</text>
<text x="140" y="134" font-family="DejaVu Serif" font-size="40" font-weight="bold" fill="{G}">une pause estivale</text>

<text x="60" y="206" font-family="DejaVu Sans" font-size="23" fill="{INK}">Pour recevoir vos essentiels avant les vacances,</text>
<text x="60" y="240" font-family="DejaVu Sans" font-size="23" fill="{INK}">pensez à <tspan font-weight="bold" fill="{G}">commander avant le 22 juillet</tspan>.</text>

<!-- callout box -->
<rect x="50" y="296" width="{W-100}" height="316" rx="18" fill="{BOXBG}" stroke="{BORD}" stroke-width="2"/>
<text x="120" y="346" font-family="DejaVu Sans" font-size="19" letter-spacing="2" fill="{G2}">LES DATES À RETENIR</text>
<line x1="120" y1="392" x2="120" y2="556" stroke="{BORD}" stroke-width="2"/>
{step(392,bag(),"22 juillet","Dernier jour pour commander")}
{step(474,umbrella(),"22 juil. → 10 août","Atelier fermé — pause estivale")}
{step(556,truck(),"10 août","Reprise : vos commandes sont expédiées")}

<text x="60" y="688" font-family="DejaVu Sans" font-size="23" fill="{INK}">Les commandes passées pendant la fermeture seront préparées</text>
<text x="60" y="722" font-family="DejaVu Sans" font-size="23" fill="{INK}">et expédiées dès notre retour, le 10 août.</text>
<text x="60" y="772" font-family="DejaVu Serif" font-style="italic" font-size="24" fill="{G}">Merci pour votre patience </text>
<g transform="translate(405,765)"><ellipse cx="0" cy="0" rx="9" ry="4.2" fill="{G2}" transform="rotate(-35)"/><ellipse cx="11" cy="-3" rx="9" ry="4.2" fill="{G}" transform="rotate(20 11 -3)"/></g>
</svg>'''
open("newsletter-pause-estivale.svg","w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(),write_to="newsletter-pause-estivale.png",output_width=1500,output_height=1230)
print("ok")
