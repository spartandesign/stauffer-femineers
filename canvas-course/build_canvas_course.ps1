param(
  [string]$OutputDirectory = $PSScriptRoot
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$courseTitle = 'Limitless: Designed by Her — Stauffer Femineers 2026–2027'
$courseCode = 'STAUFFER-FEM-2627'
$baseUrl = 'https://spartandesign.github.io/stauffer-femineers'
$canvasNamespace = 'http://canvas.instructure.com/xsd/cccv1p0'
$canvasSchema = 'https://canvas.instructure.com/xsd/cccv1p0.xsd'
$ccNamespace = 'http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1'
$lorType = 'associatedcontent/imscc_xmlv1p1/learning-application-resource'

function New-StableId([string]$Key) {
  $md5 = [System.Security.Cryptography.MD5]::Create()
  try {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Key)
    $hash = $md5.ComputeHash($bytes)
    return 'g' + (($hash | ForEach-Object { $_.ToString('x2') }) -join '')
  }
  finally {
    $md5.Dispose()
  }
}

function ConvertTo-XmlText([string]$Value) {
  if ($null -eq $Value) { return '' }
  return [System.Security.SecurityElement]::Escape($Value)
}

function Write-Utf8([string]$Path, [string]$Content) {
  $parent = Split-Path -Parent $Path
  if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
  }
  [System.IO.File]::WriteAllText($Path, $Content, [System.Text.UTF8Encoding]::new($false))
}

function New-CanvasPageHtml($Page, [string]$Identifier) {
  $links = ($Page.Links | ForEach-Object {
    $label = [System.Net.WebUtility]::HtmlEncode($_.Label)
    $url = [System.Net.WebUtility]::HtmlEncode($_.Url)
    '<a href="{0}" style="display:inline-block;margin:0 8px 8px 0;padding:10px 16px;border-radius:999px;background:#5f3dc4;color:#ffffff;text-decoration:none;font-weight:700;">{1}</a>' -f $url, $label
  }) -join "`n"

  $title = [System.Net.WebUtility]::HtmlEncode($Page.Title)
  $eyebrow = [System.Net.WebUtility]::HtmlEncode($Page.Eyebrow)
  $lede = [System.Net.WebUtility]::HtmlEncode($Page.Lede)
  $frontPageMeta = if ($Page.Slug -eq 'welcome') { '<meta name="front_page" content="true"/>' } else { '' }

  return @"
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>$title</title>
<meta name="identifier" content="$Identifier"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="active"/>
$frontPageMeta
</head>
<body>
<div style="max-width:900px;margin:0 auto;font-family:Arial,Helvetica,sans-serif;color:#25223a;line-height:1.55;">
  <div style="padding:28px;border-radius:18px;background:#5f3dc4;color:#ffffff;margin-bottom:22px;">
    <p style="margin:0 0 6px;text-transform:uppercase;letter-spacing:1.2px;font-size:13px;font-weight:700;">$eyebrow</p>
    <h1 style="margin:0 0 10px;font-size:34px;line-height:1.15;color:#ffffff;">$title</h1>
    <p style="margin:0;font-size:18px;">$lede</p>
  </div>
  $($Page.Content)
  <div style="margin-top:24px;padding:18px;border:2px solid #ded8f7;border-radius:14px;background:#f7f5ff;">
    <p style="margin:0 0 12px;font-weight:700;">Open the detailed visual guides:</p>
    $links
  </div>
</div>
</body>
</html>
"@
}

function New-AssignmentHtml($Assignment) {
  $title = [System.Net.WebUtility]::HtmlEncode($Assignment.Title)
  $guide = [System.Net.WebUtility]::HtmlEncode($Assignment.Guide)
  return @"
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Assignment: $title</title>
</head>
<body>
<div style="max-width:850px;margin:0 auto;font-family:Arial,Helvetica,sans-serif;color:#25223a;line-height:1.55;">
  <div style="padding:24px;border-radius:16px;background:#168b88;color:#ffffff;margin-bottom:20px;">
    <p style="margin:0 0 6px;text-transform:uppercase;letter-spacing:1px;font-size:13px;font-weight:700;">Canvas Evidence</p>
    <h1 style="margin:0;color:#ffffff;font-size:30px;">$title</h1>
  </div>
  $($Assignment.Content)
  <div style="margin-top:22px;padding:18px;border-left:6px solid #ef6a74;background:#fff3f4;">
    <p style="margin:0 0 8px;"><strong>Submission choices:</strong> file upload, text entry, website URL, or media recording. Use the format your mentor directs.</p>
    <p style="margin:0;"><strong>Due date:</strong> intentionally unset in this template. Mentors will add the approved date in Canvas.</p>
  </div>
  <p style="margin-top:20px;"><a href="$guide" style="display:inline-block;padding:10px 16px;border-radius:999px;background:#5f3dc4;color:#ffffff;text-decoration:none;font-weight:700;">Open the detailed evidence guide</a></p>
</div>
</body>
</html>
"@
}

