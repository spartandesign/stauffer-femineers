from pathlib import Path
from typing import Iterable, Sequence

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = letter
MARGIN = 34
CONTENT_TOP = PAGE_H - 100
CONTENT_BOTTOM = 38

NAVY = HexColor("#18233A")
PURPLE = HexColor("#5F3DC4")
TEAL = HexColor("#168B88")
CORAL = HexColor("#EF6A74")
GOLD = HexColor("#F8C24D")
INK = HexColor("#172033")
MID = HexColor("#5D687A")
LINE = HexColor("#CDD3DD")
PALE_PURPLE = HexColor("#F4F0FF")
PALE_TEAL = HexColor("#EAF7F5")
PALE_CORAL = HexColor("#FFF0F1")
PALE_GOLD = HexColor("#FFF8E6")
PALE_GRAY = HexColor("#F5F7FA")
WHITE = colors.white


def wrap_lines(text: str, font: str, size: float, width: float) -> list[str]:
    lines: list[str] = []
    for raw in str(text).split("\n"):
        words = raw.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if stringWidth(candidate, font, size) <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_text(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    font: str = "Helvetica",
    size: float = 9,
    leading: float | None = None,
    color=INK,
    max_lines: int | None = None,
) -> float:
    leading = leading or size * 1.28
    lines = wrap_lines(text, font, size, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_header(
    c: canvas.Canvas,
    kicker: str,
    title: str,
    subtitle: str,
    page_num: int,
    total_pages: int,
    accent=PURPLE,
    footer_note: str = "Studio-use only. Complete during Femineers time. No homework.",
) -> None:
    c.setFillColor(accent)
    c.rect(0, PAGE_H - 9, PAGE_W, 9, stroke=0, fill=1)
    c.setFillColor(accent)
    c.roundRect(MARGIN, PAGE_H - 54, 26, 26, 7, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(MARGIN + 13, PAGE_H - 45, "L")
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(MARGIN + 36, PAGE_H - 30, kicker.upper())
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 19)
    c.drawString(MARGIN + 36, PAGE_H - 51, title)
    c.setFillColor(MID)
    c.setFont("Helvetica", 8.5)
    c.drawString(MARGIN + 36, PAGE_H - 67, subtitle)
    c.setStrokeColor(LINE)
    c.line(MARGIN, CONTENT_BOTTOM - 4, PAGE_W - MARGIN, CONTENT_BOTTOM - 4)
    c.setFillColor(MID)
    c.setFont("Helvetica", 7.2)
    c.drawString(MARGIN, 20, footer_note)
    c.drawRightString(PAGE_W - MARGIN, 20, f"{page_num} / {total_pages}")


def section_title(c: canvas.Canvas, text: str, x: float, y: float, accent=PURPLE) -> float:
    c.setFillColor(accent)
    c.roundRect(x, y - 3, 7, 18, 2, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11.5)
    c.drawString(x + 13, y, text)
    return y - 20


def draw_bullets(
    c: canvas.Canvas,
    items: Iterable[str],
    x: float,
    y: float,
    width: float,
    size: float = 8.2,
    leading: float = 10.5,
    gap: float = 4,
    checkbox: bool = False,
    color=INK,
) -> float:
    for item in items:
        if checkbox:
            c.setStrokeColor(MID)
            c.rect(x, y - 4, 8, 8, stroke=1, fill=0)
        else:
            c.setFillColor(PURPLE)
            c.circle(x + 3, y, 2, stroke=0, fill=1)
        y = draw_text(c, item, x + 14, y + 2, width - 14, size=size, leading=leading, color=color)
        y -= gap
    return y


def draw_card(
    c: canvas.Canvas,
    x: float,
    y_top: float,
    width: float,
    height: float,
    title: str,
    body: str | None = None,
    bullets: Sequence[str] | None = None,
    accent=TEAL,
    fill=PALE_GRAY,
    title_size: float = 10.5,
    body_size: float = 8.2,
) -> float:
    y = y_top - height
    c.setFillColor(fill)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, width, height, 8, stroke=1, fill=1)
    c.setFillColor(accent)
    c.rect(x, y + height - 6, width, 6, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", title_size)
    c.drawString(x + 12, y + height - 24, title)
    cursor = y + height - 40
    if body:
        cursor = draw_text(c, body, x + 12, cursor, width - 24, size=body_size, leading=body_size * 1.3)
    if bullets:
        cursor -= 3
        draw_bullets(c, bullets, x + 12, cursor, width - 24, size=body_size, leading=body_size * 1.3, gap=2)
    return y


def draw_prompt(
    c: canvas.Canvas,
    label: str,
    x: float,
    y_top: float,
    width: float,
    height: float,
    hint: str = "",
    accent=PURPLE,
    lines: int = 2,
) -> float:
    y = y_top - height
    c.setStrokeColor(LINE)
    c.setFillColor(WHITE)
    c.roundRect(x, y, width, height, 7, stroke=1, fill=1)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 10, y + height - 18, label)
    if hint:
        draw_text(c, hint, x + 10, y + height - 31, width - 20, size=7.2, leading=8.5, color=MID, max_lines=2)
    line_top = y + height - 45 if hint else y + height - 32
    available = max(0, line_top - (y + 10))
    if lines > 0 and available > 5:
        spacing = available / max(lines, 1)
        c.setStrokeColor(HexColor("#BFC6D1"))
        for i in range(lines):
            yy = line_top - i * spacing
            c.line(x + 10, yy, x + width - 10, yy)
    return y


def p(text: str, size: float = 7.2, bold: bool = False, color=INK, align=TA_LEFT) -> Paragraph:
    style = ParagraphStyle(
        name="cell",
        fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=size,
        leading=size * 1.18,
        textColor=color,
        alignment=align,
        spaceAfter=0,
        spaceBefore=0,
    )
    return Paragraph(text, style)


def draw_table(
    c: canvas.Canvas,
    data: Sequence[Sequence[str | Paragraph]],
    x: float,
    y_top: float,
    col_widths: Sequence[float],
    row_heights: Sequence[float] | None = None,
    font_size: float = 7.2,
    header_fill=NAVY,
    stripe=True,
    grid=LINE,
    alignments: dict[int, str] | None = None,
) -> float:
    wrapped: list[list[Paragraph]] = []
    for r, row in enumerate(data):
        wrapped_row: list[Paragraph] = []
        for col, cell in enumerate(row):
            if isinstance(cell, Paragraph):
                wrapped_row.append(cell)
            else:
                align = TA_CENTER if alignments and alignments.get(col) == "center" else TA_LEFT
                wrapped_row.append(p(str(cell), size=font_size, bold=(r == 0), color=WHITE if r == 0 else INK, align=align))
        wrapped.append(wrapped_row)
    table = Table(wrapped, colWidths=list(col_widths), rowHeights=list(row_heights) if row_heights else None, repeatRows=1)
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), header_fill),
        ("GRID", (0, 0), (-1, -1), 0.55, grid),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if stripe:
        for r in range(2, len(data), 2):
            commands.append(("BACKGROUND", (0, r), (-1, r), PALE_GRAY))
    table.setStyle(TableStyle(commands))
    width, height = table.wrapOn(c, sum(col_widths), PAGE_H)
    table.drawOn(c, x, y_top - height)
    return y_top - height


def save_page(c: canvas.Canvas) -> None:
    c.showPage()


def new_pdf(filename: str, title: str) -> canvas.Canvas:
    path = OUT / filename
    c = canvas.Canvas(str(path), pagesize=letter, pageCompression=1)
    c.setTitle(title)
    c.setAuthor("Stauffer Femineers")
    c.setSubject("Low-paper studio tools for the 2026-2027 Limitless curriculum")
    return c


def finish_pdf(c: canvas.Canvas) -> None:
    c.save()


