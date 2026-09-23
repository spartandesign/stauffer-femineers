"""Render the existing four-page studio layouts with September 24 backup prompts.

Exact text mappings preserve the original PDFs and reusable drawing primitives.
Run this script after changing the prompts; build_navigation.py links these outputs.
"""
from functools import wraps
import build_print_packets as base

WEARABLES = {
    'September-14-Wearables-Studio-Sheets.pdf': 'September-24-Backup-Wearables-Studio-Sheets.pdf',
    'September 24 Wearables Studio Sheets': 'September 24 Backup Wearables Studio Sheets',
    'September 24 wearables passport': 'September 24 backup - Wearables passport',
    'September 24 wearables idea canvas': 'September 24 backup - Individual proposal',
    'Side 1 of the capability passport - carry this through the four studios.': 'Pair practice; individual evidence. Use the paper symbol and sewing activities.',
    "Try it, notice what happened, and show or explain one piece of evidence. A truthful 'not yet' helps us plan support.": 'Record what you actually did. Label observed, simulated, or deferred work. Both partners practice; each explains her own contribution.',
    '1. Future Stamp - an idea can become a visible mark': '1. Paper future symbol - wood stitching deferred',
    'I tried it': 'Paper design', 'I can show it': 'Meaning explained', 'I want more practice': 'Wood stitching deferred',
    'The printed mark, a test impression, or a change I made.': 'Draw your paper symbol and explain its colors. Save a photo or digital sketch.',
    'I made a complete path': 'Practice sewn', 'LED lit': 'Powered test passed', 'I found a break': 'Powered test deferred',
    'Show battery +, conductive thread/tape, LED direction, and battery -.': 'Show battery + and -, separate conductive-thread paths, and sewable LED polarity.',
    'Circle or note: direction / contact / loose path / short circuit.': 'My contribution: ____. What I tested or observed: ____. One change: ____.',
    'Battery stayed cool; power was removed before changing the path; needle and snips returned to the counted tray.': 'Battery removed while sewing; mentor inspected both sides before power. Record only checks actually completed. Return and count needles.',
    'Side 2 of the capability passport - explain what caused what.': 'Use the W micro:bit. NeoPixels are an observed preview; physical testing is deferred.',
    'Program ran': 'Physical board', 'Input worked': 'Simulator only', 'I changed one thing': 'Change + retest',
    'Pressed A / pressed B / shook / other': 'A / B / A+B clear',
    'IF I ____________________, THEN the micro:bit ____________________.': 'IF I ____, THEN ____. Three A/B/A+B trials: ____ / ____ / ____. After my change: ____.',
    '4. NeoPixel - code controls color, order, and timing': '4. Observed NeoPixel preview - physical test deferred',
    'Pixels lit': 'Video observed', 'Pattern changed': 'Diagram/code observed', 'I safely reset': 'Physical test deferred',
    'Pattern I tested': 'Pattern I observed', 'One variable I changed': 'A change I would try',
    'What I noticed': 'What I noticed / predict', 'My second test': 'My proposed A / B / A+B off effects',
    'Stamp / circuit / micro:bit / NeoPixel': 'Paper symbol / circuit / micro:bit / NeoPixel idea',
    'Shirt - front and inside': 'Shirt - front, back, and circuit',
    'Draw outside view. Use a dotted line for battery, thread, or controller on the inside.': 'Label art, LED positions, separate paths, and battery location. Add a back-view inset.',
    'Hat or alternate wearable - outside and inside': 'Bucket hat - outside and inside',
    'Show where a person touches, sees, hears, or safely carries each part.': 'Label pixel path, controls, removable electronics, and balanced battery pockets.',
    'Input, movement, button, time, or viewing': 'A / B / A+B off; shirt switch',
    'What is the smallest test that would teach you something important?': 'Name the smallest test, including any deferred hardware. Owner / next school-time check: ____.',
    'My first test is small enough to finish and learn from.': 'First test / decision: Approved, Revise, or Technical Review.',
    'ready / make smaller': 'status + next action',
}

ROBOTICS = {
    'September-14-Robotics-Team-Studio-Sheets.pdf': 'September-24-Backup-Robotics-Team-Studio-Sheets.pdf',
    'September 24 Robotics Team Studio Sheets': 'September 24 Backup Robotics Team Studio Sheets',
    'September 24 robotics passport': 'September 24 backup - Robotics passport',
    'September 24 robotics idea canvas': 'September 24 backup - Team proposal',
    'Kit ______  Robot/device name ______  Driver first ______  Navigator first ______': 'Kit ____ Device ____ Sensor/type ____ Port ____ Driver ____ Navigator ____',
    'Far': 'Condition A', 'Near': 'Condition B', 'Far again': 'A again',
    'A value between our near and far readings is ______ because...': 'Define A/B conditions and units: ____. Threshold ____; comparison < / > because ____.',
    'Use only mentor-marked ports, prepared connections, and safe servo angles.': 'Use tested inputs/outputs. Two LEDs are the fallback when movement is deferred.',
    'Challenge 3 - two different outputs': 'Challenge 3 - two outputs; record their actual types',
    'LED': 'Output 1', 'Servo': 'Output 2',
    '0% -> 50% -> 100% -> 0%': 'LED port ____; 0% -> 50% -> 0%',
    'Only the two marked safe angles': 'Servo HOME/ACTIVE, or second LED 0% -> 50% -> 0%',
    'Ready angle': 'HOME / LED 0%',
    'IF the object is ______ than ______, THEN the light ______ AND the pointer ______; OTHERWISE...': 'IF input ____ meets ____, THEN output 1 ____ AND output 2 ____; OTHERWISE ____. Motion: tested / deferred.',
    'Object condition': 'Input condition', 'Servo/pointer': 'Output 2',
    'Both teammates can explain the input, threshold decision, two outputs, and what the system does when the condition is false.': 'Both explain input, decision, outputs, and reset. Two LEDs are one output type. Label any untested sensor/motion as deferred.',
    'Can we prove that ______ causes ______ safely and repeatably?': 'Can ____ cause ____ reliably? Missing test / owner / next school-time check: ____.',
    'Circle together: system is explainable / needs another conversation; safe first test / make smaller; ready to prototype / repair plan first.': 'Record Approved / Revise and Return / Needs Technical Review. Name the next action; untested hardware remains pending.',
}


def render(builder, mapping):
    def translate(value):
        if isinstance(value, str):
            return mapping.get(value, value)
        if isinstance(value, list):
            return [translate(item) for item in value]
        if isinstance(value, tuple):
            return tuple(translate(item) for item in value)
        return value

    def adapted(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*translate(args), **{key: translate(value) for key, value in kwargs.items()})
        return wrapper

    names = ['new_pdf', 'draw_header', 'section_title', 'draw_check_row', 'draw_card', 'draw_prompt', 'draw_table']
    originals = {name: getattr(base, name) for name in names}
    try:
        for name, fn in originals.items():
            setattr(base, name, adapted(fn))
        builder()
    finally:
        for name, fn in originals.items():
            setattr(base, name, fn)


if __name__ == '__main__':
    render(base.build_wearables_student_sheets, WEARABLES)
    render(base.build_robotics_team_sheets, ROBOTICS)
    print('Built two four-page September 24 backup packets; original PDFs retained.')