$pages = @(
  [ordered]@{
    Slug='welcome'; Title='Welcome to Limitless: Designed by Her'; Eyebrow='Stauffer Femineers 2026–2027';
    Lede='Imagine it. Build it. Become it. Use this Canvas course to move from a future-focused idea to a tested public project.';
    Content=@'
<div style="padding:20px;border:1px solid #ded8f7;border-radius:14px;margin-bottom:18px;">
  <h2 style="margin-top:0;color:#5f3dc4;">How the course works</h2>
  <ul><li>Up to 50 Femineers work through six project phases using five full pull-out workdays and three Wednesday lunch checkpoints.</li><li>Full workdays meet in Room 14 on the Monday bell schedule, 8:00 a.m.–2:41 p.m.</li><li>Lunch checkpoints meet in Room 14 from 12:29–12:59 p.m. on October 21, January 13, and February 10.</li><li>Students must check with teachers, collect assignments and notes, and complete all classwork missed during pull-out workdays by each teacher’s deadline.</li><li>Tri Tansopalucks, Jennifer Frausto, and Stephanie Chavez are the three primary teacher mentors.</li><li>Use your iPad for Canvas, evidence, and BirdBlox. Classroom Windows laptops support MakeCode and micro:bit preparation.</li></ul>
</div>
<div style="padding:20px;border-radius:14px;background:#edf9f8;">
  <h2 style="margin-top:0;color:#168b88;">Your course routine</h2>
  <ol><li>Open the current module and read the workday or lunch-checkpoint overview.</li><li>Follow the exact guide for your project pathway.</li><li>Stop at every mentor safety or approval gate.</li><li>Capture honest evidence while the result is visible.</li><li>Submit on time, demonstrate when required, and write the next action.</li></ol>
</div>
'@;
    Links=@(@{Label='Open the visual student website';Url="$baseUrl/index.html"},@{Label='Start Phase 1';Url="$baseUrl/start-here.html"})
  },
  [ordered]@{
    Slug='roadmap'; Title='Program Roadmap and Important Dates'; Eyebrow='Orientation';
    Lede='Students are pulled from regular classes for five Stauffer workdays and are responsible for completing missed classwork. Three Wednesday lunch checkpoints maintain progress between workdays.';
    Content=@'
<table style="width:100%;border-collapse:collapse;"><thead><tr style="background:#f0edff;"><th style="padding:10px;border:1px solid #d9d3ef;text-align:left;">Date</th><th style="padding:10px;border:1px solid #d9d3ef;text-align:left;">Event</th><th style="padding:10px;border:1px solid #d9d3ef;text-align:left;">Main goal</th></tr></thead><tbody>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Sept. 21</td><td style="padding:10px;border:1px solid #d9d3ef;">Phase 1: Imagine the Future</td><td style="padding:10px;border:1px solid #d9d3ef;">Explore, brainstorm, propose, approve</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Oct. 13</td><td style="padding:10px;border:1px solid #d9d3ef;">District Kickoff at Griffiths</td><td style="padding:10px;border:1px solid #d9d3ef;">Community event; not a Stauffer build day</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Oct. 19</td><td style="padding:10px;border:1px solid #d9d3ef;">Phase 2 Design Ready package due</td><td style="padding:10px;border:1px solid #d9d3ef;">Submit design, systems, materials, and test plan</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Oct. 21</td><td style="padding:10px;border:1px solid #d9d3ef;">Design Ready lunch checkpoint</td><td style="padding:10px;border:1px solid #d9d3ef;">Demonstrate and receive readiness status</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Nov. 9</td><td style="padding:10px;border:1px solid #d9d3ef;">Phase 3: Design What’s Next</td><td style="padding:10px;border:1px solid #d9d3ef;">Quick prototype, test, and major construction</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Dec. 2</td><td style="padding:10px;border:1px solid #d9d3ef;">Project Rescue lunch</td><td style="padding:10px;border:1px solid #d9d3ef;">Invitation-only support for yellow and red projects</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Dec. 7</td><td style="padding:10px;border:1px solid #d9d3ef;">Phase 4: Build &amp; Test</td><td style="padding:10px;border:1px solid #d9d3ef;">Subsystem testing and winter restart plan</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Jan. 13</td><td style="padding:10px;border:1px solid #d9d3ef;">Restart Ready lunch checkpoint</td><td style="padding:10px;border:1px solid #d9d3ef;">Confirm status, code, supplies, and priorities</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Jan. 25</td><td style="padding:10px;border:1px solid #d9d3ef;">Phase 5: Build the Future</td><td style="padding:10px;border:1px solid #d9d3ef;">Integrate, test, redesign</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Feb. 10</td><td style="padding:10px;border:1px solid #d9d3ef;">Gala Path lunch checkpoint</td><td style="padding:10px;border:1px solid #d9d3ef;">Rank repairs and prepare for final workday</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Feb. 22</td><td style="padding:10px;border:1px solid #d9d3ef;">Phase 6: Step Into the Future</td><td style="padding:10px;border:1px solid #d9d3ef;">Inspect, pass twice, rehearse, pack</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Mar. 1</td><td style="padding:10px;border:1px solid #d9d3ef;">Stauffer Gala — Library</td><td style="padding:10px;border:1px solid #d9d3ef;">First public showcase</td></tr>
<tr><td style="padding:10px;border:1px solid #d9d3ef;">Mar. 18 evening</td><td style="padding:10px;border:1px solid #d9d3ef;">District Gala — Downey High</td><td style="padding:10px;border:1px solid #d9d3ef;">Projects, guest speakers, Culinary Arts hors d’oeuvres, and district celebration</td></tr></tbody></table>
'@;
    Links=@(@{Label='Open the visual roadmap';Url="$baseUrl/program-roadmap.html"})
  },
  [ordered]@{
    Slug='lunch-checkpoints'; Title='Lunch Checkpoints and Milestone Treats'; Eyebrow='October 21 · January 13 · February 10';
    Lede='Submit first, demonstrate your progress in Room 14 during lunch, receive a clear readiness status, and leave with one exact next action.';
    Content=@'
<h2 style="color:#5f3dc4;">Deliver · Demonstrate · Celebrate</h2><ol><li>Submit every required item by the listed deadline.</li><li>Provide genuine evidence of your progress.</li><li>Demonstrate or explain the deliverable in sixty seconds.</li><li>Identify the next action.</li><li>Complete the individual reflection.</li></ol>
<h2 style="color:#168b88;">Status</h2><ul><li><strong>Green:</strong> complete and ready.</li><li><strong>Yellow:</strong> one named revision is required.</li><li><strong>Red:</strong> mentor help is required before building.</li></ul>
<div style="padding:16px;background:#fff3c9;border-radius:12px;"><strong>Milestone Treat:</strong> students who meet the checkpoint may choose an ingredient-labeled packaged treat or a nonfood prize. The reward recognizes preparation and responsibility, not whose project looks most polished. Excused absences, documented accommodations, and verified technology problems receive a reasonable make-up opportunity.</div>
'@;
    Links=@(@{Label='Open the full lunch checkpoint guide';Url="$baseUrl/lunch-checkpoints.html"})
  },
  [ordered]@{
    Slug='choose-path'; Title='Know Your Project Pathway'; Eyebrow='Orientation';
    Lede='First-year Femineers complete Creative Robotics, second-year Femineers complete Wearable Technology, and third-year Femineers choose either pathway. Both pathways use the engineering design process.';
    Content=@'
<div style="padding:20px;border-left:7px solid #168b88;background:#edf9f8;margin-bottom:18px;"><h2 style="margin-top:0;">First year: Creative Robotics — team of two</h2><p>Use one BirdBrain Hummingbird Premium Kit and BirdBlox on an iPad to build a future-focused visitor interaction with at least one input and two outputs.</p><p><strong>You submit:</strong> shared technical evidence plus an individual contribution and reflection from each partner.</p></div>
<div style="padding:20px;border-left:7px solid #ef6a74;background:#fff3f4;margin-bottom:18px;"><h2 style="margin-top:0;">Second year: Wearable Technology — individual</h2><p>Create a painted denim shirt with 4–8 sewn LEDs and a programmable bucket hat using a removable 10–12-pixel WS2812B strip, a wearable micro:bit, and MakeCode.</p><p><strong>You submit:</strong> your own proposal, evidence, reflections, and final presentation.</p></div>
<div style="padding:20px;border-left:7px solid #5f3dc4;background:#f0edff;"><h2 style="margin-top:0;">Third year: choose either pathway</h2><p>Select Creative Robotics in a team of two or an individual Wearable Technology project, then follow that pathway’s directions for the year.</p></div>
'@;
    Links=@(@{Label='Robotics: first year or third-year choice';Url="$baseUrl/creative-robotics.html"},@{Label='Wearables: second year or third-year choice';Url="$baseUrl/wearable-technology.html"},@{Label='Browse idea starters';Url="$baseUrl/idea-starters.html"})
  },
  [ordered]@{
    Slug='safety-evidence'; Title='Safety, Supplies, and Evidence Rules'; Eyebrow='Orientation';
    Lede='The safety gate, equipment identity, and evidence routine apply during every phase.';
    Content=@'
<h2 style="color:#5f3dc4;">Always</h2><ul><li>Power off before touching wiring, stitches, sensors, servos, mechanisms, connectors, or batteries.</li><li>Use only your assigned wearable controller or numbered Hummingbird kit.</li><li>Keep electronics, batteries, switches, connectors, and repair points accessible.</li><li>Stop for heat, odor, damaged power parts, exposed conductors, uncontrolled motion, pressure, pinching, or an unstable structure.</li><li>Capture honest evidence before changing the project.</li></ul>
<h2 style="color:#ef6a74;">Mentor-only wearable work</h2><p>Students do not cut the purchased WS2812B strip, solder, splice, rebuild the pixel harness, join the two positive supplies, or alter any level interface. Mentors prepare and test the removable harness.</p>
<h2 style="color:#168b88;">Evidence pattern</h2><p>Write a success condition, record the real result, change one named variable, retest fairly, explain what the evidence shows, and leave a specific next action.</p>
'@;
    Links=@(@{Label='See our supplies';Url="$baseUrl/our-supplies.html"},@{Label='Capture good evidence';Url="$baseUrl/capture-evidence.html"},@{Label='Engineering design process';Url="$baseUrl/design-process.html"})
  },
  [ordered]@{
    Slug='phase-1-overview'; Title='Phase 1: Imagine the Future'; Eyebrow='Monday, September 21, 2026';
    Lede='Explore the technology, identify a future need or identity, brainstorm three ideas, choose with evidence, and earn mentor approval.';
    Content=@'
<h2 style="color:#5f3dc4;">Today’s finish line</h2><ol><li>Understand the Limitless challenge and your assigned or selected pathway requirements.</li><li>Explore the actual technology without beginning major construction.</li><li>Generate at least three distinct ideas.</li><li>Choose one idea using purpose, feasibility, safety, supplies, and time.</li><li>Create labeled sketches, materials, system behavior, evidence plan, and roles.</li><li>Earn mentor approval before submitting Checkpoint 1.</li></ol>
<div style="padding:16px;background:#fff3f4;border-radius:12px;"><strong>Phase boundary:</strong> Phase 1 ends with an approved plan—not permanent construction.</div>
'@;
    Links=@(@{Label='Open Phase 1 start page';Url="$baseUrl/start-here.html"},@{Label='Read the Limitless challenge';Url="$baseUrl/limitless-challenge.html"},@{Label='Mentor approval gate';Url="$baseUrl/mentor-approval.html"})
  },
  [ordered]@{
    Slug='phase-1-tools'; Title='Meet the Technology'; Eyebrow='Phase 1 exploration';
    Lede='Use the tutorials for your assigned or selected pathway, then record what each component makes possible and what safety rule controls it.';
    Content=@'
<h2 style="color:#168b88;">Creative Robotics — 1st year or 3rd-year choice</h2><ul><li>Hummingbird input, decision, two outputs, and reset</li><li>Premium Kit quantities and assigned ports</li><li>BirdBlox connection using the assigned three-word name and green dot</li><li>Driver/Navigator rotation and safe startup/shutdown</li></ul>
<h2 style="color:#ef6a74;">Wearables — 2nd year or 3rd-year choice</h2><ul><li>Sewable LEDs and polarity</li><li>Conductive thread paths and separation</li><li>micro:bit with MakeCode on a Windows laptop</li><li>WS2812B programmable strip with a mentor-prepared removable harness</li></ul>
'@;
    Links=@(@{Label='Sewable LED basics';Url="$baseUrl/sewable-led-basics.html"},@{Label='Conductive thread basics';Url="$baseUrl/conductive-thread-basics.html"},@{Label='Meet the micro:bit';Url="$baseUrl/meet-the-microbit.html"},@{Label='Meet programmable pixels';Url="$baseUrl/meet-the-neopixels.html"})
  },
  [ordered]@{
    Slug='phase-1-proposal'; Title='Prepare Your Approved Design Proposal'; Eyebrow='Phase 1 design gate';
    Lede='A mentor should be able to understand the user, purpose, appearance, technology, materials, safety, program behavior, and first test without guessing.';
    Content=@'
<h2 style="color:#5f3dc4;">Required for everyone</h2><ul><li>Future user, audience, need, identity, or opportunity</li><li>Three distinct ideas and an evidence-based selection</li><li>Labeled sketches from enough views to show hidden parts</li><li>Exact materials and electronics</li><li>Input/output or light-behavior story</li><li>Safety, comfort/stability, access, and repair plan</li><li>First prototype and success condition</li></ul>
<p><strong>Robotics teams:</strong> include both names, one kit number, three-word device name, Driver/Navigator plan, and individual reflections.</p>
'@;
    Links=@(@{Label='Wearable proposal guide';Url="$baseUrl/wearable-design-proposal.html"},@{Label='Robotics proposal guide';Url="$baseUrl/robotics-design-proposal.html"},@{Label='Checkpoint 1 visual guide';Url="$baseUrl/canvas-checkpoint-1.html"})
  },
  [ordered]@{
    Slug='phase-2-overview'; Title='Phase 2: Arrive Ready to Build'; Eyebrow='October Canvas deliverables · October 21 lunch checkpoint';
    Lede='Turn the approved proposal into a complete, buildable package and a focused first-test plan before the November 9 workday.';
    Content=@'
<h2 style="color:#5f3dc4;">Eight Design Ready deliverables</h2><ol><li>Approved proposal and revisions</li><li>Labeled project drawing</li><li>Pathway circuit or input → decision → outputs → reset diagram</li><li>Storyboard or lighting sequence</li><li>Materials and fabrication request</li><li>Tinkercad link, STL, or SVG when needed</li><li>One prototype question with an observable success condition and three-trial plan</li><li>Individual contribution, concern, and next-action reflection</li></ol>
<div style="padding:16px;background:#edf9f8;border-radius:12px;"><strong>Schedule:</strong> submit by Monday, October 19. Mentors review October 20. Demonstrate at lunch in Room 14 on Wednesday, October 21.</div>
'@;
    Links=@(@{Label='Phase 2 deliverables';Url="$baseUrl/phase-2-prototype.html"},@{Label='Lunch checkpoint guide';Url="$baseUrl/lunch-checkpoints.html"})
  },
  [ordered]@{
    Slug='phase-2-pathways'; Title='Design Ready in Your Pathway'; Eyebrow='Phase 2';
    Lede='Make the technology, materials, user experience, and first November test understandable before materials are released.';
    Content=@'
<h2 style="color:#168b88;">Robotics — 1st year or 3rd-year choice</h2><p>Show the future user and need, input → decision → at least two outputs → reset system, three-to-five-frame visitor storyboard, Hummingbird parts, physical structure, movement, service access, partner roles, and first interaction or mechanism test.</p>
<h2 style="color:#ef6a74;">Wearables — 2nd year or 3rd-year choice</h2><p>Show the shirt front and back, hat design, battery, micro:bit, LEDs, connections, removable electronics, planned light behavior, comfort and movement considerations, and first circuit or material test.</p>
<p><strong>No finished physical prototype is required in October.</strong> Students may use iPads or classroom Windows laptops for Canvas, Tinkercad, diagrams, code planning, and evidence preparation.</p>
'@;
    Links=@(@{Label='Wearable proposal guide';Url="$baseUrl/wearable-design-proposal.html"},@{Label='Robotics proposal guide';Url="$baseUrl/robotics-design-proposal.html"},@{Label='Fabrication Lab';Url="$baseUrl/fabrication-lab.html"})
  },
  [ordered]@{
    Slug='phase-3-overview'; Title='Phase 3: Design What’s Next'; Eyebrow='Monday, November 9, 2026';
    Lede='Build and test the planned quick prototype, then use that evidence to begin careful major construction while keeping important parts inspectable and repairable.';
    Content=@'
<h2 style="color:#5f3dc4;">Start only when</h2><ul><li>Your October Design Ready package is green or the named revision is complete.</li><li>Your prototype question, success condition, and three-trial plan are ready.</li><li>Prototype materials are released by a mentor.</li><li>You know what evidence must be captured before permanent construction.</li></ul>
<h2 style="color:#5f3dc4;">Workday sequence</h2><ol><li>Build the smallest useful test.</li><li>Run the planned trials and record the real result.</li><li>Change one variable and retest.</li><li>Receive mentor clearance for permanent construction.</li><li>Complete the named major-build milestone.</li></ol>
<h2 style="color:#5f3dc4;">End with</h2><p>Prototype evidence, safe and documented major-build progress, an honest status of on track, targeted repair, or blocked, and an exact first December test or repair.</p>
'@;
    Links=@(@{Label='Phase 3 workday guide';Url="$baseUrl/phase-3-build.html"},@{Label='Build progress evidence';Url="$baseUrl/build-progress-evidence.html"})
  },
  [ordered]@{
    Slug='phase-3-pathways'; Title='Prototype and Build in Your Pathway'; Eyebrow='Phase 3';
    Lede='Test the most important uncertainty first, then build the approved plan, document meaningful changes, and preserve service access.';
    Content=@'
<h2 style="color:#168b88;">Robotics — 1st year or 3rd-year choice</h2><p>Prove one critical input, output, or mechanism behavior. After mentor clearance, construct the durable physical form, mechanisms, accessible mounts, and first complete programmed interaction.</p>
<h2 style="color:#ef6a74;">Wearables — 2nd year or 3rd-year choice</h2><p>Complete a paint, material, or one-light circuit test. After mentor clearance, transfer the approved design, begin major denim-shirt painting, and construct the planned sewn circuit.</p>
'@;
    Links=@(@{Label='Wearable build guide';Url="$baseUrl/wearable-build.html"},@{Label='Robotics build guide';Url="$baseUrl/robotics-build.html"})
  },
  [ordered]@{
    Slug='phase-4-overview'; Title='Phase 4: Build & Test'; Eyebrow='Monday, December 7, 2026';
    Lede='Continue only critical construction, test one subsystem, improve one problem with evidence, and leave a January restart plan.';
    Content=@'
<h2 style="color:#5f3dc4;">Troubleshooting loop</h2><ol><li>Observe the exact behavior.</li><li>Power off before touching hardware.</li><li>Choose one likely variable.</li><li>Change only that variable.</li><li>Repeat the same test and record the comparison.</li></ol>
<h2 style="color:#5f3dc4;">Winter-storage gate</h2><p>Power is off; battery action is mentor-approved; parts are contained and counted; code is backed up; condition and storage location are photographed; the January first action begins with a specific verb.</p><p><strong>January 13 Restart Ready lunch:</strong> confirm the current status, code backup, materials needs, blocker, and three priorities for January 25. No construction is required during winter break.</p>
'@;
    Links=@(@{Label='Phase 4 workday guide';Url="$baseUrl/phase-4-test.html"},@{Label='Mid-build evidence guide';Url="$baseUrl/mid-build-evidence.html"})
  },
  [ordered]@{
    Slug='phase-4-pathways'; Title='Test and Store Your Pathway'; Eyebrow='Phase 4';
    Lede='Subsystem testing protects January integration from hidden problems.';
    Content=@'
<h2 style="color:#168b88;">Robotics — 1st year or 3rd-year choice</h2><p>Test the input, each output, mechanism, and reset separately; repair one variable; prepare a clear integration order; and count the numbered kit before storage.</p>
<h2 style="color:#ef6a74;">Wearables — 2nd year or 3rd-year choice</h2><p>Inspect and test the denim shirt, make one evidence-based repair, and create a non-electronic removable hat-mounting mockup. Do not cut or permanently install the final WS2812B strip.</p>
'@;
    Links=@(@{Label='Wearable test guide';Url="$baseUrl/wearable-test.html"},@{Label='Robotics test guide';Url="$baseUrl/robotics-test.html"})
  },
  [ordered]@{
    Slug='phase-5-overview'; Title='Phase 5: Build the Future'; Eyebrow='January 13 lunch checkpoint · Monday, January 25 workday';
    Lede='Restart safely, integrate systems in layers, test the complete experience, and make one meaningful evidence-based redesign.';
    Content=@'
<h2 style="color:#5f3dc4;">Restart Ready lunch · January 13</h2><p>Show the December project status, latest test, code backup, missing or damaged materials, three priorities, blocker, and individual commitment.</p>
<h2 style="color:#5f3dc4;">Integration sequence · January 25</h2><ol><li>Compare with the December photo, inventory, blocker, and restart card.</li><li>Use the lunch-checkpoint status to begin ready to integrate, repair first, or blocked.</li><li>Connect one proven system layer and test before adding the next.</li><li>Write a realistic complete-system success condition.</li><li>Run the baseline experience from setup through safe reset/shutdown.</li><li>Redesign the weakest high-impact variable and repeat the test fairly.</li><li>Rank February work as critical, important, or optional.</li></ol>
'@;
    Links=@(@{Label='Phase 5 workday guide';Url="$baseUrl/phase-5-integrate.html"},@{Label='Checkpoint 3 guide';Url="$baseUrl/test-learn-redesign.html"})
  },
  [ordered]@{
    Slug='phase-5-pathways'; Title='Complete-System Integration'; Eyebrow='Phase 5';
    Lede='The complete-system test should match the experience a wearer or visitor will actually have.';
    Content=@'
<h2 style="color:#168b88;">Robotics — 1st year or 3rd-year choice</h2><p>Connect the stable structure, input, output 1, output 2/mechanism, and reset; use the assigned three-word BirdBlox device; run five realistic visitor trials; and rotate Driver/Navigator.</p>
<h2 style="color:#ef6a74;">Wearables — 2nd year or 3rd-year choice</h2><p>Finish the shirt, install only mentor-released removable hat electronics, program Button A, Button B, and A+B reset in MakeCode, test on a stand before wearing, and evaluate comfort, balance, access, function, theme clarity, and safe removal.</p>
'@;
    Links=@(@{Label='Wearable integration guide';Url="$baseUrl/wearable-integration.html"},@{Label='Robotics integration guide';Url="$baseUrl/robotics-integration.html"})
  },
  [ordered]@{
    Slug='phase-6-overview'; Title='Phase 6: Step Into the Future'; Eyebrow='February 10 lunch checkpoint · Monday, February 22 workday';
    Lede='Finish only critical work, pass formal inspection and two reliability trials, document the project, rehearse, and pack for the public.';
    Content=@'
<h2 style="color:#5f3dc4;">Gala Path lunch · February 10</h2><p>Show the current project, latest complete-system test, ranked punch list, repair request, draft project card, safe backup plan, and individual presentation responsibility before the February break.</p>
<h2 style="color:#5f3dc4;">February 22 priority</h2><p>Critical safety and function work comes first. Important clarity, documentation, repairability, appearance, setup, and rehearsal follow. Optional decoration and new features are deferred.</p>
<h2 style="color:#5f3dc4;">Gala-ready proof</h2><ul><li>Formal safety and function inspection</li><li>Two complete passing trials including reset and shutdown</li><li>Safe backup or modified demonstration</li><li>Final project card and 45-second engineering explanation</li><li>Every student practices a speaking and operating role</li><li>Labeled setup, pack-down, code, power, parts, garments, kit, and transport</li></ul>
'@;
    Links=@(@{Label='Phase 6 workday guide';Url="$baseUrl/phase-6-gala-ready.html"},@{Label='Checkpoint 4 guide';Url="$baseUrl/gala-ready-evidence.html"})
  },
  [ordered]@{
    Slug='phase-6-pathways'; Title='Inspection, Reliability, and Rehearsal'; Eyebrow='Phase 6';
    Lede='A single successful demonstration is not enough. Pass the complete routine twice and practice the safe recovery plan.';
    Content=@'
<h2 style="color:#168b88;">Robotics Gala readiness — 1st year or 3rd-year choice</h2><p>Inspect stability, motion, input, two outputs, startup, reset, repairability, and numbered kit. Both partners pass as Driver, then rotate Presenter/Greeter and Operator/Resetter roles.</p>
<h2 style="color:#ef6a74;">Wearable Gala readiness — 2nd year or 3rd-year choice</h2><p>Inspect shirt and hat power, function, comfort, fit, repairability, and theme clarity. Test on the stand before wearing. Rehearse the fashion-show walk, operation, explanation, shutdown, and safe garment/power packing.</p>
'@;
    Links=@(@{Label='Wearable Gala guide';Url="$baseUrl/wearable-gala-ready.html"},@{Label='Robotics Gala guide';Url="$baseUrl/robotics-gala-ready.html"})
  },
  [ordered]@{
    Slug='stauffer-gala'; Title='Stauffer Femineers Gala'; Eyebrow='Monday, March 1, 2027 — Stauffer Library';
    Lede='Present the first public version, follow the safe demonstration plan, and observe how real visitors experience the work.';
    Content=@'
<h2 style="color:#5f3dc4;">Before the audience arrives</h2><ul><li>Use the approved layout, garment rack, robotics table map, labels, project cards, and visitor boundaries.</li><li>Run the short setup check and confirm the safe backup plan.</li><li>Do not make unapproved repairs, substitutions, or power changes at the event.</li></ul>
<h2 style="color:#5f3dc4;">During and after</h2><p>Every student speaks and operates. Record one visitor response, one reliability observation, and one focused change worth considering before the District Gala.</p>
'@;
    Links=@(@{Label='Review the program roadmap';Url="$baseUrl/program-roadmap.html"},@{Label='Review Gala-ready evidence';Url="$baseUrl/gala-ready-evidence.html"})
  },
  [ordered]@{
    Slug='district-gala'; Title='District Femineers Gala'; Eyebrow='Thursday evening, March 18, 2027 — Downey High';
    Lede='Present the polished project, hear from guest speakers, and celebrate with Femineers from across the district at an evening showcase to remember.';
    Content=@'
<h2 style="color:#5f3dc4;">Between Galas</h2><ul><li>Review real-world Stauffer reliability and visitor evidence.</li><li>Approve only focused repairs or clarity improvements.</li><li>Repeat the affected reliability test after every change.</li><li>Update the project card, code backup, labels, and transport plan.</li></ul>
<div style="padding:18px;background:#fff3c9;border-radius:12px;"><strong>Evening celebration:</strong> the District Gala includes student projects, guest speakers, and hors d’oeuvres provided by Culinary Arts. Exact arrival time, program schedule, and transportation details will be shared when confirmed.</div>
<h2 style="color:#5f3dc4;">Final reflection</h2><p>Select the strongest evidence from the year and explain how your idea, skills, testing habits, teamwork or independence, and view of your future changed.</p>
'@;
    Links=@(@{Label='Open the program roadmap';Url="$baseUrl/program-roadmap.html"})
  },
  [ordered]@{
    Slug='mentor-playbook'; Title='Mentor Lesson-Plan Playbook'; Eyebrow='Mentor planning — unpublished module';
    Lede='Preparation, exact Room 14 agendas, lunch-checkpoint review, student reflection, mentor debrief, and next-phase preparation for five full workdays.';
    Content=@'
<h2 style="color:#5f3dc4;">Use before each workday</h2><ol><li>Review the preparation list and function-test equipment.</li><li>Open the student hub and pathway guides for the current phase.</li><li>Confirm Canvas assignment, evidence model, and mentor gate.</li><li>Assign stations, roles, repair/inspect areas, storage, and cleanup.</li><li>After dismissal, complete the mentor debrief and prepare the next phase.</li></ol><h2 style="color:#168b88;">Use before each lunch checkpoint</h2><ol><li>Review Canvas submissions in advance.</li><li>Assign green, yellow, or red status.</li><li>Prepare one named revision for yellow projects.</li><li>Prioritize red projects for mentor conferences.</li><li>Prepare ingredient-labeled treats and nonfood choices.</li></ol>
<p><strong>Scheduling principle:</strong> do not depend on whole-program Saturday workdays. Use targeted school-day, lunch, advisory, or supervised after-school support when available.</p>
'@;
    Links=@(@{Label='Open the full mentor playbook';Url="$baseUrl/mentor-lesson-plans.html"},@{Label='Open lunch checkpoints';Url="$baseUrl/lunch-checkpoints.html"},@{Label='Open the roadmap';Url="$baseUrl/program-roadmap.html"})
  },
  [ordered]@{
    Slug='canvas-launch-checklist'; Title='Canvas Launch Checklist'; Eyebrow='Mentor planning — unpublished module';
    Lede='Complete these course-specific decisions after import and before publishing to students.';
    Content=@'
<ol><li>Confirm the five full workdays and three lunch checkpoints.</li><li>Review module dates, names, Room 14 schedule, and the invitation-only December 2 Project Rescue lunch.</li><li>Add final due dates and availability dates to all eight assignments, including October 19 for the Design Ready package if approved.</li><li>Confirm whether every assignment remains 10 points or uses a different grading plan.</li><li>Review allowed file types and media size limits on student iPads.</li><li>Add district-required policies, accommodations, food-reward guidance, and contact information.</li><li>Test every website button and assignment in Student View.</li><li>Publish pages, assignments, and modules only after the audit.</li><li>Publish the course when enrollment and communication are ready.</li></ol>
'@;
    Links=@(@{Label='Open the student website';Url="$baseUrl/index.html"})
  }
)