def build_sept14_mentor_pack() -> None:
    filename = "September-14-Mentor-and-Station-Pack.pdf"
    c = new_pdf(filename, "September 14 Mentor and Station Pack")
    total = 11

    # Page 1 - daily brief
    draw_header(
        c,
        "September 14 mentor brief",
        "Technology Studio at a Glance",
        "Print pages 1-3 for each working adult; keep this duplex on a clipboard.",
        1,
        total,
        accent=PURPLE,
        footer_note="Mentor studio tool. Coach understanding, not completion. No homework is assigned.",
    )
    y = CONTENT_TOP
    draw_card(
        c,
        MARGIN,
        y,
        PAGE_W - 2 * MARGIN,
        78,
        "Purpose",
        "Students are trying technologies before choosing how to use them. The finish line is understanding, not polished work. Honest 'not yet' evidence counts.",
        accent=PURPLE,
        fill=PALE_PURPLE,
        body_size=9.2,
    )
    y -= 92
    y = section_title(c, "Mentor assignments", MARGIN, y, PURPLE)
    assignments = [
        ["Stamp", "Circuit Lab", "micro:bit", "NeoPixel"],
        ["________________", "________________", "________________", "________________"],
        ["Robotics lead", "Technical float", "Final count lead", "Room/time lead"],
        ["________________", "________________", "________________", "________________"],
    ]
    y = draw_table(c, assignments, MARGIN, y, [136, 136, 136, 136], row_heights=[21, 23, 21, 23], font_size=7.5, header_fill=NAVY, stripe=False)
    y -= 12
    y = section_title(c, "Schedule", MARGIN, y, TEAL)
    schedule = [
        ["Time", "Wearables", "Robotics", "Safety / understanding gate"],
        ["9:51-10:16", "Rotation 1", "Challenge 1: identity + reset", "Core action and evidence started"],
        ["10:16-10:19", "Count, power off, move", "SAFE RESET; switch roles", "Mentor releases transition"],
        ["10:19-10:44", "Rotation 2", "Challenge 2: input", "Student can show or explain"],
        ["10:44-10:47", "Count, power off, move", "SAFE RESET; switch roles", "No loose or powered parts"],
        ["10:47-11:12", "Rotation 3", "Challenge 3: two outputs", "Evidence saved before extension"],
        ["11:12-11:15", "Count, power off, move", "SAFE RESET; switch roles", "Inspect items labeled"],
        ["11:15-11:40", "Rotation 4", "Challenge 4: interaction", "Fourth capability check"],
        ["11:40-11:45", "Evidence + final count", "Evidence + kit inventory", "Ready / inspect / missing reported"],
    ]
    y = draw_table(c, schedule, MARGIN, y, [74, 130, 150, 190], font_size=6.8)
    y -= 12
    y = section_title(c, "Movement", MARGIN, y, CORAL)
    draw_bullets(
        c,
        [
            "Wearables move clockwise with only the studio passport, iPad, and named stamp bag.",
            "Robotics teams stay with one numbered kit and switch Driver / Navigator roles.",
            "Do not open an unsupported needle or powered station. Reduce capacity or use the prepared visual backup.",
        ],
        MARGIN,
        y,
        PAGE_W - 2 * MARGIN,
        size=8.1,
        leading=10.2,
        gap=3,
    )
    save_page(c)

    # Page 2 - coaching and readiness
    draw_header(
        c,
        "September 14 mentor brief",
        "Keep It Feeling Like a Studio",
        "Short explanations, hands-on noticing, quick conversation, and safe reset.",
        2,
        total,
        accent=TEAL,
        footer_note="Mentor studio tool. Drawings, gestures, oral explanations, and honest unfinished work all count.",
    )
    y = CONTENT_TOP
    left_x = MARGIN
    col_w = (PAGE_W - 2 * MARGIN - 16) / 2
    right_x = left_x + col_w + 16
    draw_card(
        c,
        left_x,
        y,
        col_w,
        176,
        "Ask, then step back",
        bullets=[
            "Show me what changed.",
            "Trace the path with your finger.",
            "What did you expect?",
            "What evidence supports that?",
            "What would you try next?",
            "Accept arrows, labels, gestures, oral explanations, and meaningful unfinished work.",
        ],
        accent=TEAL,
        fill=PALE_TEAL,
    )
    draw_card(
        c,
        right_x,
        y,
        col_w,
        176,
        "Quick understanding check",
        "A student understands when she can do at least one:",
        bullets=[
            "SHOW the behavior.",
            "TRACE the path or system.",
            "PREDICT what will happen.",
            "EXPLAIN one cause-and-effect relationship.",
            "RESET the system safely.",
        ],
        accent=PURPLE,
        fill=PALE_PURPLE,
    )
    y -= 192
    y = section_title(c, "Before release", MARGIN, y, PURPLE)
    y = draw_bullets(
        c,
        [
            "Test every example, file, cable, board, battery, circuit, and numbered kit.",
            "Match labels across each device set; open starter files; stage known-good swaps and photo/video backups.",
            "Count needles and kits; place READY, BUILD, CHECK, EVIDENCE, RETURN, and INSPECT areas.",
            "Give each student/team only the minimum studio sheets. Canvas uploading happens later.",
        ],
        MARGIN,
        y,
        PAGE_W - 2 * MARGIN,
        size=8.2,
        leading=10.3,
        gap=3,
        checkbox=True,
    )
    y -= 6
    y = section_title(c, "Help ladder", MARGIN, y, CORAL)
    ladder = [
        ["1", "Name expected versus observed."],
        ["2", "Check one variable."],
        ["3", "Retest once."],
        ["4", "Use a known-good swap."],
        ["5", "After 60-90 seconds, label the item for inspect and continue with backup evidence."],
    ]
    y = draw_table(c, [["Step", "Mentor move"]] + ladder, MARGIN, y, [46, 498], font_size=7.6, alignments={0: "center"})
    y -= 10
    y = section_title(c, "Immediate stop conditions", MARGIN, y, CORAL)
    draw_card(
        c,
        MARGIN,
        y,
        PAGE_W - 2 * MARGIN,
        68,
        "STOP, MAKE SAFE, AND CALL THE TECHNICAL LEAD",
        "Missing needle; crossed circuit paths; warmth or odor; exposed or damaged wire; unstable flicker; wrong robot moving; loose battery; forced, buzzing, stalled, or obstructed servo.",
        accent=CORAL,
        fill=PALE_CORAL,
        body_size=8.5,
    )
    save_page(c)

    # Page 3 - master route and transition
    draw_header(
        c,
        "September 14 mentor brief",
        "Master Route, Transition, and Final Count",
        "Post one copy; keep one copy with the room/time lead.",
        3,
        total,
        accent=CORAL,
        footer_note="Wearables move. Robotics hardware stays. No transition begins until needles and power are cleared.",
    )
    y = CONTENT_TOP
    route = [
        ["Group", "9:51", "10:19", "10:47", "11:15"],
        ["W1", "Future Stamp", "Circuit Lab", "micro:bit", "NeoPixel"],
        ["W2", "Circuit Lab", "micro:bit", "NeoPixel", "Future Stamp"],
        ["W3", "micro:bit", "NeoPixel", "Future Stamp", "Circuit Lab"],
        ["W4", "NeoPixel", "Future Stamp", "Circuit Lab", "micro:bit"],
        ["Robotics", "Controller + reset", "Read input", "Test outputs", "Interaction"],
    ]
    y = draw_table(c, route, MARGIN, y, [68, 119, 119, 119, 119], row_heights=[28, 34, 34, 34, 34, 34], font_size=7.2, alignments={0: "center"})
    y -= 16
    y = section_title(c, "Three-minute transition", MARGIN, y, TEAL)
    transition = [
        ["Time", "Everyone", "Wearables", "Robotics"],
        ["0:00-0:30", "Hands off; save screen", "Stop stitching/building", "Stop program"],
        ["0:30-1:30", "Make safe", "Needle to tray; power off", "SAFE RESET; disconnect; power off"],
        ["1:30-2:00", "Account + label", "Count; bag stamp; inspect failures", "Count kit; save evidence; inspect failures"],
        ["2:00-2:40", "Move or switch", "Move clockwise", "Kit stays; partners switch roles"],
        ["2:40-3:00", "Seat; hands off", "Match incoming roster", "Confirm new Driver / Navigator"],
    ]
    y = draw_table(c, transition, MARGIN, y, [74, 132, 166, 172], row_heights=[27, 34, 38, 38, 34, 34], font_size=7.1)
    y -= 14
    y = section_title(c, "11:40-11:45 final report", MARGIN, y, PURPLE)
    draw_bullets(
        c,
        [
            "Wearables: four evidence checks; stamp/grid/floss bagged; every needle returned separately; all power off.",
            "Robotics: four evidence boxes; both names and contributions; SAFE RESET; disconnect/off; full kit inventory.",
            "Station leads report READY / INSPECT / MISSING. Unresolved counts stop dismissal to the next block.",
        ],
        MARGIN,
        y,
        PAGE_W - 2 * MARGIN,
        size=8.2,
        leading=10.5,
        gap=4,
        checkbox=True,
    )
    save_page(c)

    station_pages = [
        {
            "title": "W1 - Future Stamp",
            "subtitle": "Meaningful progress counts. Ordinary embroidery floss only.",
            "accent": PURPLE,
            "fill": PALE_PURPLE,
            "finish": "Connect one future need to a simple 6-12-stitch symbol and explain the meaning.",
            "say": "Need -> symbol -> small grid. Do not rush or force it.",
            "prep": [
                "Inspect all blanks; quarantine cracks, splinters, rough edges, and blocked holes.",
                "Pretest the exact needle, threader, floss thickness, and hole; cut short ordinary-floss lengths.",
                "Stage 6 x 6 planning grids, named bags, paper backups, one finished and one in-progress sample.",
                "Record opening needle count. No conductive thread, LEDs, or batteries at this table.",
            ],
            "flow": [
                ["0-2", "Name bag; review samples and needle rule", "Needle is in a hand or counted tray"],
                ["2-5", "Name a future need; sketch small symbol", "Reduce oversized ideas"],
                ["5-7", "Inspect blank; receive needle + floss", "Quarantine damage"],
                ["7-17", "Stitch gently; check front/back", "Stop forcing immediately"],
                ["17-20", "Show progress; secure/trim as directed", "Accept honest in-progress work"],
                ["20-23", "Save photo + meaning sentence", "Verify meaning is clear"],
                ["23-25", "Bag blank/grid/floss; return needle", "Recount before release"],
            ],
            "show": "Point to the need, symbol, and strongest stitch. Complete: 'My symbol represents ___ because ___.'",
            "fixes": [
                "Too large: stitch only the strongest feature.",
                "Tangle: let needle hang; shorten working floss.",
                "Blocked hole or damaged wood: stop and use a tested or paper backup.",
                "Time: photograph meaningful progress; bag work; return needle.",
            ],
            "stop": "Lost needle, cracked/splintered blank, blocked hole, or any stitch that requires force.",
        },
        {
            "title": "W2 - LED + Conductive-Thread Circuit Lab",
            "subtitle": "Prepared powered loop + short unpowered stitch practice.",
            "accent": CORAL,
            "fill": PALE_CORAL,
            "finish": "Make a prepared LED glow, trace the complete loop, and practice one safe unpowered connection.",
            "say": "Battery -> positive path -> LED -> negative path. Match + to + and - to -. Paths never touch.",
            "prep": [
                "Test one known-good prepared circuit per pair and mark actual polarity.",
                "Prepare safe open/reversed and crossing/loose-tail fault samples; short-risk samples remain unpowered.",
                "Stage loop visual, premarked felt, pre-threaded needles, known-good swaps, inspect bin, and count tray.",
                "Battery changes remain mentor-controlled. Decorative floss stays at the Stamp table.",
            ],
            "flow": [
                ["0-2", "Holder off; name battery, LED, + and -", "Count needles; state stop rules"],
                ["2-5", "Compare complete loop and path touch", "Never power a short example"],
                ["5-9", "Trace both paths; brief prepared test; off", "Approve steady-light test"],
                ["9-16", "Practice snug loops + flat stitches unpowered", "Coach short tails and separation"],
                ["16-19", "Partner-check both sides; diagnose fault", "Ask where path opens/reverses/crosses"],
                ["19-22", "Save photo + safety sentence", "Check concept, not polish"],
                ["22-25", "Power off; return needle/circuit", "Secure battery; recount"],
            ],
            "show": "Trace positive and negative paths without crossing. Complete: 'I prevented a short by ___.'",
            "fixes": [
                "Dark: switch/power, polarity, contact, then one known-good part.",
                "Flicker/pressure-dependent: power off; loose connection goes to inspect.",
                "Fuzzy bridge or paths touch: do not power; trim or rebuild.",
                "After 60-90 seconds: swap prepared circuit and protect learning time.",
            ],
            "stop": "Warmth, odor, damage, exposed crossing, touching paths, or a light that works only when squeezed.",
        },
        {
            "title": "W3 - micro:bit + MakeCode",
            "subtitle": "Prepared A/B/A+B starter on matched W-labeled equipment.",
            "accent": TEAL,
            "fill": PALE_TEAL,
            "finish": "Change and test one prepared program; explain button input and display output.",
            "say": "Button is the input. The event decides. The display is the output. Simulate -> download -> wait -> test.",
            "prep": [
                "Open and test the starter on every Windows laptop; stage offline files/screenshots.",
                "Match W board, USB data cable, battery holder, and bag. Keep every R board physically separate.",
                "Function-test A, B, A+B, reset, cable, port, and matched battery pair.",
                "Stage a known-good board, cable, laptop, and printed transfer sequence.",
            ],
            "flow": [
                ["0-2", "Match labels; battery off; choose roles", "Verify W board + matched set"],
                ["2-5", "Point to A, B, display, reset, P0, GND", "Name only today's parts"],
                ["5-9", "Test A, B, A+B in simulator", "All three work before editing"],
                ["9-14", "Change one icon/display choice; retest", "Preserve A+B clear/off"],
                ["14-19", "Download; wait until flashing ends", "Battery disconnected; no early unplug"],
                ["19-22", "USB off; battery on; test + reset", "Match physical behavior"],
                ["22-25", "Save evidence; power off; return kit", "Verify file and kit label"],
            ],
            "show": "Press one input and explain the output. Complete: 'When I press ___, the micro:bit ___.'",
            "fixes": [
                "No MICROBIT drive: reseat both ends; try known-good data cable/port.",
                "Old code: transfer did not finish or reached the wrong kit.",
                "Flashing: wait; never unplug.",
                "Unexpected R initials/firmware: quarantine; do not reassign casually.",
            ],
            "stop": "Battery connected during USB transfer, premature unplug, mismatched kit, damaged cable/board, or unexpected R firmware.",
        },
        {
            "title": "W4 - Prepared NeoPixel Preview",
            "subtitle": "Run and explain first. Code editing is optional after the core pass.",
            "accent": GOLD,
            "fill": PALE_GOLD,
            "finish": "Run and explain DIN, data direction, two power sources, shared ground, and A/B/A+B behavior.",
            "say": "P0 sends data into DIN. Positive power stays separate. Grounds join. Students never rebuild the harness.",
            "prep": [
                "Reliability-test every 10-12-pixel mentor-built system, harness, resistor, capacitor, and holder.",
                "Load A effect, B effect, A+B off, brightness 30-60; match every label.",
                "Inspect arrows, connector, heat-shrink, wire, coating, pixels, and batteries.",
                "Stage enlarged diagram, whole-system swap, and backup video. Students do not wear the system.",
            ],
            "flow": [
                ["0-3", "Both holders off; match labels; inspect", "Reject damage/mismatch"],
                ["3-7", "Trace P0 -> resistor -> DIN + power", "Check arrows/separate positives/shared ground"],
                ["7-11", "Pixels on, then micro:bit; test A/B/A+B", "Observe every pixel and off state"],
                ["11-15", "Observe pixel 0, direction, color, brightness", "Switch controller/tracer roles"],
                ["15-19", "Optional one color/pause change", "Core understanding stays first"],
                ["19-22", "Save photo + explanation", "Use whole-system backup, not rewire"],
                ["22-25", "A+B; micro:bit off; pixels off", "Verify both supplies off + inventory"],
            ],
            "show": "Point to DIN, pixel 0, both power sources, shared ground, and separate positive supplies.",
            "fixes": [
                "Dark: check pixel power, connector seating, and DIN direction; do not rewire.",
                "micro:bit works/pixels dark: check separate pixel supply.",
                "Flicker/random color: both off; technical mentor checks prepared harness.",
                "Partial strip: confirm pixel count; mark failure and swap whole system.",
            ],
            "stop": "Warmth, odor, bare wire, torn coating, damaged pixel, unstable flicker, or any request to alter the harness.",
        },
    ]

    for idx, station in enumerate(station_pages, start=4):
        draw_header(
            c,
            "Reusable Wearables station card",
            station["title"],
            station["subtitle"],
            idx,
            total,
            accent=station["accent"],
            footer_note="Print once, place in a sleeve, and keep at the station. Full mentor detail remains on the website.",
        )
        y = CONTENT_TOP
        draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 66, "Finish line", station["finish"], accent=station["accent"], fill=station["fill"], body_size=8.8)
        y -= 78
        draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 56, "Say", station["say"], accent=station["accent"], fill=WHITE, body_size=8.6)
        y -= 68
        y = section_title(c, "Before students", MARGIN, y, station["accent"])
        y = draw_bullets(c, station["prep"], MARGIN, y, PAGE_W - 2 * MARGIN, size=7.7, leading=9.6, gap=2, checkbox=True)
        y -= 4
        y = section_title(c, "Exact 25-minute flow", MARGIN, y, station["accent"])
        flow_data = [["Min.", "Student action", "Mentor gate"]] + station["flow"]
        y = draw_table(c, flow_data, MARGIN, y, [48, 264, 232], row_heights=[25] + [31] * 7, font_size=6.9, alignments={0: "center"})
        y -= 10
        draw_card(c, MARGIN, y, 330, 70, "Show me", station["show"], accent=TEAL, fill=PALE_TEAL, body_size=7.8)
        draw_card(c, MARGIN + 342, y, 202, 70, "Stop", station["stop"], accent=CORAL, fill=PALE_CORAL, body_size=7.4)
        y -= 82
        y = section_title(c, "Quick fixes", MARGIN, y, CORAL)
        draw_bullets(c, station["fixes"], MARGIN, y, PAGE_W - 2 * MARGIN, size=7.5, leading=9.2, gap=1)
        save_page(c)

    # Page 8 - Robotics identity and input
    draw_header(c, "Reusable Robotics lead card", "R1 + R2 - Identity, Reset, and Input", "Teams stay with one numbered kit; partners switch roles each transition.", 8, total, accent=TEAL, footer_note="Print once for the Robotics lead. Student teams record understanding in their two-sided passport.")
    y = CONTENT_TOP
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 62, "Roles", "Driver operates. Navigator reads the card, checks ports and safety, predicts, and records. Both partners explain. Switch roles at each transition.", accent=TEAL, fill=PALE_TEAL, body_size=8.6)
    y -= 76
    y = section_title(c, "Challenge 1 - 9:51-10:16", MARGIN, y, PURPLE)
    r1 = [
        ["Min.", "Team action", "Mentor checkpoint"],
        ["0-4", "Name Hummingbird, R micro:bit, BirdBlox, and power-off rule", "Correct system language"],
        ["4-8", "Match kit, iPad, three-word name/initials, and ports", "All labels agree"],
        ["8-14", "Power on; assigned device only; green dot; run R1", "Wrong-device command stopped"],
        ["14-20", "SAFE RESET; switch roles; repeat start/reset", "Both partners complete sequence"],
        ["20-25", "Save label photo + reset explanation", "Evidence box cleared"],
    ]
    y = draw_table(c, r1, MARGIN, y, [48, 300, 196], row_heights=[26] + [39] * 5, font_size=7.0, alignments={0: "center"})
    y -= 12
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 68, "SAFE RESET", "1. LED to 0%.   2. Servo to marked ready angle.   3. Stop program.   4. Disconnect BirdBlox.   5. Switch kit power off.", accent=CORAL, fill=PALE_CORAL, body_size=9)
    y -= 82
    y = section_title(c, "Challenge 2 - 10:19-10:44", MARGIN, y, TEAL)
    r2 = [
        ["Min.", "Team action", "Mentor checkpoint"],
        ["0-3", "Input reports information; code compares and decides", "Sensing is not acting"],
        ["3-8", "Reconnect; identify distance sensor + Sensor 1", "Correct device, type, port"],
        ["8-15", "Record far -> near -> far; change only distance", "Target centered; three real values"],
        ["15-20", "Choose threshold between observed ranges; predict trigger", "No copied/universal threshold"],
        ["20-25", "Explain room/placement effect; save evidence; reset", "Value changes for a reason"],
    ]
    draw_table(c, r2, MARGIN, y, [48, 300, 196], row_heights=[26] + [38] * 5, font_size=7.0, alignments={0: "center"})
    save_page(c)

    # Page 9 - outputs and interaction
    draw_header(c, "Reusable Robotics lead card", "R3 + R4 - Outputs and Interaction", "Use only identical prepared boards and mentor-marked servo angles.", 9, total, accent=PURPLE, footer_note="Students do not change wiring, firmware, batteries, terminals, or device assignments during this tour.")
    y = CONTENT_TOP
    y = section_title(c, "Challenge 3 - 10:47-11:12", MARGIN, y, PURPLE)
    r3 = [
        ["Min.", "Team action", "Mentor checkpoint"],
        ["0-4", "Identify LED 1, Servo 1, ports, and motion zone", "Rig secured; roles switched"],
        ["4-10", "Run LED at 0%, 50%, 100%, then 0%", "Correct port and safe-off"],
        ["10-16", "Run servo only between two marked safe angles", "Hands clear; stop strain/buzzing"],
        ["16-21", "Predict; run LED + servo together; switch explainer", "Two outputs observed"],
        ["21-25", "Save screenshot/note; SAFE RESET", "LED 0%; servo ready"],
    ]
    y = draw_table(c, r3, MARGIN, y, [48, 300, 196], row_heights=[26] + [39] * 5, font_size=7.0, alignments={0: "center"})
    y -= 16
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 62, "Say before Challenge 4", "IF the object is closer than our measured threshold, THEN the light turns on AND the pointer moves; OTHERWISE the light turns off AND the pointer returns to ready.", accent=TEAL, fill=PALE_TEAL, body_size=8.7)
    y -= 78
    y = section_title(c, "Challenge 4 - 11:15-11:40", MARGIN, y, TEAL)
    r4 = [
        ["Min.", "Team action", "Mentor checkpoint"],
        ["0-4", "Say full IF / THEN / AND / OTHERWISE rule", "Input, decision, two outputs, reset named"],
        ["4-10", "Load R4; confirm threshold, ports, safe angles", "No rewiring/unapproved angles"],
        ["10-17", "Test far -> near -> far; predict + record; switch role", "Three controlled trials"],
        ["17-21", "Change one approved variable; retest same condition", "One-variable discipline"],
        ["21-25", "Save screenshot/media; explain; SAFE RESET", "Evidence proves full interaction"],
    ]
    y = draw_table(c, r4, MARGIN, y, [48, 300, 196], row_heights=[26] + [39] * 5, font_size=7.0, alignments={0: "center"})
    y -= 14
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 62, "11:40-11:45", "Verify four evidence boxes, both names/contributions, SAFE RESET, disconnect/off, and complete numbered kit inventory.", accent=CORAL, fill=PALE_CORAL, body_size=8.7)
    save_page(c)

    # Page 10 - troubleshooting
    draw_header(c, "Reusable Robotics lead card", "Safe Rescue and Final Check", "Change one thing. Protect the timed learning. Swap a whole prepared set when needed.", 10, total, accent=CORAL, footer_note="An unresolved kit goes to INSPECT with its number and symptom. It never returns directly to student stock.")
    y = CONTENT_TOP
    trouble = [
        ["Observed", "Quick safe check", "Do not"],
        ["Wrong robot moves", "Stop both; disconnect/off; verify kit/name/initials; reconnect one at a time", "Do not keep testing"],
        ["Name missing / red dot", "Correct R board, power, Bluetooth, no other iPad connected", "Do not choose random device or reload firmware"],
        ["Sensor frozen", "Reset/off; Sensor 1 + sensor type; clear view; known-good swap", "Do not change several settings"],
        ["LED dark", "Reset/off; LED 1 + brightness above 0%; known-good swap", "Do not move prepared wiring"],
        ["Servo silent", "Reset/off; Servo 1 + prepared connection; known-good swap", "Do not force shaft"],
        ["Servo buzzes/stalls", "Power off immediately; clear obstruction; technical lead", "Do not continue powered"],
        ["Always true/false", "View real values; threshold between near/far; test parts separately", "Do not guess threshold"],
    ]
    y = draw_table(c, trouble, MARGIN, y, [118, 290, 136], row_heights=[28] + [50] * 7, font_size=6.9)
    y -= 16
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 78, "Universal stop conditions", "Power off before touching hardware. Stop for heat, odor, loose battery, damaged insulation, pinched wire, unstable rig, wrong device, buzzing/stall, forced motion, or an output that will not stop.", accent=CORAL, fill=PALE_CORAL, body_size=8.5)
    y -= 92
    y = section_title(c, "Final kit count", MARGIN, y, TEAL)
    draw_bullets(c, ["Controller", "R micro:bit", "Assigned iPad", "Power pack", "Distance sensor", "LED", "Position servo + pointer", "Labeled tray parts", "Saved BirdBlox file + evidence"], MARGIN, y, PAGE_W - 2 * MARGIN, size=7.6, leading=9.3, gap=1, checkbox=True)
    save_page(c)

    # Page 11 - reusable count sheet
    draw_header(c, "Reusable accountability sheet", "Needle, Tool, and Kit Count", "Print page 11 twice for needle stations; use the lower table for numbered kit issues.", 11, total, accent=GOLD, footer_note="Keep on a clipboard. Reuse in a sleeve. A count discrepancy stops movement until resolved.")
    y = CONTENT_TOP
    c.setFont("Helvetica", 9)
    c.setFillColor(INK)
    c.drawString(MARGIN, y, "Station: __________________________  Lead: __________________________  Date: __________")
    y -= 24
    count_data = [["Checkpoint", "Needles out", "Needles in", "Snips/tools", "Power off?", "Initials / note"]]
    for label in ["Opening", "10:16", "10:44", "11:12", "11:40", "Final 11:45"]:
        count_data.append([label, "", "", "", "Y / N", ""])
    y = draw_table(c, count_data, MARGIN, y, [72, 74, 74, 78, 70, 176], row_heights=[30] + [48] * 6, font_size=7.2, alignments={0: "center", 1: "center", 2: "center", 3: "center", 4: "center"})
    y -= 18
    y = section_title(c, "Inspect / missing record", MARGIN, y, CORAL)
    issue_data = [["Time", "Station / kit", "Item or symptom", "Safe state", "Owner / next action"]]
    for _ in range(5):
        issue_data.append(["", "", "", "", ""])
    y = draw_table(c, issue_data, MARGIN, y, [52, 98, 168, 92, 134], row_heights=[28] + [44] * 5, font_size=7.0)
    y -= 16
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 56, "Release rule", "Every needle is returned separately; every powered system is off; every numbered kit is complete or explicitly labeled INSPECT / MISSING with an owner.", accent=CORAL, fill=PALE_CORAL, body_size=8.4)
    save_page(c)
    finish_pdf(c)


