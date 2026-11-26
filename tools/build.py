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

NAV = ['JOSH WRIGHT', 'ABOUT', 'WORK', 'CONTACT']
MARQUEE = ['Model Training', 'Fine-Tuning', 'PyTorch', 'CUDA', 'Reinforcement Learning', 'PPO', 'Self-Play',
           'Computer Vision', 'Motion Capture', 'Forecasting', 'LLM Evaluation', 'AI Agents', 'Benchmarking',
           'Azure GPUs', 'Python', 'C++', 'AI for Animation', 'Games']
# Only projects other people used or played, or that won or scored something (Josh 11/16).
PROJECTS = [  # (site poster, slug on the site, title, result, tags)
    ('unomi-tracking', 'unomi', 'UNOMi', '2.8x faster motion capture, same accuracy', 'SWE INTERN · CV · AZURE GPUS'),
    ('nanotsfm-forecast', 'nanotsfm-forecasting', 'nanoTSFM Forecasting',
     '18% lower error than the nanoTSFM record', 'PYTORCH · FORECASTING'),
    ('trust-no-one', 'trust-no-one', 'Trust No One', 'Placed #9 of 2,253 games', 'UNITY · C# · TEAM LEAD'),
    ('battlecode', 'cambridge-battlecode-2026', 'Cambridge Battlecode 2026',
     'Mined 110,000 ladder matches, trained on 6M turns', 'CUDA · PPO · SELF-PLAY'),
    ('codee', 'theres-no-place-like-127-0-0-1', "There's No Place Like 127.0.0.1",
     'Highest scored pitch at the AZ Game Cup', 'UNITY · C# · PROC GEN'),
    ('gdcc-map', 'game-dev-club-club', 'Game Dev Club Club', 'Created a club across 104 universities', 'REACT · EVENTS'),
    ('atomoc-shelis', 'atomoc-shelis', 'AtOMoC SHeLiS', 'Placed #12 of 150 games', 'GODOT · SOLO'),
    ('gobspin', 'gob-spin', 'Gob Spin', 'Placed #140 of 3,498 games', 'UNITY · C# · PHYSICS'),
    ('slush-rush', 'slush-rush', 'Slush Rush', 'Placed #69 of 434 games', 'GODOT · PYTHON'),
]
CONTACT = [('PORTFOLIO', 'https://joshwright22.github.io/'), ('EMAIL', 'mailto:joshwright0322@gmail.com'),
           ('LINKEDIN', 'https://www.linkedin.com/in/joshua-wright-a94143338/'),
           ('YOUTUBE', 'https://www.youtube.com/@JoshWright_Dev'), ('X', 'https://x.com/joshwright_dev')]


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
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Josh Wright, Game Developer">
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
<text class="role" x="44" y="{H-28}">GAME DEVELOPER  ·  MAKING COOL STUFF  ·  ASU CS '27</text>
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


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace("'", '&#39;').replace('"', '&quot;')


def measure(text, size, bold=False, mono=False, spacing=0.0):
    """Width of a line, the widest of the fonts a visitor may get (Segoe UI on Windows,
    Arial/Helvetica on Mac and Linux), so wrapping leaves room on every system."""
    from PIL import ImageFont
    if mono:
        names = ['consola.ttf', 'cour.ttf']  # Consolas, then Courier New ~ Menlo/DejaVu Mono width
    else:
        names = ['segoeuib.ttf', 'arialbd.ttf'] if bold else ['segoeui.ttf', 'arial.ttf']
    w = max(ImageFont.truetype(f'C:/Windows/Fonts/{n}', size).getlength(text) for n in names)
    return w + spacing * max(len(text) - 1, 0)


def fixed(text, size, bold=False, mono=False, spacing=0.0):
    """textLength pins each line to one width, so a wider fallback font is squeezed to fit
    instead of running past the edge or into its neighbour."""
    return f'textLength="{measure(text, size, bold, mono, spacing):.1f}" lengthAdjust="spacingAndGlyphs"'


def wrap(text, size, width, bold=False):
    lines, line = [], ''
    for word in text.split():
        test = f'{line} {word}'.strip()
        if line and measure(test, size, bold) > width:
            lines.append(line)
            line = word
        else:
            line = test
    return lines + [line]


ABOUT = ('Game developer finishing a B.S. in Computer Science at ASU in May 2027. My jam games placed #9 of 2,253 '
         'in the Brackeys Game Jam and 2nd at the AZ Game Cup, and I am turning my roguelike AtOMoC SHeLiS into a Steam release. '
         'At UNOMi I build animation plugins for Maya, Blender, Unreal and Cinema 4D and made our markerless motion capture '
         '2.8x faster at the same accuracy. I also keyframe by hand and train AI agents to play games.')