$assignments = @(
  [ordered]@{
    Slug='checkpoint-1-proposal'; Title='Checkpoint 1: Approved Project Proposal'; Points=10; Position=1; Guide="$baseUrl/canvas-checkpoint-1.html";
    Content=@'
<h2 style="color:#168b88;">Submit</h2><ul><li>Future user, need, identity, or opportunity</li><li>Three distinct ideas and evidence-based selection</li><li>Complete labeled sketch(es), materials, and system behavior</li><li>Safety, comfort/stability, access, and repair plan</li><li>First prototype question and success condition</li><li>Mentor approval status</li></ul>
<p><strong>Wearable:</strong> one individual proposal covers both the LED denim shirt and programmable bucket hat.</p><p><strong>Robotics:</strong> submit one shared team packet plus an individual reflection from each partner.</p>
'@
  },
  [ordered]@{
    Slug='prototype-evidence'; Title='Phase 2: Design Ready Package'; Points=10; Position=2; Guide="$baseUrl/phase-2-prototype.html";
    Content=@'
<h2 style="color:#168b88;">Submit by Monday, October 19</h2><ul><li>Approved proposal and every requested revision</li><li>Labeled project drawing</li><li>Wearable circuit diagram or Robotics input → decision → at least two outputs → reset system map</li><li>Storyboard or lighting sequence</li><li>Materials and fabrication request</li><li>Tinkercad link, STL, or SVG when needed</li><li>One prototype question, observable success condition, and three-trial plan for November 9</li><li>Individual contribution, concern, and next-action reflection</li></ul>
<p><strong>October 21 lunch demonstration:</strong> show the evidence in sixty seconds, explain one important decision, name the first November test, and state the next action. Robotics partners both speak and explain different parts.</p>
'@
  },
  [ordered]@{
    Slug='checkpoint-2-build-progress'; Title='Checkpoint 2: Prototype + Build Progress #1'; Points=10; Position=3; Guide="$baseUrl/build-progress-evidence.html";
    Content=@'
<h2 style="color:#168b88;">Submit</h2><ul><li>Prototype question and success condition</li><li>Three-trial result, one named change, and matching retest evidence</li><li>Mentor clearance or documented blocker</li><li>Overall project photo</li><li>Close-up of the most important completed construction</li><li>Comparison with the October Design Ready plan</li><li>Meaningful construction change and reason</li><li>Status: on track, targeted repair, or blocked</li><li>Exact first December test or repair</li></ul>
'@
  },
  [ordered]@{
    Slug='phase-4-mid-build'; Title='Phase 4: Mid-Build Test + January Plan'; Points=10; Position=4; Guide="$baseUrl/mid-build-evidence.html";
    Content=@'
<h2 style="color:#168b88;">Submit</h2><ul><li>Starting-condition photo before repair</li><li>Named subsystem and observable success condition</li><li>Honest first result</li><li>One controlled change</li><li>Fair retest and before/after explanation</li><li>Current blocker and actionable January first step</li><li>Power status, loose parts, code backup, and storage location</li><li>Mentor winter-storage approval</li></ul>
'@
  },
  [ordered]@{
    Slug='checkpoint-3-redesign'; Title='Checkpoint 3: Test, Learn, Redesign'; Points=10; Position=5; Guide="$baseUrl/test-learn-redesign.html";
    Content=@'
<h2 style="color:#168b88;">Submit</h2><ul><li>Complete-system success condition written before testing</li><li>Baseline from setup through safe reset/shutdown</li><li>Specific evidence and learning claim</li><li>One meaningful redesign and reason</li><li>Fair retest under the original condition</li><li>Conclusion: better, worse, unchanged, or still uncertain</li><li>Critical, important, and optional February punch list</li><li>Mentor readiness status</li></ul>
<p>Robotics teams include shared evidence and an individual contribution/learning response from each partner.</p>
'@
  },
  [ordered]@{
    Slug='checkpoint-4-gala-ready'; Title='Checkpoint 4: Gala Ready'; Points=10; Position=6; Guide="$baseUrl/gala-ready-evidence.html";
    Content=@'
<h2 style="color:#168b88;">Submit</h2><ul><li>Final overall and labeled detail photos</li><li>Mentor inspection status</li><li>Two passing reliability trials and one complete demonstration video</li><li>Final project card and 45-second engineering explanation</li><li>Safe backup or modified demonstration</li><li>Final code backup name</li><li>Setup, reset/shutdown, pack-down, labels, and inventory</li></ul>
'@
  },
  [ordered]@{
    Slug='stauffer-gala-reflection'; Title='Checkpoint 5: Stauffer Gala Reflection'; Points=10; Position=7; Guide="$baseUrl/program-roadmap.html";
    Content=@'
<h2 style="color:#168b88;">Respond individually</h2><ol><li>What worked reliably with real visitors?</li><li>What failure, confusion, comfort issue, or unexpected use did you observe?</li><li>What evidence supports one focused change before the District Gala?</li><li>What will you keep exactly the same?</li><li>What did you learn about presenting engineering work publicly?</li></ol><p>Include one approved photo, short video, observation record, or visitor-response note when available.</p>
'@
  },
  [ordered]@{
    Slug='final-portfolio-reflection'; Title='Final Portfolio + District Gala Reflection'; Points=10; Position=8; Guide="$baseUrl/program-roadmap.html";
    Content=@'
<h2 style="color:#168b88;">Submit your strongest evidence</h2><ul><li>Approved proposal</li><li>Prototype and first test</li><li>Major-build progress</li><li>Most important failure or challenge</li><li>Evidence-based redesign and retest</li><li>Final project and public presentation</li></ul>
<h2 style="color:#168b88;">Reflect individually</h2><ol><li>How did your idea change from proposal to final project?</li><li>Which skill or engineering habit improved most?</li><li>How did you respond when evidence disagreed with your expectation?</li><li>What did you contribute independently or to your team?</li><li>What future interest, identity, or possibility do you see differently now?</li></ol>
'@
  }
)