STUDIO_FOOTER = "Studio-use only. Draw, circle, point, test, and explain. Honest 'not yet' is useful. No grade. No homework."


def draw_identity_line(c: canvas.Canvas, y: float, team: bool = False) -> float:
    c.setFillColor(INK)
    c.setFont("Helvetica", 8.5)
    label = "Team members" if team else "Name"
    c.drawString(MARGIN, y, f"{label}: " + "_" * (58 if team else 40))
    c.drawRightString(PAGE_W - MARGIN, y, "Date: __________")
    return y - 22


def draw_check_row(c: canvas.Canvas, labels: Sequence[str], x: float, y: float, size: float = 8.0) -> float:
    cursor = x
    c.setFont("Helvetica", size)
    c.setFillColor(INK)
    for label in labels:
        c.setStrokeColor(MID)
        c.rect(cursor, y - 4, 8, 8, stroke=1, fill=0)
        c.drawString(cursor + 13, y - 2, label)
        cursor += 16 + stringWidth(label, "Helvetica", size) + 12
    return y - 16


def draw_thumbnail(c: canvas.Canvas, number: int, x: float, y_top: float, width: float, height: float, accent=PURPLE) -> None:
    y = y_top - height
    c.setStrokeColor(LINE)
    c.setFillColor(WHITE)
    c.roundRect(x, y, width, height, 8, stroke=1, fill=1)
    c.setFillColor(accent)
    c.circle(x + 17, y_top - 17, 11, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(x + 17, y_top - 20, str(number))
    c.setStrokeColor(HexColor("#D7DCE4"))
    c.line(x + 10, y + 40, x + width - 10, y + 40)
    c.setFillColor(MID)
    c.setFont("Helvetica", 6.8)
    c.drawString(x + 10, y + 27, "It responds when...")
    c.line(x + 10, y + 14, x + width - 10, y + 14)


def build_wearables_student_sheets() -> None:
    c = new_pdf("September-14-Wearables-Studio-Sheets.pdf", "September 14 Wearables Studio Sheets")
    total = 4

    # Page 1 - Future Stamp and Circuit Lab
    draw_header(c, "September 14 wearables passport", "What I Can Make Happen", "Side 1 of the capability passport - carry this through the four studios.", 1, total, accent=PURPLE, footer_note=STUDIO_FOOTER)
    y = draw_identity_line(c, CONTENT_TOP)
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 54, "How to use this passport", "Try it, notice what happened, and show or explain one piece of evidence. A truthful 'not yet' helps us plan support.", accent=PURPLE, fill=PALE_PURPLE, body_size=8.2)
    y -= 70
    y = section_title(c, "1. Future Stamp - an idea can become a visible mark", MARGIN, y, PURPLE)
    y = draw_check_row(c, ["I tried it", "I can show it", "I want more practice"], MARGIN, y)
    y = draw_prompt(c, "My future statement", MARGIN, y, PAGE_W - 2 * MARGIN, 72, "Complete: In the future, I will use my ideas to...", accent=PURPLE, lines=2)
    y -= 12
    left = (PAGE_W - 2 * MARGIN - 12) / 2
    bottom_a = draw_prompt(c, "One design choice I made", MARGIN, y, left, 105, "Shape, word, symbol, size, or placement.", accent=PURPLE, lines=3)
    bottom_b = draw_prompt(c, "Evidence I can point to", MARGIN + left + 12, y, left, 105, "The printed mark, a test impression, or a change I made.", accent=PURPLE, lines=3)
    y = min(bottom_a, bottom_b) - 18
    y = section_title(c, "2. Circuit Lab - a complete path makes light", MARGIN, y, TEAL)
    y = draw_check_row(c, ["I made a complete path", "LED lit", "I found a break"], MARGIN, y)
    y = draw_prompt(c, "Draw the path", MARGIN, y, 265, 130, "Show battery +, conductive thread/tape, LED direction, and battery -.", accent=TEAL, lines=0)
    draw_prompt(c, "What changed when I tested?", MARGIN + 279, y + 130, 265, 130, "Circle or note: direction / contact / loose path / short circuit.", accent=TEAL, lines=4)
    y -= 14
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 54, "Quick safety check", "Battery stayed cool; power was removed before changing the path; needle and snips returned to the counted tray.", accent=CORAL, fill=PALE_CORAL, body_size=8.0)
    save_page(c)

    # Page 2 - micro:bit and NeoPixel
    draw_header(c, "September 14 wearables passport", "Inputs, Code, and Light Patterns", "Side 2 of the capability passport - explain what caused what.", 2, total, accent=TEAL, footer_note=STUDIO_FOOTER)
    y = draw_identity_line(c, CONTENT_TOP)
    y = section_title(c, "3. micro:bit - an input can trigger a response", MARGIN, y, TEAL)
    y = draw_check_row(c, ["Program ran", "Input worked", "I changed one thing"], MARGIN, y)
    rows = [
        ["I did...", "The micro:bit did...", "The block/code that caused it was..."],
        ["Pressed A / pressed B / shook / other", "", ""],
        ["Changed one block or value", "", ""],
    ]
    y = draw_table(c, rows, MARGIN, y, [150, 174, 220], row_heights=[30, 70, 70], font_size=7.3)
    y -= 14
    y = draw_prompt(c, "My IF / THEN explanation", MARGIN, y, PAGE_W - 2 * MARGIN, 64, "IF I ____________________, THEN the micro:bit ____________________.", accent=TEAL, lines=2)
    y -= 18
    y = section_title(c, "4. NeoPixel - code controls color, order, and timing", MARGIN, y, GOLD)
    y = draw_check_row(c, ["Pixels lit", "Pattern changed", "I safely reset"], MARGIN, y)
    rows = [
        ["Pattern I tested", "One variable I changed", "What I noticed"],
        ["Color / brightness / number / order / timing", "", ""],
        ["My second test", "", ""],
    ]
    y = draw_table(c, rows, MARGIN, y, [180, 174, 190], row_heights=[30, 68, 68], font_size=7.3)
    y -= 14
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 62, "Carry forward", "Star one capability you may use in a project: visible symbol / sewn circuit / physical input / programmed light pattern. Be ready to tell a mentor why.", accent=PURPLE, fill=PALE_PURPLE, body_size=8.4)
    save_page(c)

    # Page 3 - idea canvas
    draw_header(c, "September 14 wearables idea canvas", "Three Fast Ideas, Then Combine", "Sketch to think. These are possibilities, not promises or polished art.", 3, total, accent=PURPLE, footer_note=STUDIO_FOOTER)
    y = draw_identity_line(c, CONTENT_TOP)
    y = draw_prompt(c, "Future statement or message", MARGIN, y, PAGE_W - 2 * MARGIN, 66, "What do you want someone to notice, feel, understand, or do?", accent=PURPLE, lines=2)
    y -= 15
    y = section_title(c, "Make three noticeably different possibilities", MARGIN, y, PURPLE)
    gap = 10
    thumb_w = (PAGE_W - 2 * MARGIN - 2 * gap) / 3
    for idx in range(3):
        draw_thumbnail(c, idx + 1, MARGIN + idx * (thumb_w + gap), y, thumb_w, 190, accent=[PURPLE, TEAL, CORAL][idx])
    y -= 204
    y = draw_prompt(c, "Circle one idea - or combine parts", MARGIN, y, PAGE_W - 2 * MARGIN, 78, "I am choosing idea(s) ______ because the technology helps the message by...", accent=TEAL, lines=2)
    y -= 12
    choice = [
        ["Capability I might use", "What it would do for the person wearing or viewing it"],
        ["Stamp / circuit / micro:bit / NeoPixel", ""],
        ["A second capability, if useful", ""],
    ]
    y = draw_table(c, choice, MARGIN, y, [220, 324], row_heights=[30, 62, 62], font_size=7.4)
    y -= 14
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 52, "Studio rule", "A smaller idea that works safely is stronger than a crowded idea that cannot be tested.", accent=CORAL, fill=PALE_CORAL, body_size=8.4)
    save_page(c)

    # Page 4 - build map and conversation
    draw_header(c, "September 14 wearables idea canvas", "Map the Wearable Before Building", "Use simple labels and arrows. Your mentor conversation matters more than drawing skill.", 4, total, accent=TEAL, footer_note=STUDIO_FOOTER)
    y = draw_identity_line(c, CONTENT_TOP)
    y = section_title(c, "Placement map", MARGIN, y, TEAL)
    box_w = (PAGE_W - 2 * MARGIN - 12) / 2
    draw_prompt(c, "Shirt - front and inside", MARGIN, y, box_w, 245, "Draw outside view. Use a dotted line for battery, thread, or controller on the inside.", accent=TEAL, lines=0)
    draw_prompt(c, "Hat or alternate wearable - outside and inside", MARGIN + box_w + 12, y, box_w, 245, "Show where a person touches, sees, hears, or safely carries each part.", accent=TEAL, lines=0)
    y -= 260
    effects = [
        ["When this happens...", "The wearable will...", "So the audience understands/feels..."],
        ["Input, movement, button, time, or viewing", "Light, symbol, pattern, or other output", ""],
    ]
    y = draw_table(c, effects, MARGIN, y, [178, 178, 188], row_heights=[32, 78], font_size=7.2)
    y -= 14
    y = draw_prompt(c, "First prototype question", MARGIN, y, PAGE_W - 2 * MARGIN, 66, "What is the smallest test that would teach you something important?", accent=PURPLE, lines=2)
    y -= 12
    mentor = [
        ["Mentor conversation - not a score", "Circle or note"],
        ["I can explain the message and what the technology does.", "clear / talk again"],
        ["My placement protects comfort, movement, and battery access.", "safe start / revise"],
        ["My first test is small enough to finish and learn from.", "ready / make smaller"],
    ]
    draw_table(c, mentor, MARGIN, y, [410, 134], row_heights=[28, 36, 36, 36], font_size=7.4)
    save_page(c)
    finish_pdf(c)


