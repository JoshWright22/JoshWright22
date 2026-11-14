"""Builds the GitHub profile art so it matches joshwright22.github.io.
Run: py -3.12 tools/build.py [path to the site repo]"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SITE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / 'JoshWright22.github.io'
OUT = ROOT / 'assets'
BG, FG, MUTED, ACCENT, BRIGHT = '#0f0f0f', '#fdfdfd', '#7a7a7a', '#4776ca', '#7ba6e8'
SANS = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'SFMono-Regular', Menlo, monospace"

NAV = ['JOSH WRIGHT', 'ABOUT', 'WORK', 'SKILLS', 'CONTACT']
MARQUEE = ['AI Systems', 'Machine Learning', 'AI Agents', 'Computer Vision', 'AI for Animation',
           'Model Fine-Tuning', 'Reinforcement Learning', 'PyTorch', 'CUDA', 'Python', 'Motion Tracking',
           'Animation Tools', 'Graphics', 'Go', 'C++', 'C#', 'Unreal Engine', 'Devlogs']
# (site poster, out name)
POSTERS = [('unomi-tracking', 'unomi'), ('trust-no-one', 'trust-no-one'), ('codee', '127'),
           ('animation', 'reel'), ('gdcc-map', 'gdcc'), ('atomoc-shelis', 'atomoc'),
           ('gobspin', 'gob-spin'), ('slush-rush', 'slush-rush')]


def key(x, y, hl, hr, delay):
    """A keyframe like the site's: square point with Bezier handles."""
    (lx, ly), (rx, ry) = hl, hr
    return f'''<g class="k" style="animation-delay:{delay}s">
<line x1="{lx}" y1="{ly}" x2="{rx}" y2="{ry}" stroke="{MUTED}" stroke-width="1"/>
<circle cx="{lx}" cy="{ly}" r="3.5" fill="{BG}" stroke="{MUTED}"/><circle cx="{rx}" cy="{ry}" r="3.5" fill="{BG}" stroke="{MUTED}"/>
<rect x="{x-4}" y="{y-4}" width="8" height="8" fill="{FG}"/></g>'''


def header():
    W, H = 1200, 500
    nav_y, tick_y = 36, 64
    slot = W / len(NAV)
    nav, ticks = [], []
    for i, label in enumerate(NAV):
        x = slot * (i + 0.5)
        nav.append(f'<text x="{x}" y="{nav_y}" text-anchor="middle">{label}</text>')
        ticks.append(f'<rect x="{x-4}" y="{tick_y-4}" width="8" height="8" transform="rotate(45 {x} {tick_y})" fill="{BG}" stroke="{FG}" stroke-width="1"/>')
    small = ''.join(f'<line x1="{x}" y1="{tick_y-(4 if x % 50 == 0 else 2)}" x2="{x}" y2="{tick_y+2}"/>' for x in range(0, W + 1, 10))
    # Curves stay in the band above the divider so they never cross the name.
    main = 'M-20,260 C80,200 170,120 280,120 C400,120 480,290 600,290 C720,290 820,130 930,130 C1030,130 1120,230 1220,260'
    ghost = 'M-20,140 C100,190 220,280 360,280 C500,280 600,150 740,150 C880,150 1000,250 1220,220'
    keys = (key(280, 120, (230, 120), (330, 120), 1.1) + key(600, 290, (545, 290), (655, 290), 1.5)
            + key(930, 130, (880, 130), (980, 130), 1.9) + key(360, 280, (310, 280), (410, 280), 1.3)
            + key(740, 150, (690, 150), (790, 150), 1.7))
    grid = ''.join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in (150, 230, 310))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Josh Wright, AI Engineer">