$modules = @(
  [ordered]@{Slug='orientation';Title='Start Here: Limitless Course Orientation';State='active';Items=@(
    @{Type='Page';Ref='welcome';Title='Welcome to Limitless: Designed by Her'},
    @{Type='Page';Ref='roadmap';Title='Program Roadmap and Important Dates'},
    @{Type='Page';Ref='lunch-checkpoints';Title='Lunch Checkpoints and Milestone Treats'},
    @{Type='Page';Ref='choose-path';Title='Know Your Assigned Project Pathway'},
    @{Type='Page';Ref='safety-evidence';Title='Safety, Supplies, and Evidence Rules'}
  )},
  [ordered]@{Slug='phase-1';Title='Phase 1 — Imagine the Future — September 21';State='active';Items=@(
    @{Type='Page';Ref='phase-1-overview';Title='Phase 1 Overview'},
    @{Type='Page';Ref='phase-1-tools';Title='Meet the Technology'},
    @{Type='Page';Ref='phase-1-proposal';Title='Prepare Your Approved Design Proposal'},
    @{Type='Assignment';Ref='checkpoint-1-proposal';Title='Checkpoint 1: Approved Project Proposal'}
  )},
  [ordered]@{Slug='phase-2';Title='Phase 2 — Arrive Ready to Build — October Canvas + October 21 Lunch';State='active';Items=@(
    @{Type='Page';Ref='phase-2-overview';Title='Phase 2 Design Ready Overview'},
    @{Type='Page';Ref='phase-2-pathways';Title='Design Ready in Your Pathway'},
    @{Type='Assignment';Ref='prototype-evidence';Title='Phase 2: Design Ready Package'}
  )},
  [ordered]@{Slug='phase-3';Title='Phase 3 — Design What’s Next — November 9';State='active';Items=@(
    @{Type='Page';Ref='phase-3-overview';Title='Phase 3 Overview'},
    @{Type='Page';Ref='phase-3-pathways';Title='Prototype and Build in Your Pathway'},
    @{Type='Assignment';Ref='checkpoint-2-build-progress';Title='Checkpoint 2: Prototype + Build Progress #1'}
  )},
  [ordered]@{Slug='phase-4';Title='Phase 4 — Build & Test — December 7';State='active';Items=@(
    @{Type='Page';Ref='phase-4-overview';Title='Phase 4 Overview'},
    @{Type='Page';Ref='phase-4-pathways';Title='Test and Store Your Pathway'},
    @{Type='Assignment';Ref='phase-4-mid-build';Title='Mid-Build Test + January Plan'}
  )},
  [ordered]@{Slug='phase-5';Title='Phase 5 — Build the Future — January 13 Lunch + January 25 Workday';State='active';Items=@(
    @{Type='Page';Ref='phase-5-overview';Title='Phase 5 Overview'},
    @{Type='Page';Ref='phase-5-pathways';Title='Complete-System Integration'},
    @{Type='Assignment';Ref='checkpoint-3-redesign';Title='Checkpoint 3: Test, Learn, Redesign'}
  )},
  [ordered]@{Slug='phase-6';Title='Phase 6 — Step Into the Future — February 10 Lunch + February 22 Workday';State='active';Items=@(
    @{Type='Page';Ref='phase-6-overview';Title='Phase 6 Overview'},
    @{Type='Page';Ref='phase-6-pathways';Title='Inspection, Reliability, and Rehearsal'},
    @{Type='Assignment';Ref='checkpoint-4-gala-ready';Title='Checkpoint 4: Gala Ready'}
  )},
  [ordered]@{Slug='galas';Title='Galas, Reflection, and Final Portfolio';State='active';Items=@(
    @{Type='Page';Ref='stauffer-gala';Title='Stauffer Femineers Gala — March 1'},
    @{Type='Assignment';Ref='stauffer-gala-reflection';Title='Checkpoint 5: Stauffer Gala Reflection'},
    @{Type='Page';Ref='district-gala';Title='District Femineers Gala — March 18'},
    @{Type='Assignment';Ref='final-portfolio-reflection';Title='Final Portfolio + District Gala Reflection'}
  )},
  [ordered]@{Slug='mentor';Title='Mentor Planning — Keep Unpublished';State='unpublished';Items=@(
    @{Type='Page';Ref='mentor-playbook';Title='Mentor Lesson-Plan Playbook'},
    @{Type='Page';Ref='canvas-launch-checklist';Title='Canvas Launch Checklist'}
  )}
)