def build_robotics_team_sheets() -> None:
    c = new_pdf("September-14-Robotics-Team-Studio-Sheets.pdf", "September 14 Robotics Team Studio Sheets")
    total = 4

    draw_header(c, "September 14 robotics passport", "Identity, Reset, and Input", "Team studio sheet - switch Driver and Navigator every challenge.", 1, total, accent=PURPLE, footer_note=STUDIO_FOOTER)
    y = draw_identity_line(c, CONTENT_TOP, team=True)
    y = draw_prompt(c, "Our numbered kit and device", MARGIN, y, PAGE_W - 2 * MARGIN, 58, "Kit ______  Robot/device name ______  Driver first ______  Navigator first ______", accent=PURPLE, lines=1)
    y -= 14
    y = section_title(c, "Challenge 1 - prove identity and safe reset", MARGIN, y, PURPLE)
    identity = [
        ["Predict", "Run", "Evidence", "Safe reset"],
        ["Which prepared output will respond?", "Trigger the mentor-approved test.", "Write or sketch what proved this is our robot.", "Output off / controller ready / roles switch"],
    ]
    y = draw_table(c, identity, MARGIN, y, [130, 130, 170, 114], row_heights=[30, 96], font_size=7.2)
    y -= 18
    y = section_title(c, "Challenge 2 - measure an input before choosing a threshold", MARGIN, y, TEAL)
    sensor = [
        ["Condition", "Prediction", "Actual sensor value", "Same unit?", "What we noticed"],
        ["Far", "", "", "Yes / fix", ""],
        ["Near", "", "", "Yes / fix", ""],
        ["Far again", "", "", "Yes / fix", ""],
    ]
    y = draw_table(c, sensor, MARGIN, y, [92, 112, 120, 72, 148], row_heights=[30, 50, 50, 50], font_size=7.1, alignments={3: "center"})
    y -= 14
    y = draw_prompt(c, "Our threshold and why", MARGIN, y, PAGE_W - 2 * MARGIN, 72, "A value between our near and far readings is ______ because...", accent=TEAL, lines=2)
    y -= 12
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 56, "Team checkpoint", "Both teammates can point to the real readings and explain why copying another team's threshold may not work.", accent=CORAL, fill=PALE_CORAL, body_size=8.2)
    save_page(c)

    draw_header(c, "September 14 robotics passport", "Outputs and a Full Interaction", "Use only mentor-marked ports, prepared connections, and safe servo angles.", 2, total, accent=TEAL, footer_note=STUDIO_FOOTER)
    y = draw_identity_line(c, CONTENT_TOP, team=True)
    y = section_title(c, "Challenge 3 - two different outputs", MARGIN, y, TEAL)
    outputs = [
        ["Output", "Prediction", "What we ran", "What actually happened", "Safe state"],
        ["LED", "", "0% -> 50% -> 100% -> 0%", "", "0%"],
        ["Servo", "", "Only the two marked safe angles", "", "Ready angle"],
        ["Together", "", "Predict, then run both", "", "Both reset"],
    ]
    y = draw_table(c, outputs, MARGIN, y, [72, 98, 142, 150, 82], row_heights=[30, 55, 55, 55], font_size=6.9)
    y -= 18
    y = section_title(c, "Challenge 4 - input -> decision -> two outputs -> reset", MARGIN, y, PURPLE)
    y = draw_prompt(c, "Say the rule before running it", MARGIN, y, PAGE_W - 2 * MARGIN, 76, "IF the object is ______ than ______, THEN the light ______ AND the pointer ______; OTHERWISE...", accent=PURPLE, lines=2)
    y -= 12
    trials = [
        ["Trial", "Object condition", "Prediction", "LED", "Servo/pointer", "Did reset work?"],
        ["1", "Far", "", "", "", ""],
        ["2", "Near", "", "", "", ""],
        ["3", "Far again", "", "", "", ""],
    ]
    y = draw_table(c, trials, MARGIN, y, [42, 100, 108, 84, 120, 90], row_heights=[30, 48, 48, 48], font_size=7.0, alignments={0: "center"})
    y -= 14
    y = draw_prompt(c, "Change one approved variable, then retest", MARGIN, y, PAGE_W - 2 * MARGIN, 72, "We changed only ______. We held ______ the same. The result was...", accent=CORAL, lines=2)
    y -= 12
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 58, "Final proof", "Both teammates can explain the input, threshold decision, two outputs, and what the system does when the condition is false.", accent=TEAL, fill=PALE_TEAL, body_size=8.2)
    save_page(c)

    draw_header(c, "September 14 robotics idea canvas", "Three Interactions Worth Discussing", "Each idea needs an input, a decision, an output, and a reason people would care.", 3, total, accent=PURPLE, footer_note=STUDIO_FOOTER)
    y = draw_identity_line(c, CONTENT_TOP, team=True)
    y = draw_prompt(c, "Problem, delight, or future possibility", MARGIN, y, PAGE_W - 2 * MARGIN, 62, "Who is the interaction for, and what should be easier, safer, clearer, or more interesting?", accent=PURPLE, lines=2)
    y -= 15
    y = section_title(c, "Sketch three different IF / THEN systems", MARGIN, y, PURPLE)
    gap = 10
    thumb_w = (PAGE_W - 2 * MARGIN - 2 * gap) / 3
    for idx in range(3):
        draw_thumbnail(c, idx + 1, MARGIN + idx * (thumb_w + gap), y, thumb_w, 185, accent=[PURPLE, TEAL, CORAL][idx])
    y -= 199
    idea_rows = [
        ["Idea", "Input", "Decision / threshold", "Output(s)", "Why it matters"],
        ["1", "", "", "", ""],
        ["2", "", "", "", ""],
        ["3", "", "", "", ""],
    ]
    y = draw_table(c, idea_rows, MARGIN, y, [42, 102, 128, 116, 156], row_heights=[30, 46, 46, 46], font_size=6.8, alignments={0: "center"})
    y -= 14
    draw_prompt(c, "Choose or combine", MARGIN, y, PAGE_W - 2 * MARGIN, 74, "We want to explore idea(s) ______ because the interaction would...", accent=TEAL, lines=2)
    save_page(c)

    draw_header(c, "September 14 robotics idea canvas", "Map the System and First Test", "Build the smallest safe interaction that can answer one useful question.", 4, total, accent=TEAL, footer_note=STUDIO_FOOTER)
    y = draw_identity_line(c, CONTENT_TOP, team=True)
    map_rows = [
        ["INPUT", "DECISION", "OUTPUT 1", "OUTPUT 2", "OTHERWISE / RESET"],
        ["What changes in the world?", "What condition or threshold?", "What happens?", "What else happens?", "How does it return safely?"],
        ["", "", "", "", ""],
    ]
    y = draw_table(c, map_rows, MARGIN, y, [105, 112, 105, 105, 117], row_heights=[30, 42, 78], font_size=6.9, alignments={0: "center", 1: "center", 2: "center", 3: "center", 4: "center"})
    y -= 16
    y = section_title(c, "Three-frame interaction storyboard", MARGIN, y, PURPLE)
    frame_w = (PAGE_W - 2 * MARGIN - 20) / 3
    for idx, label in enumerate(["BEFORE", "TRIGGER", "RESPONSE + RESET"]):
        x = MARGIN + idx * (frame_w + 10)
        draw_prompt(c, label, x, y, frame_w, 150, "Show person, sensor/input, and visible result.", accent=PURPLE, lines=0)
    y -= 164
    y = draw_prompt(c, "First prototype question", MARGIN, y, PAGE_W - 2 * MARGIN, 62, "Can we prove that ______ causes ______ safely and repeatably?", accent=TEAL, lines=2)
    y -= 12
    roles = [
        ["First build roles", "Names / contribution"],
        ["Hardware guardian", ""],
        ["Coder / logic explainer", ""],
        ["Test and evidence lead", ""],
    ]
    y = draw_table(c, roles, MARGIN, y, [210, 334], row_heights=[28, 35, 35, 35], font_size=7.3)
    y -= 12
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 55, "Mentor conversation - not a score", "Circle together: system is explainable / needs another conversation; safe first test / make smaller; ready to prototype / repair plan first.", accent=CORAL, fill=PALE_CORAL, body_size=8.0)
    save_page(c)
    finish_pdf(c)


