"""Six fixed-home-table cards for the September 24 available-supplies plan."""
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'output/pdf/September-24-Backup-Table-Cards.pdf'
W, H = landscape(letter)
INK = HexColor('#18233A')
MUTED = HexColor('#4C5869')
LINE = HexColor('#CDD3DD')
PURPLE = HexColor('#5F3DC4')
TEAL = HexColor('#168B88')


def para(c, text, x, top, width, *, size=12, leading=16, bold=False, color=INK):
    style = ParagraphStyle('card', fontName='Helvetica-Bold' if bold else 'Helvetica',
                           fontSize=size, leading=leading, textColor=color)
    p = Paragraph(text, style)
    _, height = p.wrap(width, H)
    assert top - height >= 38, (text, top, height)
    p.drawOn(c, x, top - height)
    return top - height


def make_card(c, code, robotics, page):
    accent = TEAL if robotics else PURPLE
    mentor = 'Stephanie' if robotics else 'Jennifer'
    pathway = 'ROBOTICS' if robotics else 'WEARABLES'
    pale = HexColor('#EAF7F5' if robotics else '#F4F0FF')
    c.setFillColor(accent)
    c.rect(0, H-8, W, 8, fill=1, stroke=0)
    para(c, 'STAUFFER FEMINEERS / THURSDAY, SEPTEMBER 24', 34, 582, 710,
         size=10, leading=12, bold=True, color=accent)
    c.setFillColor(accent)
    c.setFont('Helvetica-Bold', 76)
    c.drawString(32, 487, code)
    para(c, pathway, 202, 550, 550, size=29, leading=33, bold=True)
    para(c, f'Mentor: {mentor}  /  6 students in 3 pairs', 203, 511, 550, size=17, leading=21)
    para(c, 'This is your home table. Follow your mentor; there is no station rotation.',
         203, 483, 548, size=12, leading=16)
    c.setStrokeColor(LINE)
    c.line(34, 445, W-34, 445)
    para(c, 'YOUR ACTIVITY SEQUENCE', 34, 425, 430, bold=True, color=accent, size=11, leading=14)
    if robotics:
        steps = [
            ('1. Connect + identify', 'Use your assigned Hummingbird Bit kit and iPad. Check the full device name and the safe reset.'),
            ('2. Explore + program', 'Read the input your mentor prepared. Control two outputs. Movement requires mentor release.'),
            ('3. Test + improve', 'Run three trials. Change one thing and retest. Swap Driver and Navigator after each challenge.'),
            ('4. Share + design', 'Join the paper-symbol and NeoPixel preview. Develop three ideas and a shared robot proposal.'),
            ('5. Save + close', 'Save code, results, and both reflections. At 2:21, reset safely, power off, count, and store.'),
        ]
        safety = '<b>One numbered kit per pair.</b><br/>Keep the kit at this table.<br/><br/><b>Power off before wiring changes.</b><br/>Ask a mentor to make the change.<br/><br/><b>R boards stay in Robotics.</b><br/>Do not load MakeCode on them.<br/><br/><b>Unexpected motion, heat, or odor?</b><br/>Stop, power off, and tell a mentor.'
        note = 'Two LEDs are the fallback. If no servo was tested, record motion as deferred.'
    else:
        steps = [
            ('1. Sew one LED circuit', 'Share one felt practice set per pair. Both partners practice stitches and pad connections.'),
            ('2. Program a micro:bit', 'Use your W board and laptop. A = heart, B = happy, A+B = clear. Both partners take a turn.'),
            ('3. Test + improve', 'Change a symbol for a real user. Test A, B, and A+B. Save code and record the actual result.'),
            ('4. Share + design', 'Draw a paper symbol and observe the NeoPixel preview. Each student develops three ideas and a shirt-and-hat proposal.'),
            ('5. Save + close', 'Save your own evidence and reflection. At 2:21, remove power, return needles, count, and store.'),
        ]
        safety = '<b>Battery out while sewing.</b><br/>Keep + and - stitch paths apart.<br/><br/><b>Mentor checks before power.</b><br/>Keep coin cells in the mentor tray until your circuit is released.<br/><br/><b>Needle in hand or counted tray.</b><br/>Return it before breaks and coding.<br/><br/><b>Heat or odor?</b><br/>Stop and tell a mentor.'
        note = 'Share practice equipment. Your final shirt-and-hat proposal is individual.'
    top = 398
    for title, body in steps:
        top = para(c, title, 34, top, 438, bold=True, size=13, leading=16)
        top = para(c, body, 34, top-3, 438, size=12, leading=15) - 12
    assert top > 73, top
    c.setFillColor(pale)
    c.roundRect(496, 116, 262, 311, 10, fill=1, stroke=0)
    top = para(c, 'SAFETY + ROLES', 512, 411, 230, size=11, leading=14, bold=True, color=accent)
    top = para(c, safety, 512, top-12, 230, size=11.5, leading=15)
    assert top >= 132, top
    para(c, note, 496, 105, 262, size=10, leading=13, color=MUTED)
    c.setStrokeColor(LINE)
    c.line(34, 64, W-34, 64)
    para(c, 'SNACK 9:25-9:38    LUNCH 12:42-1:12    CLEANUP 2:21-2:41',
         34, 53, 700, size=10, leading=12, bold=True)
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 8)
    c.drawString(34, 22, 'Follow the September 24 student guide for the full agenda. Power off and count before leaving.')
    c.drawRightString(W-34, 22, f'{page} / 6')
    c.linkURL('https://spartandesign.github.io/stauffer-femineers/september-24-backup.html',
              (34, 17, 650, 33), relative=0)
    c.showPage()


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=(W,H), pageCompression=1)
    c.setTitle('September 24 Backup Plan - Six Home Table Cards')
    c.setAuthor('Stauffer Femineers')
    for page, code in enumerate(['W1','W2','W3','R1','R2','R3'], 1):
        make_card(c, code, code.startswith('R'), page)
    c.save()
    print(OUTPUT)


if __name__ == '__main__':
    main()