def about():
    W, lh = 1200, 36
    lines = wrap(ABOUT, 24, W - 80)
    H = 96 + len(lines) * lh + 40
    text = ''.join(f'<text x="40" y="{96 + i * lh}" {fixed(l, 24)}>{esc(l)}</text>' for i, l in enumerate(lines))
    look = 96 + len(lines) * lh + 10
    want = 'LOOKING FOR  NEW GRAD GAME DEV · GAMEPLAY · ANIMATION TOOLS · GAME AI'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(ABOUT)}">
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="40" y="48" style="font:500 14px {MONO};letter-spacing:3px;fill:{BRIGHT}">01  ABOUT</text>
<g style="font:400 24px {SANS};fill:{FG}">{text}</g>
<text x="40" y="{look}" {fixed(want, 14, mono=True, spacing=2)} style="font:500 14px {MONO};letter-spacing:2px;fill:{MUTED}">LOOKING FOR  <tspan fill="{FG}">NEW GRAD GAME DEV · GAMEPLAY · ANIMATION TOOLS · GAME AI</tspan></text>
<line x1="0" y1="{H-0.5}" x2="{W}" y2="{H-0.5}" stroke="{FG}" stroke-opacity=".14"/>
</svg>'''


def card(i, poster, title, result, tags):
    """One project card: still on the left, number, title, result and tags on the right."""
    import base64
    import io
    W, H, iw, ih = 600, 210, 300, 169
    # A still made here (tools/<name>-poster.jpg) wins over the site's, for a site panel with no video.
    path = ROOT / 'tools' / f'{poster}-poster.jpg'
    if not path.exists():
        path = SITE / 'assets' / f'{poster}-poster.jpg'
    im = ImageOps.fit(Image.open(path).convert('RGB'), (iw * 2, ih * 2), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=78, optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    still = f'<image x="20" y="20" width="{iw}" height="{ih}" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{data}"/>'
    tx, tw = 20 + iw + 22, W - iw - 62
    tag_y = 20 + ih - 2
    # Shrink the title and result together until the result ends well above the tags.
    for ts, rs in ((24, 16), (22, 15), (20, 14), (18, 13)):
        tl, rl = wrap(title, ts, tw, bold=True), wrap(result, rs, tw)
        last = 72 + (len(tl) - 1) * (ts + 6) + ts + 8 + (len(rl) - 1) * (rs + 6)
        if last <= tag_y - 24:
            break
    parts, y = [], 72
    for line in tl:
        parts.append(f'<text x="{tx}" y="{y}" {fixed(line, ts, bold=True)} style="font:800 {ts}px {SANS};fill:{FG}">{esc(line)}</text>')
        y += ts + 6
    y += rs - ts + 8 + 2
    for line in rl:
        parts.append(f'<text x="{tx}" y="{y}" {fixed(line, rs)} style="font:400 {rs}px {SANS};fill:{BRIGHT}">{esc(line)}</text>')
        y += rs + 6
    tag_size = 12
    while measure(tags, tag_size, mono=True, spacing=1.5) > tw and tag_size > 9:
        tag_size -= 1
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(title)}: {esc(result)}">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{FG}" stroke-opacity=".14"/>
{still}
<text x="{tx}" y="40" style="font:500 13px {MONO};letter-spacing:3px;fill:{MUTED}">{i:02d}</text>
{''.join(parts)}
<text x="{tx}" y="{tag_y}" {fixed(tags, tag_size, mono=True, spacing=1.5)} style="font:500 {tag_size}px {MONO};letter-spacing:1.5px;fill:{MUTED}">{esc(tags)}</text>
</svg>'''


def pill(label):
    W, H = 220, 52
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{FG}" stroke-opacity=".25"/>
<rect x="18" y="22" width="8" height="8" transform="rotate(45 22 26)" fill="{BRIGHT}"/>
<text x="{W/2 + 8}" y="31" text-anchor="middle" style="font:500 14px {MONO};letter-spacing:3px;fill:{FG}">{label}</text>
</svg>'''


def readme():
    site = 'https://joshwright22.github.io'
    # No whitespace between the images, so the cards sit edge to edge at the header's width.
    cards = ''.join(f'<a href="{site}/projects/{slug}/"><img src="assets/card-{slug}.svg" alt="{esc(title)}: {result}" width="50%"></a>'
                    for _, slug, title, result, _ in PROJECTS)
    pills = ''.join(f'<a href="{url}"><img src="assets/link-{label.lower()}.svg" alt="{label.title()}" width="20%"></a>'
                    for label, url in CONTACT)
    return f'''<a href="{site}/"><img src="assets/hero.svg" alt="Josh Wright, Game Developer" width="100%"></a>
<img src="assets/marquee.svg" alt="" width="100%">
<img src="assets/about.svg" alt="{esc(ABOUT)}" width="100%">
<p>{cards}</p>
<p>{pills}</p>
'''


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for old in OUT.iterdir():
        old.unlink()
    (OUT / 'hero.svg').write_text(header(), encoding='utf-8')
    (OUT / 'marquee.svg').write_text(marquee(), encoding='utf-8')
    (OUT / 'about.svg').write_text(about(), encoding='utf-8')
    for i, (poster, slug, title, result, tags) in enumerate(PROJECTS, 1):
        (OUT / f'card-{slug}.svg').write_text(card(i, poster, title, result, tags), encoding='utf-8')
    for label, _ in CONTACT:
        (OUT / f'link-{label.lower()}.svg').write_text(pill(label), encoding='utf-8')
    (ROOT / 'README.md').write_text(readme(), encoding='utf-8')
    print('built', len(list(OUT.iterdir())), 'files')