def build_engineering_workday_log() -> None:
    c = new_pdf("Reusable-Engineering-Workday-Log.pdf", "Reusable Engineering Workday Conversation Mat")
    total = 2
    footer = "Reusable studio mat. Place in a dry-erase sleeve. This thinking surface stays in the studio; it is not homework."

    draw_header(c, "Reusable project conversation mat", "Start Small, Test Three Times", "Front - a five-minute team huddle before tools, code, or materials move.", 1, total, accent=TEAL, footer_note=footer)
    y = CONTENT_TOP
    c.setFont("Helvetica", 8.5)
    c.setFillColor(INK)
    c.drawString(MARGIN, y, "Project/team: " + "_" * 36)
    c.drawRightString(PAGE_W - MARGIN, y, "Workday: __________")
    y -= 22
    y = draw_prompt(c, "Today's smallest useful goal", MARGIN, y, PAGE_W - 2 * MARGIN, 70, "By the end of this work block, we will be able to show...", accent=TEAL, lines=2)
    y -= 12
    half = (PAGE_W - 2 * MARGIN - 12) / 2
    a = draw_prompt(c, "Good enough is observable", MARGIN, y, half, 74, "What will a person see, hear, measure, or repeat?", accent=PURPLE, lines=2)
    b = draw_prompt(c, "Stop condition", MARGIN + half + 12, y, half, 74, "When do we stop, power down, or ask a mentor?", accent=CORAL, lines=2)
    y = min(a, b) - 14
    roles = [
        ["Role for this test", "Person", "What they protect"],
        ["Builder / hardware guardian", "", "Safe connections, movement, count"],
        ["Coder / settings guardian", "", "One controlled change"],
        ["Tester / evidence lead", "", "Same condition, honest record"],
    ]
    y = draw_table(c, roles, MARGIN, y, [180, 126, 238], row_heights=[28, 38, 38, 38], font_size=7.3)
    y -= 16
    y = section_title(c, "Three controlled trials", MARGIN, y, TEAL)
    trials = [
        ["Trial", "Condition we kept the same", "Prediction", "What happened / measured", "Pass?"],
        ["1", "", "", "", "Y / N"],
        ["2", "", "", "", "Y / N"],
        ["3", "", "", "", "Y / N"],
    ]
    y = draw_table(c, trials, MARGIN, y, [46, 166, 110, 160, 62], row_heights=[30, 64, 64, 64], font_size=7.1, alignments={0: "center", 4: "center"})
    y -= 14
    draw_prompt(c, "The pattern we see", MARGIN, y, PAGE_W - 2 * MARGIN, 66, "Across the three trials, the evidence suggests...", accent=PURPLE, lines=2)
    save_page(c)

    draw_header(c, "Reusable project conversation mat", "Change One Thing, Then Close Safely", "Back - use evidence to choose the next move and leave a clean restart.", 2, total, accent=PURPLE, footer_note=footer)
    y = CONTENT_TOP
    y = draw_prompt(c, "One variable we will change", MARGIN, y, PAGE_W - 2 * MARGIN, 68, "We will change only ______ because our evidence suggests...", accent=PURPLE, lines=2)
    y -= 12
    halves = (PAGE_W - 2 * MARGIN - 12) / 2
    a = draw_prompt(c, "What stays the same", MARGIN, y, halves, 82, "Same test condition, code, placement, power, timing, or material.", accent=TEAL, lines=2)
    b = draw_prompt(c, "Retest result", MARGIN + halves + 12, y, halves, 82, "Better / same / worse / new problem - and what proves it?", accent=TEAL, lines=2)
    y = min(a, b) - 14
    evidence = [
        ["Evidence saved", "Filename / location / person responsible"],
        ["Photo or short video", ""],
        ["Code / settings / measurement", ""],
        ["Design note or labeled sketch", ""],
    ]
    y = draw_table(c, evidence, MARGIN, y, [206, 338], row_heights=[28, 34, 34, 34], font_size=7.1)
    y -= 12
    y = section_title(c, "Safe close before the team leaves", MARGIN, y, CORAL)
    close_rows = [
        ["Check", "Done / note", "Check", "Done / note"],
        ["Power off / battery safe", "", "Needles, tools, loose parts counted", ""],
        ["Moving parts parked", "", "Damaged or uncertain item labeled", ""],
        ["Files named and saved", "", "Work stored for a clean restart", ""],
    ]
    y = draw_table(c, close_rows, MARGIN, y, [142, 130, 142, 130], row_heights=[26, 34, 34, 34], font_size=6.8)
    y -= 10
    y = draw_prompt(c, "Next five-minute action", MARGIN, y, PAGE_W - 2 * MARGIN, 54, "When we return, the first person will ______ using ______.", accent=TEAL, lines=1)
    y -= 10
    status = [
        ["Mentor conversation - circle one", "What must be true next time?"],
        ["READY TO CONTINUE / REPAIR FIRST / MENTOR HOLD / READY TO SHARE", ""],
    ]
    draw_table(c, status, MARGIN, y, [330, 214], row_heights=[26, 42], font_size=6.9)
    save_page(c)
    finish_pdf(c)


