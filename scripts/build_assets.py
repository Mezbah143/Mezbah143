#!/usr/bin/env python3
"""Rebuild the original Midnight Aurora SVG artwork (Python standard library)."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1] / 'assets'


def header(mobile=False):
    w,h = (600,490) if mobile else (1200,420)
    x = 40 if mobile else 58
    title_y = 154 if mobile else 166
    font = 58 if mobile else 72
    role_y = 260 if mobile else 228
    tagline_y = 329 if mobile else 284
    footer_y = 439 if mobile else 364
    roles = ['Software Developer','Full-Stack Development Enthusiast','IT Student in South Korea','Building Real-World Applications']
    css = '''@keyframes orbit {to {transform:rotate(360deg)}}
@keyframes breathe {50% {opacity:.55}}
@keyframes type {0% {clip-path:inset(0 100% 0 0)} 12%,21% {clip-path:inset(0 0 0 0)} 25%,100% {clip-path:inset(0 100% 0 0)}}
.orbit {transform-box:fill-box;transform-origin:center;animation:orbit 60s linear infinite}
.pulse {animation:breathe 6s ease-in-out infinite}
.role {clip-path:inset(0 100% 0 0);animation:type 24s steps(34,end) infinite}
@media (prefers-reduced-motion:reduce) {.orbit,.pulse,.role {animation:none}.role {display:none}.role.first {display:block;clip-path:none}}
'''
    art = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">Mezbah Uddin | Software Developer</title>
<desc id="desc">Turning ideas into practical software. IT student in Ulsan, South Korea. Animated roles: software developer, full-stack development enthusiast, IT student in South Korea, building real-world applications.</desc>
<defs>
<linearGradient id="base" x2="1" y2="1"><stop stop-color="#080d1b"/><stop offset=".6" stop-color="#11192f"/><stop offset="1" stop-color="#201638"/></linearGradient>
<linearGradient id="accent"><stop stop-color="#67e8f9"/><stop offset=".52" stop-color="#a78bfa"/><stop offset="1" stop-color="#f0abcf"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#5044a8" stop-opacity=".38"/><stop offset="1" stop-color="#5044a8" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#8099c9" stroke-opacity=".07"/></pattern>
</defs><style>{css}</style>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#base)" stroke="#2b3551"/>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="24" fill="url(#grid)"/>
<ellipse class="pulse" cx="{w-90}" cy="180" rx="330" ry="280" fill="url(#halo)"/>
<path d="M{x} 28H{x+86}" stroke="url(#accent)" stroke-width="3" stroke-linecap="round"/>
<g font-family="Arial, Helvetica, sans-serif">
<circle cx="{x+5}" cy="65" r="4" fill="#67e8f9" class="pulse"/>
<text x="{x+20}" y="70" fill="#cbd5eb" font-size="13" letter-spacing="2">CODE WITH PURPOSE.</text>
'''
    if mobile:
        art += f'<text x="{x}" y="{title_y}" fill="#f3f5ff" font-size="{font}" font-weight="700" letter-spacing="-2">MEZBAH</text><text x="{x}" y="{title_y+66}" fill="url(#accent)" font-size="{font}" font-weight="700" letter-spacing="-2">UDDIN</text>'
    else:
        art += f'<text x="{x}" y="{title_y}" fill="#f3f5ff" font-size="{font}" font-weight="700" letter-spacing="-3">MEZBAH <tspan fill="url(#accent)">UDDIN</tspan></text>'
    for index,role in enumerate(roles):
        art += f'<g class="role {"first" if index==0 else ""}" style="animation-delay:{index*6}s"><text x="{x}" y="{role_y}" fill="#67e8f9" font-family="monospace" font-size="{21 if mobile else 23}">{escape(role)}</text></g>'
    if mobile:
        art += f'<text x="{x}" y="{tagline_y}" fill="#d1d9ec" font-size="25">Turning ideas into</text><text x="{x}" y="{tagline_y+36}" fill="#d1d9ec" font-size="25">practical software.</text>'
    else:
        art += f'<text x="{x}" y="{tagline_y}" fill="#d1d9ec" font-size="24">Turning ideas into practical software.</text>'
    art += f'<path d="M{x} {footer_y-30}H{w-x}" stroke="#2b3551"/><text x="{x}" y="{footer_y}" fill="#98a9c8" font-size="{14 if mobile else 13}" letter-spacing="1">ULSAN, SOUTH KOREA</text>'
    if not mobile:
        art += f'<text x="{w-x}" y="{footer_y}" fill="#98a9c8" font-size="13" letter-spacing="1" text-anchor="end">JAVA / WEB / MOBILE / AI</text>'
        art += '''<g transform="translate(968 190)"><circle r="111" fill="none" stroke="#525981" stroke-opacity=".45"/><circle r="84" fill="none" stroke="#586b98" stroke-opacity=".45" stroke-dasharray="2 7"/>
<g class="orbit"><ellipse rx="141" ry="53" transform="rotate(-32)" fill="none" stroke="url(#accent)" stroke-opacity=".6"/><circle cx="118" cy="-44" r="5" fill="#67e8f9"/></g>
<rect x="-48" y="-48" width="96" height="96" rx="25" fill="#141c35" stroke="url(#accent)"/><text x="0" y="13" fill="#e8eaff" text-anchor="middle" font-family="monospace" font-size="37">&lt;/&gt;</text>
<text x="0" y="145" text-anchor="middle" font-family="monospace" font-size="11" letter-spacing="3" fill="#b6a0ff">BUILD. LEARN. REPEAT.</text></g>'''
    art += '</g></svg>'
    (ROOT / ('header-mobile.svg' if mobile else 'header.svg')).write_text(art)


def badge(name,labels,height=28):
    x,parts = 0,[]
    for index,label in enumerate(labels):
        width = len(label)*7+24
        color = ['#67e8f9','#c4b5fd','#f0abcf'][index%3]
        parts.append(f'<rect x="{x+.5}" y=".5" width="{width-1}" height="{height-1}" rx="7" fill="#111a2e" stroke="#293752"/><text x="{x+width/2}" y="{height/2+4}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="12" fill="{color}">{escape(label)}</text>')
        x += width+6
    (ROOT / f'{name}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{x-6}" height="{height}" viewBox="0 0 {x-6} {height}"><title>{escape(", ".join(labels))}</title>'+''.join(parts)+'</svg>')


if __name__ == '__main__':
    ROOT.mkdir(exist_ok=True)
    header(); header(True)
    for name,labels in {
        'stack-studentbridge':['HTML','CSS','JavaScript','Java Servlets','Tomcat','MySQL'],
        'stack-soccer':['HTML','CSS','JavaScript'],
        'stack-atm':['Java','JavaFX'],
        'stack-arduino':['Arduino','Keypad','LCD','Servo'],
    }.items(): badge(name,labels)
    for name,label in [('portfolio','Portfolio ↗'),('email','Email ↗'),('github','GitHub ↗')]:
        badge('contact-'+name,[label],36)