$outputRoot = [System.IO.Path]::GetFullPath($OutputDirectory)
$workspaceRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (-not $outputRoot.StartsWith($workspaceRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "Output directory must remain inside the Femineers workspace: $workspaceRoot"
}

$buildRoot = Join-Path $outputRoot '.build'
$packagePath = Join-Path $outputRoot 'Stauffer-Femineers-Limitless-2026-27.imscc'
$checksumPath = "$packagePath.sha256.txt"

if (Test-Path -LiteralPath $buildRoot) { Remove-Item -LiteralPath $buildRoot -Recurse -Force }
if (Test-Path -LiteralPath $packagePath) { Remove-Item -LiteralPath $packagePath -Force }
if (Test-Path -LiteralPath $checksumPath) { Remove-Item -LiteralPath $checksumPath -Force }

New-Item -ItemType Directory -Path (Join-Path $buildRoot 'course_settings') -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $buildRoot 'wiki_content') -Force | Out-Null

$courseId = New-StableId "course:$courseCode"
$assignmentGroupId = New-StableId 'assignment-group:femineers-evidence'
$pageIds = @{}
$assignmentIds = @{}
$moduleIds = @{}

foreach ($page in $pages) {
  $id = New-StableId "page:$($page.Slug)"
  $pageIds[$page.Slug] = $id
  Write-Utf8 (Join-Path $buildRoot "wiki_content/$($page.Slug).html") (New-CanvasPageHtml $page $id)
}