def build_lunch_checkpoint_tracker() -> None:
    c = new_pdf("Mentor-Lunch-Checkpoint-Tracker.pdf", "Mentor Lunch Checkpoint Tracker")
    total = 5
    footer = "Mentor clipboard tool. Ask, listen, point to evidence, and set one next action. No student homework is created."

    checkpoint_pages = [
        (
            "October 21 - Launch Pulse",
            "Can each team name its user, intended interaction, smallest first test, and safe starting point?",
            ["Project / team", "User + need", "Smallest test", "Owner before next work block", "Status"],
            [150, 110, 118, 108, 58],
            "READY / MAKE SMALLER / SAFETY TALK / NEEDS MENTOR MATCH",
            PURPLE,
        ),
        (
            "December 2 - Project Rescue",
            "What is actually working now, what evidence exists, and what must be cut or repaired?",
            ["Project / team", "Working evidence", "Current blocker", "One rescue move", "Status"],
            [150, 112, 112, 112, 58],
            "CONTINUE / CUT SCOPE / REPAIR FIRST / TECH LEAD",
            CORAL,
        ),
        (
            "January 13 - Clean Restart",
            "Can the team restart from saved evidence without reconstructing the whole project?",
            ["Project / team", "File / stored build", "First five-minute action", "Who begins", "Status"],
            [150, 120, 132, 84, 58],
            "READY / FIND EVIDENCE / REPAIR / REMAP ROLES",
            TEAL,
        ),
        (
            "February 10 - Reliability + Backup",
            "What works repeatedly, what still fails, and what can visitors experience if the main interaction fails?",
            ["Project / team", "Repeated proof", "Known failure", "Safe backup", "Status"],
            [150, 110, 106, 120, 58],
            "GALA PATH / MORE TRIALS / BACKUP FIRST / DISPLAY ONLY",
            GOLD,
        ),
    ]

    for page_num, (title, question, headers, widths, legend, accent) in enumerate(checkpoint_pages, start=1):
        draw_header(c, "Low-paper lunch checkpoint", title, "Print only this event page; one reusable clipboard copy per mentor table.", page_num, total, accent=accent, footer_note=footer)
        y = CONTENT_TOP
        draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 70, "Two-minute conversation", question, accent=accent, fill=PALE_PURPLE if accent == PURPLE else PALE_TEAL if accent == TEAL else PALE_CORAL if accent == CORAL else PALE_GOLD, body_size=8.7)
        y -= 86
        data = [headers]
        for _ in range(8):
            data.append(["", "", "", "", ""])
        y = draw_table(c, data, MARGIN, y, widths, row_heights=[34] + [54] * 8, font_size=6.8)
        y -= 14
        draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 64, "Status key", legend + ". Status is a coaching signal, not a grade.", accent=accent, fill=PALE_GRAY, body_size=8.2)
        save_page(c)

    draw_header(c, "Optional cut-apart studio tool", "Next-Action Project Bookmarks", "Print on cardstock only when a project needs a physical restart cue; cut on dotted lines.", 5, total, accent=PURPLE, footer_note="These stay with studio projects. They are not take-home tasks, grades, or homework.")
    top = CONTENT_TOP
    card_h = 147
    for idx in range(4):
        row = idx // 2
        col = idx % 2
        x = MARGIN + col * 278
        y_top = top - row * (card_h + 14)
        c.setDash(3, 3)
        c.setStrokeColor(MID)
        c.roundRect(x, y_top - card_h, 266, card_h, 8, stroke=1, fill=0)
        c.setDash()
        c.setFillColor(PURPLE)
        c.rect(x, y_top - 7, 266, 7, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 12, y_top - 25, "NEXT FIVE-MINUTE ACTION")
        c.setFont("Helvetica", 7.3)
        c.drawString(x + 12, y_top - 42, "Project: ______________________________")
        c.drawString(x + 12, y_top - 59, "First person: __________________________")
        c.drawString(x + 12, y_top - 76, "Use / open: ____________________________")
        c.drawString(x + 12, y_top - 93, "Do this first: __________________________")
        c.drawString(x + 12, y_top - 110, "Stop and ask if: ________________________")
        c.setFont("Helvetica-Oblique", 6.8)
        c.setFillColor(MID)
        c.drawString(x + 12, y_top - 130, "Leave with the project in the studio - not homework.")
    y = top - 2 * (card_h + 14) - 6
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 88, "Mentor use", "Write the cue with the team during the lunch conversation. Place it inside the project bin, on the sleeve, or beside the saved-device label so the next workday begins with action instead of recall.", accent=TEAL, fill=PALE_TEAL, body_size=8.5)
    save_page(c)
    finish_pdf(c)


