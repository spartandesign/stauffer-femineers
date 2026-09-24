"""Build a student-paced companion from attributed photos and official media."""
import json
from html import escape
from build_supply_photos import panel, assets

BIRD = 'https://learn.birdbraintechnologies.com/hummingbirdbit/birdblox/program'
SPARK = 'https://learn.sparkfun.com/tutorials/lilypad-basics-e-sewing'

def video(title, video_id, source, cue, youtube=False):
    host = 'https://www.youtube-nocookie.com/embed/' if youtube else 'https://fast.wistia.net/embed/iframe/'
    return f'<details class="learn-media"><summary>{escape(title)}</summary><p>{cue}</p><iframe class="prep-video no-print" loading="lazy" src="{host}{video_id}" title="{escape(title)}" allow="fullscreen; picture-in-picture" allowfullscreen></iframe><p><a href="{source}">Open the original tutorial and illustrated steps</a></p></details>'

def steps(items):
    return '<ol class="learn-steps">' + ''.join(f'<li>{x}</li>' for x in items) + '</ol>'

def check(question, answer):
    return f'<details class="learn-check"><summary>Check yourself: {question}</summary><p>{answer}</p></details>'

def build(root, document):
    catalog = {r['id']: r for r in json.loads((root/'assets/supply-photos/catalog.json').read_text(encoding='utf-8'))}
    def photos(keys, name): return panel(keys, 'photos-'+name, catalog)
    def diagram(file, alt): return f'<a href="assets/mentor-guides/{file}" target="_blank" rel="noopener"><img class="learn-diagram" src="assets/mentor-guides/{file}" alt="{alt}" loading="lazy"></a>'
    body = '''<section class="page-hero prep-hero"><p class="eyebrow">September 24 backup plan · Student learning companion</p><h1>Watch. Try.<br><span>Check. Explain.</span></h1><p class="lede">Short lessons you can pause and repeat. Choose your pathway and follow the steps at your own pace within today's activity times.</p><nav class="prep-jumps no-print" aria-label="Learning modules"><a href="#start">Start here</a><a href="#sewing">1 · Sew</a><a href="#microbit">2 · Code</a><a href="#robotics">3 · Robotics</a><a href="#glowing-pin">4 · Glowing Pin</a><a href="#robot-mood">5 · Robot Mood</a><a href="#preview">6 · Paper &amp; pixels</a><a href="#save">Save &amp; reflect</a></nav></section>
<section class="section compact" id="start"><h2>Start here</h2><p><strong>Wearables:</strong> module 1, then module 2. Module 4 is optional before the 10:05 needle count. <strong>Robotics:</strong> module 3, then optional module 5. <strong>Everyone:</strong> module 6 at 11:17 with your mentor, then proposals.</p><p>Open one video at a time. Watch, pause, do the written step, and compare the result. BirdBlox videos are silent: the written instructions are your guide. You can use the written lessons if media is blocked. No additional homework is assigned.</p><div class="callout"><strong>Independent learning with mentor checkpoints:</strong> reading, sketching, and simulator work can be independent. Jennifer checks sewn circuits before power. Stephanie or Tri checks actual ports, sensor conditions, and any motion. If a mentor is unavailable, stop at that checkpoint and continue with a drawing or prediction.</div><p>Photos below are real manufacturer/supplier reference photographs, not photos of our classroom inventory. Match the actual markings with your mentor. Diagrams and block drawings are labeled illustrations. Tap photos or diagrams to enlarge.</p><p><a href="september-24-backup.html#agenda">Today's schedule</a> · <a href="mentor-backup-plan.html">Mentor preparation and release checks</a></p></section>'''
    body += '<section class="section compact" id="sewing"><h2>1 · Sew a one-LED felt circuit</h2><p>Wearables · Share one set per pair · Finish or save progress by 10:05.</p>'
    body += photos(['sewable-led','coin-holder','coin-cell','conductive-thread','needles','threaders'], 'sewing')
    body += video('Watch: sewable-electronics overview', 'T46MzLMpjfM', 'https://www.youtube.com/watch?v=T46MzLMpjfM', 'This is an overview of a supplier kit. Identify the holder, sew pads, and conductive thread; use the parts approved for our classroom circuit.', True)
    body += f'<p><a href="{SPARK}">SparkFun photo tutorial: needle, pad loops, stitches, knots, and short-circuit checks</a> · <a href="mentor-circuit-lab-prep.html#prepare">Our detailed circuit preparation</a></p>'
    body += diagram('circuit-loop.svg','Illustration: separate positive and negative paths between an approved holder and sewable LED.')
    body += steps([
      '<strong>Identify.</strong> Place the holder and LED on felt. Point to each + and − marking. Ask Jennifer to confirm the matching cell and LED/module; do not infer compatibility from a photo.',
      '<strong>Trace.</strong> With no battery installed, draw one route from holder + to LED + and a separate route from LED − to holder −. Check that neither route crosses on the front or back.',
      '<strong>Practice.</strong> Thread a counted needle. On scrap felt, make small running stitches and snug loops through a practice pad. Each partner takes a turn; ask Jennifer to check the connection.',
      '<strong>Sew the positive route.</strong> Follow the approved example: secure the thread, make snug pad loops, stitch to the other + pad, secure the end, and trim its loose tail. Do not continue that same strand into the negative route.',
      '<strong>Sew the negative route.</strong> Use a separate strand for the two − pads. Keep stitches and knots separated from the positive route on both sides.',
      '<strong>Stop for inspection.</strong> Keep the battery out. Show both sides to Jennifer. Point out loose tails, crossings, or frayed thread for correction before a powered test.',
      '<strong>Test and document.</strong> After approval, install the cell in the holder’s marked orientation and test. Record lit / not lit and what you observed. Remove power before any repair; stop and tell a mentor if a component becomes warm.',
      '<strong>Save and return.</strong> Photograph both sides and explain your contribution. Return every needle before snack and before coding. An unfinished sample can be saved with its next step.'
    ])
    body += diagram('circuit-stitch.svg','Illustration of pad loops, running stitches, and inspection on both sides.')
    body += check('Can one continuous thread connect all four pads?', 'No. That can join the positive and negative paths. Use the two separate paths in the approved example; inspect both fabric sides before power.')
    body += '<details><summary>If the LED does not light</summary><p>Remove the cell. Check the marked polarity, switch position, pad loops, and loose tails with your mentor. Do not add more batteries or bypass components. Record powered test pending if the fault is unresolved.</p></details></section>'
    body += '<section class="section compact" id="microbit"><h2>2 · Make buttons communicate</h2><p>Wearables · 10:05–11:09 · Use the W board and laptop; leave the Hummingbird R boards with their kits.</p>'
    body += photos(['microbit','microbit-kit','usb-cable'],'microbit')
    body += video('Watch: transfer code over USB','vhgjNH3de0Y','https://support.microbit.org/support/solutions/articles/19000013986-how-do-i-transfer-my-code-onto-the-micro-bit-via-usb','Watch the connection and transfer sequence. A cable that supplies power may still lack data wires.',True)
    body += diagram('microbit-buttons-blocks.svg','Illustrated MakeCode stacks: start clear, A heart, B happy, A+B clear.')
    body += steps([
      '<strong>Open.</strong> Go to <a href="https://makecode.microbit.org/">MakeCode</a>, create a project, and give it a recognizable name. Or open <a href="mentor-microbit-prep.html#starter">our editable starter and text code</a>.',
      '<strong>Start clear.</strong> In Blocks, place Basic → clear screen inside on start. Remove an unused forever block to keep your workspace readable.',
      '<strong>Add A.</strong> Drag Input → on button A pressed onto the workspace. Put Basic → show icon inside it and choose the heart.',
      '<strong>Add B and A+B.</strong> Add two more button events. Select B and place a happy-face icon inside; select A+B and place clear screen inside.',
      '<strong>Simulate.</strong> Click A, B, and A+B on the on-screen board. Predict each result first. Fix an icon in the wrong event before downloading.',
      '<strong>Transfer.</strong> Connect the W board using the tested USB data cable. Follow the editor’s Download instructions; if it saves a .hex file, copy it to the MICROBIT drive. Wait for transfer activity to finish.',
      '<strong>Test together.</strong> Press the physical buttons. Repeat the A/B/A+B sequence three times; swap roles so both partners can explain and test the program. Label a simulator-only result honestly.',
      '<strong>Personalize and save.</strong> Change two symbols for a user, ask a partner what they mean, and retest. Download the .hex file and save a screenshot. Use mentor-approved battery power only after disconnecting USB in this classroom workflow.'
    ])
    body += check('Does a successful simulator test prove the USB transfer worked?', 'No. Record the simulator result separately and test the physical board after the transfer.')
    body += '<details><summary>If the board does not appear</summary><p>Keep your code open. Check the cable and connection with Tri; try the tested spare data cable. Continue in the simulator and record physical transfer pending. Do not reflash an R board to replace it.</p></details></section>'
    body += '<section class="section compact" id="robotics"><h2>3 · Connect, sense, and respond</h2><p>Creative Robotics · Finish core evidence by 11:09 · One kit and iPad per pair.</p>'
    body += photos(['hummingbird-controller','microbit','robot-led','distance-sensor','position-servo','hummingbird-power'],'robotics')
    for title,vid,cue in [
        ('Watch: connect the assigned kit','venbr7iqc4','Match the kit identity; do not connect to a neighboring table.'),
        ('Watch: single-color LED connection','i4grfkkyh0','With kit power off, compare the LED port and polarity with your mentor-approved setup.'),
        ('Watch: LED programming','fjyw30dg0d','Find the LED control block and identify its port and brightness fields.'),
        ('Watch: light sensor introduction','cijsxk94r5','Choose this only if your kit has the mentor-identified light sensor. Record two actual readings.'),
        ('Watch: dial sensor introduction','kgx73bpqcb','Choose this only for a dial sensor. Compare two knob positions; let the mentor confirm your comparison.'),
        ('Watch: distance sensor introduction','q86zodv78l','Choose this only for the distance sensor. Use your tested positions and comparison; do not copy an unrelated threshold.'),
        ('Watch: button input introduction','f0tbcmy2kp','Use only the mentor-prepared button fallback if a sensor is unavailable. Mark sensor work deferred.'),
        ('Watch: position servo connection — optional','0ckiknl45h','Watch for later understanding. Physical movement requires a secured servo and mentor-released travel range.')]:
        body += video(title,vid,BIRD,cue+' These official clips are silent; read the steps below.')
    body += steps([
      '<strong>Identify and inspect.</strong> Record your R kit name, actual sensor type, and input/output ports. Stephanie checks wiring with power off. Two LEDs are enough for today’s nonmoving version.',
      '<strong>Connect.</strong> Use the assigned iPad in BirdBlox, open a named project, and connect to your kit’s identity. Ask for help if it is missing; students do not replace the kit firmware.',
      '<strong>Read the input.</strong> Watch the lesson that matches the actual sensor. Show two repeatable conditions and write down their readings. Have Stephanie confirm the threshold, units, and comparison direction.',
      '<strong>Test outputs separately.</strong> For the two-LED setup use LEDS 1 and 2. Test LED 1 at the approved brightness and back to 0, then LED 2. If nothing lights, stop and ask for a power-off wiring check.',
      '<strong>Build one finite response.</strong> Start with both LEDs at 0. Use if/else for the approved input condition: true → LED 1 at 50, LED 2 at 0; false → LED 1 at 0, LED 2 at 50. Wait one second, then set both to 0. Stephanie rehearses this on the actual kit before release.',
      '<strong>Predict and test.</strong> Run once for each condition. Record three trials with condition, prediction, actual response, and reset. Change one thing and retest the same conditions.',
      '<strong>Swap and explain.</strong> Exchange Driver/Navigator. Each partner traces input → decision → output and explains how the program ends.',
      '<strong>Save and shut down.</strong> Save the BirdBlox project, capture readable blocks and the actual setup, then use the rehearsed reset, Stop, disconnect, and power off. For unexpected movement, heat, or a jam, power off and call the mentor; do not command another movement.'
    ])
    body += check('Are two LEDs two different types of output?', 'They are two output devices of the same type. Record motion deferred if you did not test a servo.')
    body += '<details><summary>If the sensor or connection fails</summary><p>Save the readings or connection message. Recheck the assigned kit identity with Stephanie. Use only her rehearsed fallback, or observe a working demonstration and label it observed. Do not invent passing trials.</p></details></section>'
    body += '<section class="section compact" id="glowing-pin"><h2>4 · Optional: Glowing Pin</h2><p>Wearables · 10–20 minutes of remaining Circuit Lab time · Stop for needle count at 10:05.</p><p><a href="https://learn.sparkfun.com/tutorials/glowing-pin/all">Open SparkFun’s photo-by-photo Glowing Pin tutorial</a>. This is an inspiration example; our parts and LED orientation may differ.</p>'
    body += steps(['Choose a character, symbol, or message for the existing inspected felt circuit. Sketch where its single light belongs.','Remove the cell before trimming or adding stitching. Keep decoration and attachments away from conductive paths and keep the battery holder accessible.','Show both sides to Jennifer again before a powered test. A pin back is optional and only used if available and approved; a flat glowing sample is a complete practice outcome.','Save a photo with one sentence explaining the light. Share the circuit with your partner and record your own contribution. Return all needles on time.'])
    body += '<p><a href="mentor-backup-plan.html#optional-glowing-pin">Materials and mentor instructions</a> · <a href="#sewing">Review photos and circuit steps</a>. This uses a coin cell, not a micro:bit. It is separate from the October 13 badge event.</p></section>'
    body += '<section class="section compact" id="robot-mood"><h2>5 · Optional: Robot Mood</h2><p>Creative Robotics · 10–15 minutes after core evidence · End by 11:09.</p><p>Use two LEDs to communicate welcome/wait or calm/excited. This is our classroom extension; the official LED and input clips above teach its component skills.</p>'
    body += steps(['Sketch two messages and choose which tested input condition means each. Keep the existing ports and mentor-approved comparison.','Copy your working program under a new name. Start both LEDs at 0. In the true branch, keep LED 2 off and light LED 1 at the approved brightness for one second.','In the false branch, keep LED 1 off. Repeat twice: LED 2 on, wait 0.25 seconds, LED 2 off, wait 0.25 seconds. End the whole program with both LEDs at 0. Run once per test.','Swap roles, try both conditions, and ask another pair to interpret the messages. Change one pattern and retest. Save blocks and a short result before shutdown.'])
    body += check('Must we build a moving robot body to finish?', 'No. Two LEDs on the table can demonstrate the interaction. A paper face is optional; servo work needs a separately tested setup.')
    body += '<p><a href="#robotics">Replay the LED/input videos</a> · <a href="mentor-backup-plan.html#optional-robot-mood">Full optional challenge</a></p></section>'
    body += '<section class="section compact" id="preview"><h2>6 · Paper Future Stamp and NeoPixel observation</h2><p>Everyone · Follow the 11:17–11:45 shared session: share, draw, observe. Wood stitching and physical NeoPixel testing remain deferred.</p>'
    body += steps(['After the group share, choose a future person or need. Draw a simple symbol on paper or digitally, choose two colors, and write what they mean. Label it paper symbol design; wood stitching deferred.','Watch the preview below or open the illustrated blocks. Sketch a possible hat-light pattern. Describe what A, B, and A+B off could do.','Save the sketch as observed video or observed diagram/code, whichever you used. A video is not evidence that your own strip works. Do not assemble a new pixel power harness today.'])
    body += '<details class="learn-media"><summary>Watch: official micro:bit NeoPixel preview</summary><video class="prep-video no-print" controls preload="none"><source src="https://video.microbit.org/support/neopixel.mp4" type="video/mp4"></video><p><a href="https://video.microbit.org/support/neopixel.mp4">Open video directly</a> · <a href="https://support.microbit.org/support/solutions/articles/19000130206-using-neopixels-with-the-micro-bit">Official illustrated example</a>. This hardware example does not replace our prepared system’s wiring instructions.</p></details>'
    body += video('Watch: coding NeoPixel patterns','G5LjM_Izk88','https://www.youtube.com/watch?v=G5LjM_Izk88','Observe programming ideas. Use our illustrated starter to discuss A/B/off behavior; physical tests are deferred.',True)
    body += '<p><a href="mentor-neopixel-prep.html#starter">Our illustrated blocks and text starter</a> · <a href="mentor-neopixel-prep.html#wiring">Labeled system diagram</a></p>'
    body += photos(['neopixel-strip','jst-connector'],'preview')
    body += '</section><section class="section compact" id="save"><h2>Save, explain, and continue</h2><p>Use the existing studio sheets or a named digital record. For every activity write: <strong>what I tried → what happened → one change → what I still need to test</strong>. Mark results physical, simulator, observed, or deferred.</p><ul><li>Wearables: each student explains her own contribution to shared practice.</li><li>Robotics: both partners explain the complete interaction and reset.</li><li>Save code plus a readable screenshot; a screenshot alone cannot be loaded back onto the board.</li><li>If Canvas upload fails, record the local file location and upload pending.</li></ul><p><a href="september-24-backup.html#evidence">Required evidence checklist and proposals</a> · <a href="mentor-backup-plan.html#review">Mentor review and next tests</a></p><p>Use your three ideas and labeled proposal after the shared preview. Optional activities do not replace those deliverables. Stop for cleanup at 2:21.</p></section>'
    from september_backup import page
    result = assets(page(document,'learn-at-your-pace.html','Learn at your pace · Femineers',body))
    result = result.replace('</head>','<link rel="stylesheet" href="assets/self-paced.css"></head>')
    (root/'learn-at-your-pace.html').write_text(result,encoding='utf-8',newline='\n')