foreach ($assignment in $assignments) {
  $id = New-StableId "assignment:$($assignment.Slug)"
  $assignmentIds[$assignment.Slug] = $id
  $folder = Join-Path $buildRoot $id
  New-Item -ItemType Directory -Path $folder -Force | Out-Null
  Write-Utf8 (Join-Path $folder 'body.html') (New-AssignmentHtml $assignment)
  $settings = @"
<?xml version="1.0" encoding="UTF-8"?>
<assignment identifier="$id" xmlns="$canvasNamespace" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="$canvasNamespace $canvasSchema">
  <title>$(ConvertTo-XmlText $assignment.Title)</title>
  <assignment_group_identifierref>$assignmentGroupId</assignment_group_identifierref>
  <workflow_state>active</workflow_state>
  <points_possible>$($assignment.Points)</points_possible>
  <grading_type>points</grading_type>
  <submission_types>online_text_entry,online_url,online_upload,media_recording</submission_types>
  <position>$($assignment.Position)</position>
  <peer_reviews>false</peer_reviews>
  <automatic_peer_reviews>false</automatic_peer_reviews>
  <anonymous_peer_reviews>false</anonymous_peer_reviews>
  <allowed_attempts>-1</allowed_attempts>
</assignment>
"@
  Write-Utf8 (Join-Path $folder 'assignment_settings.xml') $settings
}