def build_gala_readiness_pack() -> None:
    c = new_pdf("Gala-Readiness-Studio-Pack.pdf", "Gala Readiness Studio Pack")
    total = 5
    footer = "Studio safety and readiness check. Complete with a mentor during Femineers time. No grade. No homework."

    draw_header(c, "Gala readiness - wearables", "Wearable Safety and Experience Check", "One copy per wearable project; mentor and student inspect together.", 1, total, accent=PURPLE, footer_note=footer)
    y = CONTENT_TOP
    y = draw_identity_line(c, y, team=True)
    checks = [
        ["Inspect together", "PASS", "FIX", "DISPLAY ONLY", "Evidence / action"],
        ["Power source secure, accessible, cool, and removable", "", "", "", ""],
        ["Conductive paths covered; no loose strands or short-circuit risk", "", "", "", ""],
        ["Needles and temporary sharp tools fully removed and counted", "", "", "", ""],
        ["Controller, LEDs, and wiring protected from pull and movement", "", "", "", ""],
        ["Comfort and fit checked with safe motion; no pinching or hot spots", "", "", "", ""],
        ["Main interaction can be explained and safely turned off", "", "", "", ""],
        ["Visitor touch point and mentor supervision are clear", "", "", "", ""],
        ["Display-only version still communicates the project's idea", "", "", "", ""],
    ]
    y = draw_table(c, checks, MARGIN, y, [250, 46, 46, 72, 130], row_heights=[34] + [54] * 8, font_size=6.9, alignments={1: "center", 2: "center", 3: "center"})
    y -= 14
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 62, "Release decision", "Circle one: PASS FOR WEAR / FIX BEFORE RECHECK / DISPLAY ONLY. Mentor initials ______  Student initials ______", accent=CORAL, fill=PALE_CORAL, body_size=8.2)
    save_page(c)

    draw_header(c, "Gala readiness - robotics", "Robotics Safety and Experience Check", "One copy per robotics project; verify safe motion, repeatability, and control.", 2, total, accent=TEAL, footer_note=footer)
    y = CONTENT_TOP
    y = draw_identity_line(c, y, team=True)
    checks = [
        ["Inspect together", "PASS", "FIX", "MODIFIED DEMO", "Evidence / action"],
        ["Base and moving parts secured; reach and pinch zones marked", "", "", "", ""],
        ["Batteries, terminals, and wires protected and accessible to mentor", "", "", "", ""],
        ["Servo/motor limits do not strain, buzz, stall, or strike objects", "", "", "", ""],
        ["Correct device connects reliably; wrong-device risk is controlled", "", "", "", ""],
        ["Input threshold works in the actual Gala placement and lighting", "", "", "", ""],
        ["Outputs stop and reset safely when condition is false", "", "", "", ""],
        ["Visitor boundary, touch point, and stop control are clear", "", "", "", ""],
        ["Modified demo still proves the central interaction safely", "", "", "", ""],
    ]
    y = draw_table(c, checks, MARGIN, y, [234, 46, 46, 88, 130], row_heights=[34] + [54] * 8, font_size=6.8, alignments={1: "center", 2: "center", 3: "center"})
    y -= 14
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 62, "Release decision", "Circle one: PASS FOR LIVE DEMO / FIX BEFORE RECHECK / MODIFIED DEMO. Mentor initials ______  Team initials ______", accent=CORAL, fill=PALE_CORAL, body_size=8.1)
    save_page(c)

    draw_header(c, "Gala readiness - all projects", "Two-Trial Reliability and Safe Backup", "Run in the real setup. A safe backup is part of good engineering, not a failure.", 3, total, accent=PURPLE, footer_note=footer)
    y = CONTENT_TOP
    y = draw_identity_line(c, y, team=True)
    y = draw_prompt(c, "What a visitor will do and experience", MARGIN, y, PAGE_W - 2 * MARGIN, 62, "In one sentence: A visitor will ______ and the project will ______.", accent=PURPLE, lines=1)
    y -= 10
    trials = [
        ["Real-setup trial", "Starting condition", "Visitor action / input", "Observed response", "Reset safe?", "Pass?"],
        ["1", "", "", "", "Y / N", "Y / N"],
        ["2", "", "", "", "Y / N", "Y / N"],
    ]
    y = draw_table(c, trials, MARGIN, y, [62, 108, 130, 130, 62, 52], row_heights=[30, 64, 64], font_size=6.9, alignments={0: "center", 4: "center", 5: "center"})
    y -= 12
    y = draw_prompt(c, "Known failure or uncertainty", MARGIN, y, PAGE_W - 2 * MARGIN, 60, "If ______ happens, stop / reset / ask a mentor by...", accent=CORAL, lines=1)
    y -= 10
    y = draw_prompt(c, "Safe backup experience", MARGIN, y, PAGE_W - 2 * MARGIN, 68, "Without unsafe improvising, visitors can still understand or experience the idea through...", accent=TEAL, lines=2)
    y -= 10
    backup = [
        ["Backup pieces ready", "Location / owner"],
        ["Photo, video, storyboard, sample, or manual demonstration", ""],
        ["Sign or exact words explaining the modified experience", ""],
    ]
    y = draw_table(c, backup, MARGIN, y, [310, 234], row_heights=[28, 38, 38], font_size=7.0)
    y -= 10
    draw_card(c, MARGIN, y, PAGE_W - 2 * MARGIN, 48, "Mentor release", "Circle one: LIVE EXPERIENCE / MODIFIED EXPERIENCE / DISPLAY ONLY / HOLD FOR REPAIR. Initials ______", accent=PURPLE, fill=PALE_PURPLE, body_size=7.8)
    save_page(c)

    draw_header(c, "Gala public-facing tool", "Project Story Card", "Write for a visitor: large, brief, human, and free of unexplained technical words.", 4, total, accent=GOLD, footer_note="Complete in the studio. Display at the Gala; this is not a graded assignment or homework.")
    y = CONTENT_TOP
    y = draw_prompt(c, "PROJECT TITLE", MARGIN, y, PAGE_W - 2 * MARGIN, 70, "Short enough to read from a few feet away.", accent=GOLD, lines=2)
    y -= 14
    y = draw_prompt(c, "WE IMAGINED...", MARGIN, y, PAGE_W - 2 * MARGIN, 102, "What future, need, delight, or question inspired the project?", accent=PURPLE, lines=3)
    y -= 14
    y = draw_prompt(c, "TRY / NOTICE...", MARGIN, y, PAGE_W - 2 * MARGIN, 102, "What may a visitor safely do? What response should they notice?", accent=TEAL, lines=3)
    y -= 14
    y = draw_prompt(c, "THE ENGINEERING IDEA...", MARGIN, y, PAGE_W - 2 * MARGIN, 102, "Explain the input, decision, circuit, code, structure, or output in plain language.", accent=PURPLE, lines=3)
    y -= 14
    y = draw_prompt(c, "WE LEARNED...", MARGIN, y, PAGE_W - 2 * MARGIN, 90, "One test, change, surprise, or repair that made the project stronger.", accent=CORAL, lines=3)
    y -= 14
    c.setFont("Helvetica", 8.5)
    c.setFillColor(INK)
    c.drawString(MARGIN, y, "Creators: " + "_" * 54)
    c.drawRightString(PAGE_W - MARGIN, y, "Pathway: Wearables / Robotics")
    save_page(c)

    draw_header(c, "Gala logistics tool", "Setup, Packdown, and Transport Tag", "Keep the upper checklist with the project bin; cut and attach the lower tag.", 5, total, accent=CORAL, footer_note="Studio logistics tool. Adults retain accountability for batteries, sharps, powered systems, and transport.")
    y = CONTENT_TOP
    y = draw_identity_line(c, y, team=True)
    setup = [
        ["SETUP ORDER", "Person / note", "PACKDOWN ORDER", "Person / note"],
        ["1. Place base/display and mark visitor boundary", "", "1. Stop interaction and power off", ""],
        ["2. Secure hardware/wearable and inspect damage", "", "2. Remove/secure battery and power source", ""],
        ["3. Connect only labeled prepared power/device", "", "3. Count tools, sharps, controllers, loose parts", ""],
        ["4. Run one real-placement safety trial", "", "4. Save evidence; label repair/inspect items", ""],
        ["5. Place story card, backup, and stop instructions", "", "5. Pack in labeled order and sign transport tag", ""],
    ]
    y = draw_table(c, setup, MARGIN, y, [164, 108, 164, 108], row_heights=[32] + [53] * 5, font_size=6.8)
    y -= 18
    c.setDash(4, 3)
    c.setStrokeColor(MID)
    c.roundRect(MARGIN, y - 220, PAGE_W - 2 * MARGIN, 220, 8, stroke=1, fill=0)
    c.setDash()
    c.setFillColor(CORAL)
    c.rect(MARGIN, y - 7, PAGE_W - 2 * MARGIN, 7, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 14, y - 28, "CUT-APART PROJECT TRANSPORT TAG")
    tag_lines = [
        "Project / pathway: _________________________________________________",
        "Bin / case number: __________  Stored at: ____________________________",
        "Power source removed or secured by: _________________________________",
        "Fragile / moving / sharp / inspect notes: ____________________________",
        "Setup first action: __________________________________________________",
        "Adult release out: __________________  Adult receipt in: ______________",
    ]
    yy = y - 50
    c.setFont("Helvetica", 8.5)
    for line in tag_lines:
        c.drawString(MARGIN + 14, yy, line)
        yy -= 25
    save_page(c)
    finish_pdf(c)


def main() -> None:
    builders = [
        build_sept14_mentor_pack,
        build_wearables_student_sheets,
        build_robotics_team_sheets,
        build_engineering_workday_log,
        build_lunch_checkpoint_tracker,
        build_gala_readiness_pack,
    ]
    expected = [
        "September-14-Mentor-and-Station-Pack.pdf",
        "September-14-Wearables-Studio-Sheets.pdf",
        "September-14-Robotics-Team-Studio-Sheets.pdf",
        "Reusable-Engineering-Workday-Log.pdf",
        "Mentor-Lunch-Checkpoint-Tracker.pdf",
        "Gala-Readiness-Studio-Pack.pdf",
    ]
    for builder in builders:
        builder()
    for filename in expected:
        path = OUT / filename
        if not path.exists() or path.stat().st_size < 1000:
            raise RuntimeError(f"PDF was not created correctly: {path}")
        print(path)


if __name__ == "__main__":
    main()
