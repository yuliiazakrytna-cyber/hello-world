import cairosvg, math
GREENC="#16A34A"; GREEN="#3F5E3A"; GREEN2="#6F9A52"; INK="#2C2C2C"; CREAM="#FBF7EF"; LAV="#EDE7F3"
W,H=1240,600
def sun(cx,cy,r,col):
    s=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>'
    for i in range(8):
        a=math.radians(i*45)
        s+=f'<line x1="{cx+math.cos(a)*(r+4):.1f}" y1="{cy+math.sin(a)*(r+4):.1f}" x2="{cx+math.cos(a)*(r+10):.1f}" y2="{cy+math.sin(a)*(r+10):.1f}" stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>'
    return s
leaves=""
pts=[(0,0),(13,-5),(25,-1),(9,-15),(21,-13),(33,-8)]
gr=["#8FB573","#6F9A52","#A7C48C"]
for i,(dx,dy) in enumerate(pts):
    leaves+=f'<ellipse cx="{dx}" cy="{dy}" rx="6" ry="2.8" fill="{gr[i%3]}" transform="rotate({i*40} {dx} {dy})"/>'
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{CREAM}"/><stop offset="1" stop-color="{LAV}"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<!-- LEFT: product photo placeholder -->
<rect x="40" y="60" width="640" height="480" rx="20" fill="#ffffff" stroke="#E4DFEA" stroke-width="2" stroke-dasharray="8 7"/>
{sun(360,250,22,"#E2A53C")}
<text x="360" y="320" text-anchor="middle" font-family="DejaVu Sans" font-size="26" fill="#B7AEC2">Votre photo produits ici</text>
<text x="360" y="352" text-anchor="middle" font-family="DejaVu Sans" font-size="18" fill="#C7BFD2">(savons, soins, Le Carré…)</text>

<!-- RIGHT: offer card -->
<rect x="712" y="80" width="488" height="440" rx="24" fill="#ffffff" stroke="#E7E3DB" stroke-width="2"/>
<g transform="translate(760,150)">{sun(0,-6,11,"#E2A53C")}</g>
<text x="792" y="146" font-family="DejaVu Sans" font-size="22" letter-spacing="4" fill="{GREEN2}">OFFRE D'ÉTÉ</text>
<text x="956" y="290" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="150" fill="{GREENC}">-25%</text>
<text x="956" y="340" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="34" letter-spacing="2" fill="{INK}">SUR TOUT LE SITE</text>
<!-- deadline pill -->
<rect x="806" y="366" width="300" height="46" rx="23" fill="#FBEEE2"/>
<text x="956" y="397" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="22" fill="#C77A2B">Jusqu'au 22 juillet</text>
<!-- CTA -->
<rect x="820" y="432" width="272" height="60" rx="30" fill="{GREENC}"/>
<text x="956" y="471" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="24" fill="#ffffff">J'EN PROFITE</text>
<!-- logo -->
<g transform="translate(956,530)">
  <text x="0" y="0" text-anchor="middle" font-family="DejaVu Serif" font-size="22" fill="{GREEN}">les paillettes vertes</text>
  <g transform="translate(120,-14)">{leaves}</g>
</g>
</svg>'''
open("banner-offre-ete.svg","w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(),write_to="banner-offre-ete.png",output_width=1860,output_height=900)
print("ok")