foreach ($module in $modules) {
  $moduleIds[$module.Slug] = New-StableId "module:$($module.Slug)"
}

$courseSettings = @"
<?xml version="1.0" encoding="UTF-8"?>
<course identifier="$courseId" xmlns="$canvasNamespace" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="$canvasNamespace $canvasSchema">
  <title>$(ConvertTo-XmlText $courseTitle)</title>
  <course_code>$courseCode</course_code>
  <default_view>modules</default_view>
  <time_zone>America/Los_Angeles</time_zone>
</course>
"@
Write-Utf8 (Join-Path $buildRoot 'course_settings/course_settings.xml') $courseSettings

$assignmentGroups = @"
<?xml version="1.0" encoding="UTF-8"?>
<assignmentGroups xmlns="$canvasNamespace" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="$canvasNamespace $canvasSchema">
  <assignmentGroup identifier="$assignmentGroupId">
    <title>Femineers Evidence</title>
    <position>1</position>
    <group_weight>100</group_weight>
  </assignmentGroup>
</assignmentGroups>
"@
Write-Utf8 (Join-Path $buildRoot 'course_settings/assignment_groups.xml') $assignmentGroups

$flag = @'
Q: What did the panda say when he was forced out of his natural habitat?
A: This is un-BEAR-able
'@
Write-Utf8 (Join-Path $buildRoot 'course_settings/canvas_export.txt') $flag

$syllabus = @"
<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><title>Syllabus</title></head><body>
<div style="max-width:850px;margin:0 auto;font-family:Arial,Helvetica,sans-serif;color:#25223a;line-height:1.55;">
<h1>$courseTitle</h1><p><strong>Theme:</strong> Limitless: Designed by Her</p><p><strong>Tagline:</strong> Imagine it. Build it. Become it.</p>
<p>Participation year shapes each student’s pathway: first-year Femineers complete Creative Robotics in teams of two, second-year Femineers complete Wearable Technology individually, and third-year Femineers choose either pathway. Six school-day work sessions move each project through proposal, prototype, major build, subsystem testing, integration, redesign, public-readiness inspection, rehearsal, and reflection.</p>
<p><strong>Mentors:</strong> Tri Tansopalucks, Jennifer Frausto, and Stephanie Chavez</p>
<p><strong>Workday location:</strong> Room 14, Monday bell schedule, 8:00 a.m.–2:41 p.m.</p>
<p><strong>Website:</strong> <a href="$baseUrl/index.html">$baseUrl</a></p>
<p>Detailed attendance, behavior, grading, accommodations, communication, and district policies should be added by the course instructors before publication.</p>
</div></body></html>
"@
Write-Utf8 (Join-Path $buildRoot 'course_settings/syllabus.html') $syllabus

$moduleXml = [System.Text.StringBuilder]::new()
[void]$moduleXml.AppendLine('<?xml version="1.0" encoding="UTF-8"?>')
[void]$moduleXml.AppendLine(('<modules xmlns="{0}" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="{0} {1}">' -f $canvasNamespace, $canvasSchema))
$modulePosition = 0
foreach ($module in $modules) {
  $modulePosition++
  $moduleId = $moduleIds[$module.Slug]
  [void]$moduleXml.AppendLine(('  <module identifier="{0}">' -f $moduleId))
  [void]$moduleXml.AppendLine("    <title>$(ConvertTo-XmlText $module.Title)</title>")
  [void]$moduleXml.AppendLine("    <workflow_state>$($module.State)</workflow_state>")
  [void]$moduleXml.AppendLine("    <position>$modulePosition</position>")
  [void]$moduleXml.AppendLine('    <require_sequential_progress>true</require_sequential_progress>')
  [void]$moduleXml.AppendLine('    <items>')
  $itemPosition = 0
  $moduleItemRecords = @()
  foreach ($item in $module.Items) {
    $itemPosition++
    $itemId = New-StableId "module-item:$($module.Slug):${itemPosition}:$($item.Type):$($item.Ref)"
    $resourceId = if ($item.Type -eq 'Page') { $pageIds[$item.Ref] } else { $assignmentIds[$item.Ref] }
    $contentType = if ($item.Type -eq 'Page') { 'WikiPage' } else { 'Assignment' }
    $requirement = if ($item.Type -eq 'Page') { 'must_view' } else { 'must_submit' }
    $moduleItemRecords += @{Id=$itemId;Requirement=$requirement}
    [void]$moduleXml.AppendLine(('      <item identifier="{0}">' -f $itemId))
    [void]$moduleXml.AppendLine("        <content_type>$contentType</content_type>")
    [void]$moduleXml.AppendLine('        <workflow_state>active</workflow_state>')
    [void]$moduleXml.AppendLine("        <title>$(ConvertTo-XmlText $item.Title)</title>")
    [void]$moduleXml.AppendLine("        <identifierref>$resourceId</identifierref>")
    [void]$moduleXml.AppendLine("        <position>$itemPosition</position>")
    [void]$moduleXml.AppendLine('        <indent>0</indent>')
    [void]$moduleXml.AppendLine('      </item>')
  }
  [void]$moduleXml.AppendLine('    </items>')
  [void]$moduleXml.AppendLine('    <completionRequirements>')
  foreach ($record in $moduleItemRecords) {
    [void]$moduleXml.AppendLine(('      <completionRequirement type="{0}"><identifierref>{1}</identifierref></completionRequirement>' -f $record.Requirement, $record.Id))
  }
  [void]$moduleXml.AppendLine('    </completionRequirements>')
  [void]$moduleXml.AppendLine('  </module>')
}
[void]$moduleXml.AppendLine('</modules>')
Write-Utf8 (Join-Path $buildRoot 'course_settings/module_meta.xml') $moduleXml.ToString()

