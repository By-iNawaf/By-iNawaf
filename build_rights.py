#!/usr/bin/env python3
"""Builds assets/rights.svg  (vertical neon timeline, no boxes). Edit ROWS to change the text."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROWS = [
 ("shield", "رقابة كاملة",  "جميع البوتات التي أقوم بتطويرها تخضع لرقابة شخصية كاملة"),
 ("ban",    "ممنوع البيع", "ممنوع بيعها في أي متجر أو منصة خارجية"),
 ("check",  "متاحة للجميع", "متاحة للاستفادة العامة بصيغة أفضل وأكثر تطوراً"),
 ("lock",   "حماية الحقوق", "أي محاولة لإعادة بيعها أو التعديل عليها دون إذن تعتبر انتهاكاً للحقوق"),
]
CSS = """:root{--g:#00ff88;--c:#00e5ff;--m:#ff3d8b;--o:#ff8a3d;--t:#e6edf3;--k:#06130d}
@media (prefers-color-scheme:light){:root{--g:#00b868;--c:#0096b4;--m:#e0245e;--o:#e8701a;--t:#1f2328;--k:#fff}}
text{font-family:"Segoe UI","SF Pro Arabic","Geeza Pro",Tahoma,Arial,sans-serif}
.h{font-size:23px;font-weight:800;fill:url(#gr)}.s{font-size:17px;fill:var(--t);opacity:.82}
.num{font-family:ui-monospace,Consolas,monospace;font-size:64px;font-weight:800;fill:none;stroke:var(--g);stroke-opacity:.28;stroke-width:1.4}
.f1{fill:url(#gr)}.fm{fill:url(#gm)}.sg{stroke:url(#gr);fill:none}
.k{stroke:var(--k);fill:none;stroke-width:5.5;stroke-linecap:round;stroke-linejoin:round}
.ring{fill:none;stroke:var(--g);stroke-width:2}"""
DEFS = """<linearGradient id="gr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--g)"/><stop offset="1" style="stop-color:var(--c)"/></linearGradient>
<linearGradient id="gm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--m)"/><stop offset="1" style="stop-color:var(--o)"/></linearGradient>
<linearGradient id="sp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--g)" stop-opacity="0"/><stop offset=".12" style="stop-color:var(--g)"/><stop offset=".88" style="stop-color:var(--c)"/><stop offset="1" style="stop-color:var(--c)" stop-opacity="0"/></linearGradient>
<filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>"""
def draw(d, L):
    return (f'<path class="k" d="{d}" stroke-dasharray="{L}" stroke-dashoffset="{L}"><animate attributeName="stroke-dashoffset" '
            f'values="{L};0;0;{L}" keyTimes="0;.28;.85;1" dur="3.6s" repeatCount="indefinite"/></path>')
def pulse(r=29):
    return (f'<circle cx="32" cy="32" r="{r}" class="ring"><animate attributeName="r" values="{r-6};{r+3}" dur="2.4s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".7;0" dur="2.4s" repeatCount="indefinite"/></circle>')
ICONS = {
 "shield": pulse()+'<g filter="url(#gl)"><path class="f1" d="M32 5L10 13v17c0 14 9.5 24 22 29 12.5-5 22-15 22-29V13z"/></g>'+draw("M21 32l8 8 15-17",40),
 "check":  pulse()+'<g filter="url(#gl)"><circle class="f1" cx="32" cy="32" r="24"><animate attributeName="r" values="23;25;23" dur="2.4s" repeatCount="indefinite"/></circle></g>'+draw("M20 33l8 8 17-19",42),
 "ban":    '<circle cx="32" cy="32" r="29" fill="none" stroke="var(--m)" stroke-width="2"><animate attributeName="r" values="23;31" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="2s" repeatCount="indefinite"/></circle><g filter="url(#gl)"><circle class="fm" cx="32" cy="32" r="24"/></g>'+draw("M21 21l22 22",34),
 "lock":   pulse()+'<g filter="url(#gl)"><path class="sg" stroke-width="6.5" stroke-linecap="round" d="M20 28V21a12 12 0 0 1 24 0v7"><animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 -5;0 0;0 0" keyTimes="0;.25;.5;.75;1" dur="3.6s" repeatCount="indefinite"/></path><rect class="f1" x="12" y="27" width="40" height="30" rx="8"/></g><circle cx="32" cy="40" r="4.5" fill="var(--k)"/><rect x="30" y="42" width="4" height="8" rx="2" fill="var(--k)"/>',
}
GAP, TOP, SX = 108, 78, 742
H = TOP + GAP * (len(ROWS) - 1) + 78
b = f'<rect x="{SX-1.5}" y="14" width="3" height="{H-28}" rx="1.5" fill="url(#sp)"/>'
b += (f'<circle cx="{SX}" r="6" fill="#fff" filter="url(#gl)"><animate attributeName="cy" values="20;{H-20}" dur="4.5s" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="4.5s" repeatCount="indefinite"/></circle>')
for i, (ic, head, text) in enumerate(ROWS):
    cy = TOP + i * GAP; d = 0.5 + i * 0.45
    b += (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{d}s" dur="0.8s" fill="freeze"/>'
          f'<animateTransform attributeName="transform" type="translate" from="18 0" to="0 0" begin="{d}s" dur="0.8s" fill="freeze"/>'
          f'<g transform="translate({SX-30},{cy-30})">{ICONS[ic]}</g>'
          f'<text x="{SX-52}" y="{cy-3}" text-anchor="end" class="h">{head}</text>'
          f'<text x="{SX-52}" y="{cy+26}" text-anchor="end" class="s">{text}</text></g>')
open(os.path.join(ROOT, "assets", "rights.svg"), "w", encoding="utf-8").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {H}" width="800" height="{H}"><defs>{DEFS}</defs><style>{CSS}</style>{b}</svg>')
print("rights.svg", H)
