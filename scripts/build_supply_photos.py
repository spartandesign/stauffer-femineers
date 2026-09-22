"""Rebuild compact supply-photo panels without changing existing lesson text.

Edit assets/supply-photos/catalog.json to replace a supplier reference with a
verified classroom photograph, then run this script. Original photos are kept
unmodified; captions distinguish order-list products from equivalent examples.
"""
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- supply-photos:start -->'
END = '<!-- supply-photos:end -->'
PATTERN = re.compile(re.escape(START) + r'.*?' + re.escape(END), re.S)
CIRCUIT = ['sewable-led', 'coin-holder', 'conductive-thread', 'coin-cell', 'needles', 'threaders']
STAMP = ['wood-blanks', 'floss', 'needles', 'threaders']
MICROBIT = ['microbit', 'microbit-kit', 'usb-cable']
NEOPIXEL = ['microbit', 'neopixel-strip', 'microbit-kit', 'three-aaa', 'jst-connector', 'usb-cable']
ROBOTICS = ['hummingbird-controller', 'microbit', 'distance-sensor', 'robot-led', 'position-servo', 'hummingbird-power']
GUIDES = {
    'mentor-badge-prep.html': CIRCUIT,
    'mentor-circuit-lab-prep.html': CIRCUIT,
    'mentor-future-stamp-prep.html': STAMP,
    'mentor-microbit-prep.html': MICROBIT,
    'mentor-neopixel-prep.html': NEOPIXEL,
    'mentor-hummingbird-prep.html': ROBOTICS,
}
SUPPLIES = {
    'Denim-shirt circuit supplies': ('shirt-supply-photos', CIRCUIT[:4]),
    'Future-stamp stitching station': ('stamp-supply-photos', STAMP),
    'District Kickoff badge materials · separate event stock': ('badge-supply-photos', CIRCUIT),
    'Sewing and painting tools': ('sewing-supply-photos', ['needles', 'threaders', 'floss']),
    'Programmable-hat electronics': ('hat-supply-photos', NEOPIXEL),
    'Programming devices': ('device-supply-photos', MICROBIT),
    'Creative Robotics equipment': ('robotics-supply-photos', ROBOTICS),
}

def esc(text): return html.escape(str(text), quote=True)

def without_photo_panels(text):
    """Ignore only generated photo additions when checking preserved lessons."""
    return PATTERN.sub('', text)

def panel(keys, panel_id, catalog):
    cards=[]
    for key in keys:
        r=catalog[key]
        cards.append(f'''<figure class="supply-photo-card"><a class="supply-photo-link" href="{esc(r['src'])}" target="_blank" rel="noopener" aria-label="View photo: {esc(r['title'])}"><img src="{esc(r['src'])}" alt="{esc(r['alt'])}" width="{r['width']}" height="{r['height']}" loading="lazy" decoding="async"></a><figcaption><strong class="supply-photo-name">{esc(r['title'])}</strong><span class="supply-photo-kind">{esc(r['kind'])}</span><p class="supply-photo-note">{esc(r['note'])}</p><span class="supply-photo-source">Photo: <a href="{esc(r['source'])}" target="_blank" rel="noopener">{esc(r['credit'])}</a></span></figcaption></figure>''')
    return START + f'''<details class="supply-photos no-print" id="{panel_id}"><summary><span>See supply photos</span><small>{len(keys)} reference photos · tap to identify</small></summary><div class="supply-photo-body"><p class="supply-photo-intro">Product/reference photos, not our delivered inventory. Tap a photo to enlarge it. Compare the actual labels and kit list; appearance alone does not confirm electrical compatibility. These optional photos stay out of printouts.</p><div class="supply-photo-grid">{''.join(cards)}</div></div></details>''' + END

def assets(source):
    css='<link rel="stylesheet" href="assets/supply-photos.css">'
    js='<script src="assets/supply-photos.js"></script>'
    if css not in source: source=source.replace('</head>',css+'</head>')
    if js not in source: source=source.replace('</body>',js+'</body>')
    return source

def main():
    catalog={r['id']:r for r in json.loads((ROOT/'assets/supply-photos/catalog.json').read_text(encoding='utf-8'))}
    for name,keys in GUIDES.items():
        path=ROOT/name
        source=without_photo_panels(path.read_text(encoding='utf-8'))
        pattern=r'(<section\b[^>]*\bid="gather"[^>]*>.*?)(</section>)'
        source,count=re.subn(pattern,lambda m:m[1]+panel(keys,'supply-photos',catalog)+m[2],source,count=1,flags=re.S)
        assert count==1, name
        path.write_text(assets(source),encoding='utf-8')
    path=ROOT/'our-supplies.html'
    source=without_photo_panels(path.read_text(encoding='utf-8'))
    for heading,(panel_id,keys) in SUPPLIES.items():
        pattern=r'(<section\b[^>]*><h2>'+re.escape(heading)+r'</h2>.*?)(</section>)'
        source,count=re.subn(pattern,lambda m:m[1]+panel(keys,panel_id,catalog)+m[2],source,count=1,flags=re.S)
        assert count==1, heading
    # Keep the existing concept illustrations available without competing with
    # the identification photos. Never present these cartoons as supply photos.
    if 'supply-concept-preview' not in source:
        pattern=r'(<div class="concept-visual-grid">.*?</div>)'
        source,count=re.subn(pattern,r'<details class="supply-concept-preview no-print"><summary>See the optional concept illustrations</summary>\1</details>',source,count=1,flags=re.S)
        assert count==1
    path.write_text(assets(source),encoding='utf-8')
    # The badge clipboard stays compact; its screen-only toolbar opens photos
    # in the detailed guide instead of adding pictures to the printed sheet.
    path=ROOT/'mentor-badge-checklist.html'
    source=without_photo_panels(path.read_text(encoding='utf-8'))
    anchor='<a class="button secondary" href="mentor-badge-prep.html">Full badge mentor guide</a>'
    assert source.count(anchor)==1
    source=source.replace(anchor,anchor+START+'<a class="button secondary" href="mentor-badge-prep.html#supply-photos">See supply photos</a>'+END)
    path.write_text(source,encoding='utf-8')
    print(f'Built photo panels in {len(GUIDES)+1} pages using {len(catalog)} reference photographs.')

if __name__=='__main__': main()
