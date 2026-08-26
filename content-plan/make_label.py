import qrcode, io, base64, math
from qrcode.image.svg import SvgPathImage

# ---- real QR (website) ----
qr = qrcode.QRCode(border=0, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data("https://www.lespaillettesvertes.ch")
qr.make(fit=True)
m = qr.get_matrix()
n = len(m)
cell = 1.0
qr_paths=[]
for r,row in enumerate(m):
    for c,v in enumerate(row):
        if v:
            qr_paths.append(f'<rect x="{c*cell:.3f}" y="{r*cell:.3f}" width="{cell}" height="{cell}"/>')
qr_svg = f'<g>{"".join(qr_paths)}</g>'
QRN=n

# ---- barcode (representative EAN-style bars, deterministic) ----
import hashlib
seed = "6616054429911"
bars=[]
x=0.0
h=hashlib.md5(seed.encode()).hexdigest()
widths=[ (int(ch,16)%3)+1 for ch in (h*4) ]
i=0; pos=0.0
toggle=True
for w in widths[:60]:
    if toggle:
        bars.append(f'<rect x="{pos:.2f}" y="0" width="{w}" height="60" fill="#222"/>')
    pos+=w
    toggle=not toggle
barcode_svg="".join(bars)
BARW=pos

# ---- paillettes leaves (cluster, upper-right of wordmark) ----
greens = ["#8FB573","#6F9A52","#A7C48C","#5E8C46"]
leaves=[]
import random
random.seed(7)
pts=[(0,0),(14,-6),(28,-2),(10,-18),(24,-16),(38,-10),(20,-30),(34,-26),(48,-20),(6,-30),(44,-34),(30,-40),(16,2),(2,-14)]
for idx,(dx,dy) in enumerate(pts):
    ang = (idx*47)%180 - 90
    col = greens[idx%len(greens)]
    leaves.append(f'<ellipse cx="{dx}" cy="{dy}" rx="7.2" ry="3.3" fill="{col}" transform="rotate({ang} {dx} {dy})"/>')
leaves_svg="".join(leaves)

W,H = 820, 1160
MX = 70
CX = W/2

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <clipPath id="card"><rect x="14" y="14" width="{W-28}" height="{H-28}" rx="26"/></clipPath>
</defs>
<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>
<rect x="14" y="14" width="{W-28}" height="{H-28}" rx="26" fill="#FCFBF6" stroke="#E4E7DE" stroke-width="2"/>
<g clip-path="url(#card)">
  <!-- Eben-Hezer colour-code corner -->
  <path d="M14 14 L184 14 L14 184 Z" fill="#8E2A3B"/>
</g>

<!-- Logo: paillettes + wordmark -->
<g transform="translate({CX-70},150)">
  <g transform="translate(150,4)">{leaves_svg}</g>
  <text x="150" y="2" text-anchor="end" font-family="DejaVu Serif" font-style="italic" font-size="26" fill="#4A4A4A">les</text>
  <text x="150" y="46" text-anchor="end" font-family="DejaVu Serif" font-size="52" fill="#3F5E3A">paillettes</text>
  <text x="150" y="96" text-anchor="end" font-family="DejaVu Serif" font-size="52" fill="#3F5E3A">vertes</text>
</g>

<!-- rules + product name -->
<line x1="{MX}" y1="300" x2="{W-MX}" y2="300" stroke="#CFT" stroke="#D2D8CC" stroke-width="1.5"/>
<text x="{CX}" y="372" text-anchor="middle" font-family="DejaVu Sans Mono" font-weight="bold" font-size="50" letter-spacing="3" fill="#262626">ACIDE CITRIQUE</text>
<text x="{CX}" y="416" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="24" letter-spacing="2" fill="#8A8F86">Zitronensäure · Citric Acid</text>
<line x1="{MX}" y1="452" x2="{W-MX}" y2="452" stroke="#D2D8CC" stroke-width="1.5"/>

<!-- weight -->
<text x="{CX}" y="582" text-anchor="middle" font-family="DejaVu Sans Mono" font-weight="bold" font-size="46" fill="#262626">1 kg</text>

<!-- provenance -->
<text x="{CX}" y="700" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="24" fill="#3F5E3A">Provenance : Europe Occidentale</text>

<!-- storage block -->
<line x1="{MX}" y1="800" x2="{W-MX}" y2="800" stroke="#E0E4DA" stroke-width="1.5"/>
<text x="{MX}" y="846" font-family="DejaVu Sans Mono" font-size="21" fill="#555">Stockage : dans un endroit frais et sec,</text>
<text x="{MX}" y="876" font-family="DejaVu Sans Mono" font-size="21" fill="#555">à l'abri de l'humidité.</text>
<text x="{MX}" y="916" font-family="DejaVu Sans Mono" font-size="21" fill="#555">Date de consommation recommandée :</text>

<!-- footer: address + codes -->
<line x1="{MX}" y1="978" x2="{W-MX}" y2="978" stroke="#E0E4DA" stroke-width="1.5"/>
<g font-family="DejaVu Sans Mono" fill="#333">
  <text x="{MX}" y="1026" font-size="22" font-weight="bold">Les Paillettes Vertes Sàrl</text>
  <text x="{MX}" y="1056" font-size="20">Ch. du Polny 31</text>
  <text x="{MX}" y="1084" font-size="20">1066 Epalinges</text>
  <text x="{MX}" y="1112" font-size="20" fill="#3F5E3A">www.lespaillettesvertes.ch</text>
</g>

<!-- QR -->
<g transform="translate({W-MX-250},1010)">
  <g transform="scale({110.0/QRN})" fill="#222">{qr_svg}</g>
</g>
<!-- barcode -->
<g transform="translate({W-MX-118},1012)">
  <g transform="scale({108.0/BARW},1.5)">{barcode_svg}</g>
  <text x="54" y="112" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="14" fill="#333">6 616054 429911</text>
  <text x="54" y="-6" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="13" fill="#777">LOT : AC2501</text>
</g>
</svg>'''

# fix stray token
svg = svg.replace('stroke="#CFT" ','')
open("label-acide-citrique.svg","w",encoding="utf-8").write(svg)

import cairosvg
cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to="label-acide-citrique.png", output_width=1640, output_height=2320)
cairosvg.svg2pdf(bytestring=svg.encode("utf-8"), write_to="label-acide-citrique.pdf")
print("done")