<style>
.nav{{font:500 15px {MONO};letter-spacing:3px;fill:{FG}}}
.draw{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.4s cubic-bezier(.22,1,.36,1) .2s forwards}}
.k{{opacity:0;animation:pop .6s ease forwards}}
.head{{animation:play 9s linear infinite}}
.name{{font:900 92px {SANS};letter-spacing:-3px;fill:{FG}}}
.role{{font:500 15px {MONO};letter-spacing:3px;fill:{BRIGHT}}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes pop{{to{{opacity:1}}}}
@keyframes play{{from{{transform:translateX(0)}}to{{transform:translateX({W}px)}}}}
@media (prefers-reduced-motion:reduce){{.draw{{stroke-dashoffset:0;animation:none}}.k{{opacity:1;animation:none}}.head{{animation:none}}}}
</style>
<rect width="{W}" height="{H}" fill="{BG}"/>
<g stroke="{FG}" stroke-opacity=".07">{grid}</g>
<g class="nav">{''.join(nav)}</g>
<g stroke="{FG}" stroke-opacity=".35">{small}</g>
<line x1="0" y1="{tick_y+2}" x2="{W}" y2="{tick_y+2}" stroke="{FG}" stroke-opacity=".14"/>
{''.join(ticks)}
<path class="draw" pathLength="1" d="{ghost}" fill="none" stroke="#5b6b88" stroke-width="1.4"/>
<path class="draw" pathLength="1" d="{main}" fill="none" stroke="{ACCENT}" stroke-width="2.4"/>
{keys}
<g class="head"><circle cx="0" cy="{tick_y-26}" r="5" fill="{BRIGHT}"/><line x1="0" y1="{tick_y-20}" x2="0" y2="330" stroke="{BRIGHT}" stroke-opacity=".35"/></g>
<line x1="0" y1="340" x2="{W}" y2="340" stroke="{FG}" stroke-opacity=".14"/>
<text class="name" x="40" y="{H-64}">Josh Wright</text>
<text class="role" x="44" y="{H-28}">AI ENGINEER  ·  ASU CS '27  ·  TEMPE, AZ</text>
</svg>'''


def marquee():
    """The site's skills billboard. A sliding row cuts words at the edges here, so it
    shows one full row of whole words at a time and fades to the next row."""
    from PIL import ImageFont
    W, H, size, gap, hold = 1200, 96, 34, 64, 3.0
    font = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', size)
    words = [(w.upper(), font.getlength(w.upper())) for w in MARQUEE]
    pages, row = [], []
    for word in words:
        if row and sum(w for _, w in row) + len(row) * gap + word[1] > W - 80:
            pages.append(row)
            row = []
        row.append(word)
    pages.append(row)
    n = len(pages)
    total = n * hold
    end = 100 / n
    out = []
    for i, page in enumerate(pages):
        x = (W - (sum(w for _, w in page) + (len(page) - 1) * gap)) / 2
        parts = []
        for j, (word, w) in enumerate(page):
            parts.append(f'<text x="{x:.1f}" y="60" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs">{word}</text>')
            x += w
            if j < len(page) - 1:
                c = x + gap / 2
                parts.append(f'<rect x="{c-5:.1f}" y="43" width="10" height="10" transform="rotate(45 {c:.1f} 48)" fill="{BRIGHT}"/>')
                x += gap
        out.append(f'<g class="p" style="animation-delay:{i * hold - 0.0:.1f}s">{"".join(parts)}</g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" aria-hidden="true">
<style>
.t{{font:800 {size}px {SANS};fill:{FG}}}
.p{{opacity:0;animation:page {total:.0f}s linear infinite}}
@keyframes page{{0%{{opacity:0;transform:translateY(14px)}}{end*0.12:.2f}%{{opacity:1;transform:translateY(0)}}{end*0.88:.2f}%{{opacity:1;transform:translateY(0)}}{end:.2f}%,100%{{opacity:0;transform:translateY(-14px)}}}}
@media (prefers-reduced-motion:reduce){{.p{{animation:none}}.p:first-child{{opacity:1}}}}
</style>
<rect width="{W}" height="{H}" fill="{BG}"/>
<line x1="0" y1="0.5" x2="{W}" y2="0.5" stroke="{FG}" stroke-opacity=".14"/><line x1="0" y1="{H-0.5}" x2="{W}" y2="{H-0.5}" stroke="{FG}" stroke-opacity=".14"/>
<g class="t">{"".join(out)}</g>
</svg>'''


def section(label, num):
    """Section divider in the site's mono label style."""
    W, H = 1200, 70
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="40" y="44" style="font:500 13px {MONO};letter-spacing:3px;fill:{BRIGHT}">{num}</text>
<text x="90" y="44" style="font:800 26px {SANS};letter-spacing:-.5px;fill:{FG}">{label.upper()}</text>
<line x1="40" y1="{H-1}" x2="{W-40}" y2="{H-1}" stroke="{FG}" stroke-opacity=".14"/>
<rect x="{W-44}" y="{H-5}" width="8" height="8" transform="rotate(45 {W-40} {H-1})" fill="{BG}" stroke="{FG}"/>
</svg>'''


def posters():
    for src, name in POSTERS:
        im = Image.open(SITE / 'assets' / f'{src}-poster.jpg').convert('RGB')
        ImageOps.fit(im, (640, 360), Image.LANCZOS).save(OUT / f'{name}.jpg', quality=82, optimize=True)


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    (OUT / 'header.svg').write_text(header(), encoding='utf-8')
    (OUT / 'marquee.svg').write_text(marquee(), encoding='utf-8')
    for label, num in [('About', '01'), ('Work', '02'), ('Skills', '03'), ('Contact', '04')]:
        (OUT / f'section-{label.lower()}.svg').write_text(section(label, num), encoding='utf-8')
    posters()
    print('built', len(list(OUT.iterdir())), 'files')
