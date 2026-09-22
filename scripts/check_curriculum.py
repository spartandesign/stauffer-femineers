"""Validate local curriculum navigation, old anchors, and preserved lesson content."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import subprocess
from build_navigation import GENERATED
from build_supply_photos import without_photo_panels

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids, self.links, self.nav = [], [], []
        self.in_nav = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'nav' and attrs.get('id') == 'main-nav':
            self.in_nav = True
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
            if self.in_nav:
                self.nav.append(attrs['href'])

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.in_nav = False

def main_body(source):
    return re.search(r'<main\b[^>]*>(.*?)</main>', source, re.S).group(1)

def main():
    sources = {p.name: p.read_text(encoding='utf-8-sig') for p in ROOT.glob('*.html')}
    pages = {name: Page(source) for name, source in sources.items()}
    errors = []
    for name, page in pages.items():
        if page.nav != ['index.html', 'my-project.html', 'tutorials.html', 'mentors.html']:
            errors.append(f'{name}: inconsistent main navigation {page.nav}')
        if len(set(page.ids)) != len(page.ids):
            errors.append(f'{name}: duplicate ids')
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = unquote(url.path) or name
            if not (ROOT / target).is_file():
                errors.append(f'{name}: missing {href}')
            elif target in pages and url.fragment and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{name}: missing anchor {href}')
    visited, pending = set(), ['index.html']
    while pending:
        name = pending.pop()
        if name in visited:
            continue
        visited.add(name)
        for href in pages[name].links:
            url = urlsplit(href)
            if not url.scheme and not url.netloc and url.path in pages:
                pending.append(url.path)
    unreachable = set(pages) - visited - {'404.html'}
    if unreachable:
        errors.append(f'Unreachable pages: {sorted(unreachable)}')
    original_names = subprocess.check_output(['git', 'ls-tree', '--name-only', 'HEAD'], cwd=ROOT, text=True).splitlines()
    preserved = 0
    allowed_body_changes = {'index.html', 'start-here.html', 'mentor-lesson-plans.html', 'mentor-print-center.html', 'mentor-neopixel-prep.html', 'program-roadmap.html', 'lunch-checkpoints.html', 'phase-2-prototype.html', 'recruitment.html', 'recruitment-toolkit.html', 'family-commitment.html', 'student-application.html', 'returning-member-confirmation.html', 'our-supplies.html', 'meet-the-neopixels.html', 'wearable-design-proposal.html', 'fabrication-lab.html', '404.html'}
    for name in original_names:
        if not name.endswith('.html'):
            continue
        original = subprocess.check_output(['git', 'show', f'HEAD:{name}'], cwd=ROOT).decode('utf-8-sig')
        if name not in sources:
            errors.append(f'Deleted original guide: {name}')
            continue
        lost = set(Page(original).ids) - set(pages[name].ids)
        if lost:
            errors.append(f'{name}: removed old anchors {sorted(lost)}')
        if name not in allowed_body_changes | GENERATED:
            old_body = main_body(original).replace('September 14', 'September 24').replace('Sept. 14', 'Sept. 24')
            if without_photo_panels(old_body).strip() != without_photo_panels(main_body(sources[name])).strip():
                errors.append(f'{name}: unexpected lesson body change')
            else:
                preserved += 1
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(f'PASS: {len(pages)} pages share the four-link menu; all local links and anchors resolve; every lesson is reachable; {preserved} detailed lesson bodies match the original; all original pages and anchors remain.')

if __name__ == '__main__':
    main()