$manifest = [System.Text.StringBuilder]::new()
[void]$manifest.AppendLine('<?xml version="1.0" encoding="UTF-8"?>')
[void]$manifest.AppendLine(('<manifest identifier="{0}" xmlns="{1}" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:lomimscc="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="{1} http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_imscp_v1p2_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lommanifest_v1p0.xsd">' -f (New-StableId 'manifest:stauffer-femineers-2627'), $ccNamespace))
[void]$manifest.AppendLine('  <metadata>')
[void]$manifest.AppendLine('    <schema>IMS Common Cartridge</schema>')
[void]$manifest.AppendLine('    <schemaversion>1.1.0</schemaversion>')
[void]$manifest.AppendLine("    <lomimscc:lom><lomimscc:general><lomimscc:title><lomimscc:string>$(ConvertTo-XmlText $courseTitle)</lomimscc:string></lomimscc:title></lomimscc:general></lomimscc:lom>")
[void]$manifest.AppendLine('  </metadata>')
[void]$manifest.AppendLine('  <organizations>')
[void]$manifest.AppendLine('    <organization identifier="org_1" structure="rooted-hierarchy">')
[void]$manifest.AppendLine('      <item identifier="LearningModules">')
$modulePosition = 0
foreach ($module in $modules) {
  $modulePosition++
  $moduleId = $moduleIds[$module.Slug]
  [void]$manifest.AppendLine(('        <item identifier="{0}">' -f $moduleId))
  [void]$manifest.AppendLine("          <title>$(ConvertTo-XmlText $module.Title)</title>")
  $itemPosition = 0
  foreach ($item in $module.Items) {
    $itemPosition++
    $itemId = New-StableId "module-item:$($module.Slug):${itemPosition}:$($item.Type):$($item.Ref)"
    $resourceId = if ($item.Type -eq 'Page') { $pageIds[$item.Ref] } else { $assignmentIds[$item.Ref] }
    [void]$manifest.AppendLine(('          <item identifier="{0}" identifierref="{1}"><title>{2}</title></item>' -f $itemId, $resourceId, (ConvertTo-XmlText $item.Title)))
  }
  [void]$manifest.AppendLine('        </item>')
}
[void]$manifest.AppendLine('      </item>')
[void]$manifest.AppendLine('    </organization>')
[void]$manifest.AppendLine('  </organizations>')
[void]$manifest.AppendLine('  <resources>')
foreach ($page in $pages) {
  $id = $pageIds[$page.Slug]
  $href = "wiki_content/$($page.Slug).html"
  [void]$manifest.AppendLine(('    <resource identifier="{0}" type="webcontent" href="{1}"><file href="{1}"/></resource>' -f $id, $href))
}
foreach ($assignment in $assignments) {
  $id = $assignmentIds[$assignment.Slug]
  $bodyHref = "$id/body.html"
  $settingsHref = "$id/assignment_settings.xml"
  [void]$manifest.AppendLine(('    <resource identifier="{0}" type="{1}" href="{2}"><file href="{2}"/><file href="{3}"/></resource>' -f $id, $lorType, $bodyHref, $settingsHref))
}
[void]$manifest.AppendLine(('    <resource identifier="{0}" type="{1}" href="course_settings/canvas_export.txt"><file href="course_settings/canvas_export.txt"/><file href="course_settings/course_settings.xml"/><file href="course_settings/module_meta.xml"/><file href="course_settings/assignment_groups.xml"/></resource>' -f $courseId, $lorType))
[void]$manifest.AppendLine(('    <resource identifier="{0}_syllabus" type="{1}" href="course_settings/syllabus.html" intendeduse="syllabus"><file href="course_settings/syllabus.html"/></resource>' -f $courseId, $lorType))
[void]$manifest.AppendLine('  </resources>')
[void]$manifest.AppendLine('</manifest>')
Write-Utf8 (Join-Path $buildRoot 'imsmanifest.xml') $manifest.ToString()

# Validate source XML and identifier references before packaging.
$xmlFiles = Get-ChildItem -LiteralPath $buildRoot -Recurse -File -Filter *.xml
foreach ($xmlFile in $xmlFiles) { [void][xml](Get-Content -Raw -Encoding UTF8 -LiteralPath $xmlFile.FullName) }
$manifestXml = [xml](Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $buildRoot 'imsmanifest.xml'))
$resourceIds = @{}
foreach ($node in $manifestXml.SelectNodes("//*[local-name()='resource']")) { $resourceIds[$node.identifier] = $true }
foreach ($node in $manifestXml.SelectNodes("//*[local-name()='item'][@identifierref]")) {
  if (-not $resourceIds.ContainsKey($node.identifierref)) { throw "Manifest identifierref does not resolve: $($node.identifierref)" }
}
$moduleMetaXml = [xml](Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $buildRoot 'course_settings/module_meta.xml'))
foreach ($node in $moduleMetaXml.SelectNodes("//*[local-name()='item']/*[local-name()='identifierref']")) {
  if (-not $resourceIds.ContainsKey($node.InnerText)) { throw "Module identifierref does not resolve: $($node.InnerText)" }
}
foreach ($fileNode in $manifestXml.SelectNodes("//*[local-name()='file']")) {
  $target = Join-Path $buildRoot ($fileNode.href -replace '/', [System.IO.Path]::DirectorySeparatorChar)
  if (-not (Test-Path -LiteralPath $target)) { throw "Manifest file is missing: $($fileNode.href)" }
}

$writeArchive = [System.IO.Compression.ZipFile]::Open($packagePath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
  foreach ($sourceFile in (Get-ChildItem -LiteralPath $buildRoot -Recurse -File | Sort-Object FullName)) {
    $relativePath = $sourceFile.FullName.Substring($buildRoot.Length).TrimStart([char]'\', [char]'/') -replace '\\', '/'
    [void][System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($writeArchive, $sourceFile.FullName, $relativePath, [System.IO.Compression.CompressionLevel]::Optimal)
  }
}
finally {
  $writeArchive.Dispose()
}

$archive = [System.IO.Compression.ZipFile]::OpenRead($packagePath)
try {
  $entries = @($archive.Entries | ForEach-Object { $_.FullName })
  if ($entries -notcontains 'imsmanifest.xml') { throw 'imsmanifest.xml is not at the archive root.' }
  if ($entries | Where-Object { $_ -match '^\.build/' -or $_ -match '\\' }) { throw 'Archive contains an invalid entry path.' }
  $expectedCount = 1 + 5 + $pages.Count + ($assignments.Count * 2)
  if ($entries.Count -ne $expectedCount) { throw "Unexpected archive entry count: $($entries.Count); expected $expectedCount." }
}
finally {
  $archive.Dispose()
}

$hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $packagePath).Hash.ToLowerInvariant()
Write-Utf8 $checksumPath "$hash  $(Split-Path -Leaf $packagePath)`n"

Remove-Item -LiteralPath $buildRoot -Recurse -Force

$pointsTotal = ($assignments | ForEach-Object { [int]$_['Points'] } | Measure-Object -Sum).Sum
[pscustomobject]@{
  Package = $packagePath
  SHA256 = $hash
  Modules = $modules.Count
  Pages = $pages.Count
  Assignments = $assignments.Count
  Points = $pointsTotal
} | Format-List
