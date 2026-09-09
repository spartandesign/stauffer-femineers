"""Build the curriculum entry pages and consistent, JavaScript-independent navigation.

Run after changing the data below. Existing lesson bodies and their URLs are retained.
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parents[1]

# Date labels and curriculum links are shared by the student and mentor entry pages.
SESSIONS = [
    dict(id="september-24", date="September 24, 2026", kind="Workday · Phase 1", title="Explore & plan", guide="start-here.html", mentor="mentor-lesson-plans.html#day-1", evidence="canvas-checkpoint-1.html", evidence_label="Checkpoint 1: approved proposal", goal="Save your technology explorations and an approved proposal or documented revision plan.", w="wearable-design-proposal.html", r="robotics-design-proposal.html", w_task="Explore your materials, brainstorm three ideas, and plan the LED shirt and programmable hat.", r_task="Explore the Hummingbird, brainstorm three ideas, and explain your invention’s input, two outputs, and reset.", prepare="Assign the six home tables; stage samples, tested equipment, and the studio sheets.", j="Guide the 18 Wearables students through exploration and individual proposals.", s="Guide nine Robotics pairs through their kit explorations and team proposals.", t="Lead technical demonstrations, support equipment, and resolve safety or programming questions."),
    dict(id="october-13", date="October 13, 2026", kind="District kickoff · Griffiths", title="Glow Up Your Badge", guide="glow-up-your-badge.html", mentor="mentor-lesson-plans.html#kickoff-badge", evidence="glow-up-your-badge.html#reflect", evidence_label="Kickoff photo reflection", goal="Make the released badge design and explain how its circuit works. Complete the reflection in the scheduled school-time window.", prepare="Complete the physical prototype, novice timing, safety check, and mentor rehearsal before releasing kits.", j="Support personalization, attachment, and the finished-badge check.", s="Support student flow, explanations, and the station reset.", t="Release the tested circuit and model troubleshooting with known-good parts."),
    dict(id="october-21", date="October 21, 2026", kind="Lunch checkpoint · Phase 2", title="Arrive ready to build", guide="phase-2-prototype.html", mentor="mentor-lesson-plans.html#day-2", evidence="phase-2-prototype.html#submit", evidence_label="Design Ready package · October 19", goal="Submit the design package October 19; demonstrate it at lunch October 21 and record your next action.", w="wearable-design-proposal.html", r="robotics-design-proposal.html", w_task="Complete labeled shirt and hat plans, circuits, materials, and your first test plan.", r_task="Complete the labeled invention, input/output system, storyboard, materials, and first test plan.", prepare="Review October 19 evidence on October 20 and stage the status tracker.", j="Check each Wearables plan for a buildable system and clear first test.", s="Check each team’s interaction and both partners’ understanding.", t="Resolve technical and fabrication questions; record green, yellow, or red status."),
    dict(id="november-16", date="November 16, 2026", kind="Workday · Phase 3", title="Prototype & build", guide="phase-3-build.html", mentor="mentor-lesson-plans.html#day-3", evidence="build-progress-evidence.html", evidence_label="Checkpoint 2: prototype & build progress", goal="Test a small prototype, use the result to guide construction, and save the build evidence.", w="wearable-build.html", r="robotics-build.html", w_task="Test the planned paint, circuit, and pixel questions, then begin the approved shirt construction.", r_task="Test your structure and interaction, then build the approved physical system.", prepare="Rehearse the working examples and prepare the approved materials and reusable workday logs.", j="Guide painting and sewn-circuit construction after prototype evidence is reviewed.", s="Guide structures, mechanisms, role switching, and the first programmed interaction.", t="Clear technical gates, troubleshoot one variable at a time, and protect repair access."),
    dict(id="december-2", date="December 2, 2026", kind="Support lunch · By invitation", title="Project Rescue", guide="lunch-checkpoints.html#december-rescue", mentor="mentor-lesson-plans.html#december-2-rescue", evidence="lunch-checkpoints.html#december-rescue", evidence_label="Record one December 7 starting action", goal="Use existing evidence to identify the blocker and leave with one safe starting action. No construction or homework.", prepare="Invite the projects that need a decision and prefill their existing evidence and tracker rows.", j="Conference with invited Wearables projects and narrow each blocker.", s="Conference with invited Robotics teams and check both partners’ next roles.", t="Resolve unknown technical issues and choose continue, cut scope, repair first, or technical lead."),
    dict(id="december-7", date="December 7, 2026", kind="Workday · Phase 4", title="Build, test & store", guide="phase-4-test.html", mentor="mentor-lesson-plans.html#day-4", evidence="mid-build-evidence.html", evidence_label="Mid-build evidence & January restart plan", goal="Record a fair test and one improvement; label and store the project with a clear restart plan.", w="wearable-test.html", r="robotics-test.html", w_task="Test and repair the shirt, mock up hat mounting, and prepare safe winter storage.", r_task="Test subsystems, troubleshoot, and prepare the kit and code for January.", prepare="Stage the December Rescue starting actions, known-good examples, and labeled storage.", j="Guide shirt testing, repairs, mounting plans, and wearable storage.", s="Guide subsystem tests, team explanations, code backups, and kit inventory.", t="Use controlled troubleshooting and stop unresolved faults before storage."),
    dict(id="january-13", date="January 13, 2027", kind="Lunch checkpoint", title="Restart ready", guide="lunch-checkpoints.html#january", mentor="lunch-checkpoints.html#january", evidence="lunch-checkpoints.html#january", evidence_label="Restart status & three priorities", goal="Confirm project condition, code backup, materials, and the three priorities for January 25.", prepare="Review December evidence and stage the current lunch tracker.", j="Check Wearables condition, repair needs, and materials.", s="Check Robotics kit condition, code access, and partner priorities.", t="Identify equipment or programming blockers before the integration workday."),
    dict(id="january-25", date="January 25, 2027", kind="Workday · Phase 5", title="Integrate & redesign", guide="phase-5-integrate.html", mentor="mentor-lesson-plans.html#day-5", evidence="test-learn-redesign.html", evidence_label="Checkpoint 3: test, learn, redesign", goal="Integrate the complete system, compare a baseline and retest, and document a meaningful redesign.", w="wearable-integration.html", r="robotics-integration.html", w_task="Complete the shirt, integrate the removable hat electronics, and test comfort and programmed effects.", r_task="Connect the complete invention, test visitor interactions, and improve the system.", prepare="Stage January 13 priorities, tested systems, and the workday logs.", j="Guide shirt completion, hat mounting, comfort checks, and repair access.", s="Guide complete-system interactions, visitor trials, and team redesign decisions.", t="Check integration gates and compare the same test before and after a change."),
    dict(id="february-10", date="February 10, 2027", kind="Lunch checkpoint", title="Choose your Gala priorities", guide="lunch-checkpoints.html#february", mentor="lunch-checkpoints.html#february", evidence="lunch-checkpoints.html#february", evidence_label="Ranked punch list & project story", goal="Show test evidence, rank the final repairs, and practice the opening line of your project story.", prepare="Review January test evidence and stage the Gala-path tracker.", j="Prioritize wearable reliability, comfort, and fashion-show needs.", s="Prioritize interaction reliability, reset, and visitor experience.", t="Identify repairs and backup demonstrations that must be prepared before February 22."),
    dict(id="february-22", date="February 22, 2027", kind="Workday · Phase 6", title="Get Gala ready", guide="phase-6-gala-ready.html", mentor="mentor-lesson-plans.html#day-6", evidence="gala-ready-evidence.html", evidence_label="Checkpoint 4: Gala Ready", goal="Pass two reliability trials, rehearse the demonstration, and finish the project card, backup, and packing plan.", w="wearable-gala-ready.html", r="robotics-gala-ready.html", w_task="Inspect the outfit, test twice, rehearse wearing it, and prepare a backup and packing plan.", r_task="Inspect the invention, test twice, rehearse the gallery interaction, and pack the numbered kit.", prepare="Stage the February 10 punch lists, Gala inspection sheets, and backup examples.", j="Check wearable fit and safety, coach the fashion-show explanation, and confirm packing.", s="Check team reliability, visitor reset, presentation roles, and kit packing.", t="Resolve final technical faults and approve the appropriate backup or modified demonstration."),
    dict(id="march-1", date="March 1, 2027", kind="Showcase · Stauffer Library", title="Stauffer Gala", guide="program-roadmap.html", mentor="mentor-lesson-plans.html#day-6", evidence="gala-ready-evidence.html", evidence_label="Canvas: Stauffer Gala Reflection", goal="Present to real visitors, save evidence, and reflect on one improvement before the district celebration.", prepare="Use the February Gala-ready records to confirm transport, setup, and backup arrangements.", j="Support the Wearables fashion show and student explanations.", s="Support the Robotics gallery, resets, and partner participation.", t="Support reliable setup and record technical changes needed before the district event."),
    dict(id="march-18", date="March 18, 2027 · Evening", kind="Showcase · Downey High", title="District Femineers Gala", guide="program-roadmap.html", mentor="mentor-lesson-plans.html#day-6", evidence="gala-ready-evidence.html", evidence_label="Canvas: final portfolio & district reflection", goal="Present the polished project and complete the final portfolio and reflection in the scheduled Canvas window.", prepare="Confirm the district logistics and retest any changes made after the Stauffer Gala.", j="Support Wearables presentation, comfort, and packing.", s="Support Robotics demonstrations, both partners, and kit return.", t="Support technical readiness, backups, and final equipment inventory."),
]

TUTORIALS = {
    "Wearables": [
        ("wearable-technology.html", "Wearable Technology overview", "Shirt and hat requirements; four technology explorations."),
        ("stamp-from-the-future.html", "Stamp from the Future", "Ordinary floss, a wooden blank, and a symbol for your future idea."),
        ("sewable-led-basics.html", "Sewable LED basics", "Polarity, complete circuits, and a prepared LED test."),
        ("conductive-thread-basics.html", "Conductive thread basics", "Stitching paths, connections, and avoiding shorts."),
        ("meet-the-microbit.html", "micro:bit & MakeCode", "Windows laptops, buttons, events, and programming."),
        ("meet-the-neopixels.html", "NeoPixels", "Prepared wiring, separate power, shared ground, and effects."),
    ],
    "Creative Robotics": [
        ("creative-robotics.html", "Creative Robotics overview", "Teams of two, an input, two outputs, and a visitor interaction."),
        ("meet-the-hummingbird.html", "Hummingbird & BirdBlox", "Controller, sensors, LEDs, servos, Bluetooth, and official tutorials."),
        ("robotics-design-proposal.html", "Plan a Robotics invention", "Labeled sketch, storyboard, system, and partner responsibilities."),
    ],
    "Ideas, design & materials": [
        ("limitless-challenge.html", "The Limitless Challenge", "Find a future need and a meaningful project purpose."),
        ("idea-starters.html", "60 idea starters", "Search Robotics and Wearables concepts and personalize an idea."),
        ("design-process.html", "Engineering design process", "Imagine, plan, prototype, build, test, and improve."),
        ("wearable-design-proposal.html", "Plan your shirt & hat", "Sketches, circuits, programmed behaviors, and materials."),
        ("our-supplies.html", "Our supplies", "Program equipment, materials, and what each part does."),
        ("fabrication-lab.html", "Fabrication Lab", "Tinkercad, STL/SVG files, machine access, and custom-part requests."),
        ("glow-up-your-badge.html", "Glow Up Your Badge", "The separate October 13 district kickoff activity."),
    ],
    "Build, test & improve": [
        (f"{path}-{stage}.html", f"{label}: {name}", description)
        for path, label in [("wearable", "Wearables"), ("robotics", "Robotics")]
        for stage, name, description in [
            ("prototype", "prototype", "Small tests before permanent construction."),
            ("build", "major build", "Complete construction directions for November 16."),
            ("test", "test & repair", "December testing, troubleshooting, and winter storage."),
            ("integration", "integrate & redesign", "January complete-system tests and improvements."),
            ("gala-ready", "Gala readiness", "Inspection, reliability, rehearsal, backups, and packing."),
        ]
    ],
    "Evidence & mentor review": [
        ("capture-evidence.html", "Capture good evidence", "Clear photos, screenshots, videos, captions, and explanations."),
        ("mentor-approval.html", "Mentor approval", "Explain the plan and record an approval or revision decision."),
        ("canvas-checkpoint-1.html", "Checkpoint 1: proposal", "The complete first proposal submission checklist."),
        ("prototype-evidence.html", "Prototype evidence reference", "Questions, trial records, observations, and next steps."),
        ("build-progress-evidence.html", "Checkpoint 2: build progress", "Prototype findings and November construction evidence."),
        ("mid-build-evidence.html", "Mid-build evidence", "December tests and the January restart plan."),
        ("test-learn-redesign.html", "Checkpoint 3: test & redesign", "Baseline, one meaningful change, and a fair retest."),
        ("gala-ready-evidence.html", "Checkpoint 4: Gala Ready", "Reliability trials, project card, backup, and logistics."),
        ("lunch-checkpoints.html", "Lunch checkpoints", "Dates, demonstrations, status, and next actions."),
    ],
}

NAV = [("index.html", "Home"), ("my-project.html", "My Project"), ("tutorials.html", "Tutorials"), ("mentors.html", "Mentors")]
GENERATED = {"index.html", "my-project.html", "wearables-project.html", "robotics-project.html", "tutorials.html", "mentors.html", "404.html"}


def esc(value):
    return html.escape(str(value), quote=True)


def link(url, label, cls=""):
    return f'<a href="{esc(url)}"' + (f' class="{cls}"' if cls else '') + f'>{esc(label)}</a>'


def list_html(items):
    return '<ul>' + ''.join(f'<li>{item}</li>' for item in items) + '</ul>'


def category(filename):
    if filename in {"mentors.html", "mentor-lesson-plans.html", "mentor-print-center.html", "recruitment-toolkit.html"}:
        return "mentors.html"
    if filename in {"index.html", "recruitment.html", "student-application.html", "returning-member-confirmation.html", "teacher-recommendation.html", "family-commitment.html", "404.html"}:
        return "index.html"
    if filename == "tutorials.html" or filename in {p for group in TUTORIALS.values() for p, _, _ in group} and not filename.startswith(("wearable-", "robotics-")) and filename not in {"lunch-checkpoints.html", "mentor-approval.html", "canvas-checkpoint-1.html", "build-progress-evidence.html", "mid-build-evidence.html", "test-learn-redesign.html", "gala-ready-evidence.html"}:
        return "tutorials.html"
    return "my-project.html"


def header(filename):
    links = []
    for url, label in NAV:
        current = ' aria-current="page"' if filename == url else (' aria-current="location"' if category(filename) == url else '')
        links.append(f'<a href="{url}"{current}>{label}</a>')
    return '<a class="skip-link" href="#main-content">Skip to content</a>\n<header class="site-header"><div class="header-inner"><a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">L</span> Limitless</a><button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" hidden>Menu</button><nav class="site-nav" id="main-nav" aria-label="Main navigation">' + ''.join(links) + '</nav></div></header>'


def footer_nav():
    return '<nav class="footer-nav no-print" aria-label="Program information">' + ''.join(link(*item) for item in [("program-roadmap.html", "All dates"), ("recruitment.html", "About & joining"), ("family-commitment.html", "Family information"), ("mentors.html", "Mentor resources")]) + '</nav>'


def document(filename, title, body):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#5f3dc4"><meta name="description" content="{esc(title)} — Stauffer Femineers 2026–2027."><title>{esc(title)} | Limitless</title><link rel="stylesheet" href="assets/styles.css"></head>
<body>{header(filename)}
<main id="main-content">{body}</main>
<footer class="site-footer"><p><strong>Stauffer Femineers</strong></p><p>Imagine it. Build it. Become it.</p>{footer_nav()}</footer><script src="assets/site.js"></script></body></html>
'''


def hero(eyebrow, title, intro):
    return f'<section class="page-hero hub-hero"><p class="eyebrow">{esc(eyebrow)}</p><h1>{title}</h1><p class="lede">{intro}</p></section>'


def pathway_choices():
    return '<div class="hub-pathways">' + ''.join(
        f'<a class="choice-card {cls}" href="{url}"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2><p>{desc}</p><span class="card-link">Open my workdays →</span></a>'
        for cls, url, eyebrow, title, desc in [
            ("wearable", "wearables-project.html", "2nd year + 3rd-year choice", "Wearables", "18 students · Individual shirt-and-hat projects · Tables W1–W3 · Jennifer"),
            ("robotics", "robotics-project.html", "1st year + 3rd-year choice", "Creative Robotics", "18 students · Nine teams of two · Tables R1–R3 · Stephanie"),
        ]) + '</div>'


def home():
    body = hero("Stauffer Femineers · 2026–2027", 'Your next step<br>starts <span>here.</span>', 'Open your pathway, find the workday, and follow its checklist. Complete tutorials and examples are always available when you need to go deeper.')
    body += '<section class="section compact"><div class="next-session"><div><p class="eyebrow">First workday · Thursday, September 24</p><h2>Explore &amp; plan</h2><p>Room 14 · 8:00 a.m.–2:41 p.m. · 36 students · Six home tables</p><p>Snack 9:25–9:38 a.m. · Lunch 12:42–1:12 p.m.</p></div><div class="button-row">' + link("my-project.html", "Open my project", "button") + link("mentors.html#september-24", "Open the mentor plan", "button secondary") + '</div></div>'
    body += pathway_choices() + '</section>'
    body += '<section class="section compact"><div class="hub-links">' + link("tutorials.html", "Find a tutorial or example") + link("program-roadmap.html", "See every program date") + link("lunch-checkpoints.html", "Prepare for a lunch checkpoint") + '</div><details class="curriculum-detail" id="assigned-path"><summary>Pathway placement &amp; family commitment</summary><div class="detail-body"><p>First-year Femineers complete Creative Robotics in pairs. Second-year Femineers complete Wearables individually. Third-year Femineers choose either pathway; mentors confirm the final roster.</p><p>Five school-day work sessions take place in Room 14. Students and families arrange and complete all missed regular classwork.</p>' + link("family-commitment.html", "Read the complete family information", "button secondary") + '</div></details></section>'
    return body


def my_project():
    return hero("My Project", 'Choose your <span>pathway.</span>', 'Use the pathway on your roster. Each workday has a short starting checklist, full instructions, and an evidence finish line.') + '<section class="section compact">' + pathway_choices() + '<div class="callout teal"><strong>Know your home table:</strong> W1–W3 have six Wearables students each. R1–R3 have three Robotics pairs each. Equipment stays assigned to the table or team.</div><div class="hub-links">' + link("start-here.html", "New to Femineers? Read the full introduction") + link("tutorials.html", "Explore all tutorials") + link("program-roadmap.html", "Open the full roadmap") + '</div></section>'


def session_summary(s):
    return f'<span class="session-summary"><span class="session-date">{esc(s["date"])}</span><span><strong>{esc(s["title"])}</strong><small>{esc(s["kind"])}</small></span></span>'


def pathway(path):
    wearables = path == "w"
    label = "Wearables" if wearables else "Creative Robotics"
    body = hero(f'My Project · {label}', 'One workday.<br>One clear <span>next step.</span>', '18 individual projects · Tables W1–W3 · Jennifer' if wearables else '18 students · Nine teams of two · Tables R1–R3 · Stephanie')
    body += '<section class="section compact"><div class="hub-links">' + link("my-project.html", "Change pathway") + link("wearable-technology.html" if wearables else "creative-robotics.html", "Read the full pathway introduction") + link("tutorials.html", "Explore the tutorial library") + '</div><p class="section-intro">Open the date your mentor assigns. The first workday is expanded to help you begin.</p>'
    for i, s in enumerate(SESSIONS):
        body += f'<details class="curriculum-detail" id="{s["id"]}"' + (' open' if i == 0 else '') + f'><summary>{session_summary(s)}</summary><div class="detail-body">'
        task = s.get(f'{path}_task', s['goal'])
        body += f'<div class="day-quickstart"><div><h3>Start here</h3><p>{esc(task)}</p></div><div><h3>Your finish line</h3><p>{esc(s["goal"])}</p></div></div><div class="button-row">'
        body += link(s.get(path, s['guide']), "Open the full pathway guide" if path in s else "Open the full event guide", "button")
        body += link(s['guide'], "Workday overview", "button secondary") if path in s else ''
        body += link(s['evidence'], s['evidence_label'], "button secondary") + '</div>'
        if s['id'] == 'september-24':
            body += '<div class="deeper-links"><h3>Explore the technology</h3>' + list_html([link(url, name) for url, name, _ in TUTORIALS['Wearables' if wearables else 'Creative Robotics'] if 'proposal' not in url]) + '</div>'
        if s['id'] == 'november-16':
            body += '<p>' + link('wearable-prototype.html' if wearables else 'robotics-prototype.html', 'Open the complete prototype and first-test guide') + '</p>'
        if s['id'].startswith('march-'):
            body += '<p class="form-helper">Open the named reflection assignment in your Canvas course. The linked evidence guide supports presentation preparation.</p>'
        body += '</div></details>'
    body += '</section>'
    return body


def tutorials():
    body = hero('Tutorials', 'Go as deep as<br>you <span>need.</span>', 'The complete curriculum library: instructions, diagrams, examples, troubleshooting, and evidence guides. Start with your workday or explore a topic here.')
    body += '<section class="section compact"><div class="tutorial-search" hidden><label for="tutorial-query">Find a topic</label><input id="tutorial-query" type="search" placeholder="Try circuits, BirdBlox, proposal, or evidence" autocomplete="off"><p id="tutorial-count" role="status" aria-live="polite"></p></div>'
    for title, items in TUTORIALS.items():
        body += f'<section class="tutorial-category" aria-label="{esc(title)}"><h2>{esc(title)}</h2><ul class="tutorial-list">'
        for url, name, desc in items:
            body += f'<li data-tutorial><a href="{url}"><strong>{esc(name)}</strong><span>{esc(desc)}</span></a></li>'
        body += '</ul></section>'
    body += '<p id="tutorial-empty" hidden>No matching topics. Try a shorter word or clear the search to see every guide.</p></section>'
    return body


def room_plan():
    groups = []
    for label, lead, prefix in [('Wearables', 'Jennifer', 'W'), ('Creative Robotics', 'Stephanie', 'R')]:
        tables = ''.join(f'<li><strong>{prefix}{i}</strong><span>6 students · ' + ('6 individual projects' if prefix == 'W' else f'3 pairs · Teams R{3*i-2:02}–R{3*i:02} · 3 kits') + '</span></li>' for i in range(1, 4))
        groups.append(f'<section><h3>{lead} · {label}</h3><ul class="home-tables">{tables}</ul></section>')
    return '<details class="curriculum-detail" id="room-14"><summary>Room 14 · Six home tables · 36 students</summary><div class="detail-body"><div class="hub-pathways">' + ''.join(groups) + '</div><p><strong>Tri:</strong> technical demonstrations and support across both pathways. Keep the same table labels on the roster, signs, and student directions.</p><p>Home tables organize students. Schedule hands-on activities and demonstrations for groups that the available adults and prepared equipment can supervise.</p><p><strong>Prepare:</strong> 18 Wearables student sets and nine Robotics team sets, plus the Print Center’s labeled backup copies. Each Robotics pair uses one numbered kit/iPad set.</p></div></details>'


def mentors():
    body = hero('Tri · Jennifer · Stephanie', 'Your mentor<br><span>start page.</span>', 'Choose the date, read your role, and open the complete lesson when you need the technical detail. The full playbook and print resources remain available.')
    body += '<section class="section compact"><div class="hub-links">' + link("mentor-lesson-plans.html", "Full mentor playbook") + link("mentor-print-center.html", "Print Center") + link("program-roadmap.html", "All dates") + link("recruitment-toolkit.html", "Recruitment toolkit") + '</div>' + room_plan()
    body += '<label class="session-picker" for="mentor-session" hidden>Jump to a date<select id="mentor-session">' + ''.join(f'<option value="{s["id"]}">{esc(s["date"])} · {esc(s["title"])}</option>' for s in SESSIONS) + '</select></label>'
    for i, s in enumerate(SESSIONS):
        body += f'<details class="curriculum-detail mentor-session" id="{s["id"]}"' + (' open' if i == 0 else '') + f'><summary>{session_summary(s)}</summary><div class="detail-body"><p><strong>Prepare:</strong> {esc(s["prepare"])}</p><div class="mentor-role-grid">'
        for person, role, key in [('Jennifer', 'Wearables', 'j'), ('Stephanie', 'Creative Robotics', 's'), ('Tri', 'Technical lead', 't')]:
            body += f'<article><h3>{person}</h3><strong>{role}</strong><p>{esc(s[key])}</p></article>'
        body += f'</div><p><strong>Before students leave:</strong> {esc(s["goal"])}</p><div class="button-row">' + link(s['mentor'], 'Open the complete mentor plan', 'button') + link(s['guide'], 'Open the student guide', 'button secondary') + link('mentor-print-center.html#september-14' if i == 0 else 'mentor-print-center.html#later-workdays', 'Find the print materials', 'button secondary') + '</div>'
        if i == 0:
            body += '<details class="agenda-detail"><summary>September 24 agenda · Thursday bells</summary><div class="agenda-wrap"><table class="agenda-table"><thead><tr><th>Time</th><th>Plan</th></tr></thead><tbody>' + ''.join(f'<tr><th>{a}</th><td>{b}</td></tr>' for a, b in [
                ('8:00–9:25', 'Attendance, welcome, safety, and three-idea brainstorm'), ('9:25–9:38', 'Snack'), ('9:38–9:42', 'Return and settle'), ('9:42–11:09', 'Supervised technology exploration'), ('11:09–11:17', 'Pause, save evidence, and reset'), ('11:17–12:42', 'Finish exploration and begin labeled proposals'), ('12:42–1:12', 'Lunch'), ('1:12–1:16', 'Return and settle'), ('1:16–2:21', 'Proposal studio, staggered mentor reviews, and revisions'), ('2:21–2:41', 'Evidence, next action, safe storage, and cleanup')]) + '</tbody></table></div><p>Bell times follow the supplied Stauffer 2025–2026 schedule. Keep all required exploration evidence; use supervised demonstrations or smaller groups when a live activity exceeds capacity.</p></details>'
        elif 'lunch' in s['kind'].lower():
            body += '<p class="form-helper">Wednesday lunch · Room 14 · 11:37 a.m.–12:07 p.m.</p>'
        body += '</div></details>'
    return body + '</section>'


def breadcrumb(filename, title):
    parent = category(filename)
    items = [link(parent, dict(NAV)[parent])]
    if filename.startswith('wearable-'):
        items.append(link('wearables-project.html', 'Wearables'))
    elif filename.startswith('robotics-') or filename == 'creative-robotics.html':
        items.append(link('robotics-project.html', 'Creative Robotics'))
    items.append(f'<span aria-current="page">{esc(html.unescape(title.split(" | ")[0]))}</span>')
    return '<nav class="breadcrumbs no-print" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(items) + '</nav>'


def sync_existing(path):
    source = path.read_text(encoding='utf-8-sig')
    if 'class="site-header' not in source:
        return
    source = re.sub(r'<a class="skip-link"[^>]*>.*?</a>\s*', '', source)
    source = re.sub(r'<header class="site-header[^\"]*">.*?</header>', header(path.name), source, count=1, flags=re.S)
    source = re.sub(r'\s*<nav class="breadcrumbs no-print".*?</nav>\s*', '\n', source, flags=re.S)
    title = re.search(r'<title>(.*?)</title>', source).group(1)
    source = source.replace('</header>', '</header>\n' + breadcrumb(path.name, title), 1)
    source = re.sub(r'<main(?![^>]*\bid=)([^>]*)>', r'<main id="main-content"\1>', source, count=1)
    source = re.sub(r'<nav class="footer-nav no-print".*?</nav>', '', source, flags=re.S)
    source = source.replace('</footer>', footer_nav() + '</footer>')
    path.write_text(source, encoding='utf-8', newline='\n')


def main():
    pages = {'index.html': ('Student home', home()), 'my-project.html': ('My Project', my_project()), 'wearables-project.html': ('My Wearables workdays', pathway('w')), 'robotics-project.html': ('My Creative Robotics workdays', pathway('r')), 'tutorials.html': ('Tutorial library', tutorials()), 'mentors.html': ('Mentor start page', mentors())}
    pages['404.html'] = ('Page not found', hero('404 · Page not found', 'Find your <span>next step.</span>', 'Use My Project to find your workday, or browse the full tutorial library.') + '<section class="section compact"><div class="button-row">' + link('my-project.html', 'Open My Project', 'button') + link('tutorials.html', 'Find a tutorial', 'button secondary') + '</div></section>')
    for filename, (title, body) in pages.items():
        (ROOT / filename).write_text(document(filename, title, body), encoding='utf-8', newline='\n')
    for path in ROOT.glob('*.html'):
        if path.name not in GENERATED:
            sync_existing(path)
    print(f'Built {len(pages)} entry pages and synchronized curriculum navigation.')


if __name__ == '__main__':
    main()
