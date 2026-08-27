# Canvas Import Guide

## Package

`Stauffer-Femineers-Limitless-2026-27.imscc`

Content revision: **2026-08-26 — Stamp from the Future added to Phase 1; Glow Up Your Badge added as a separate, unpublished October 13 district-event module with a 0-point reflection.**

This Canvas-flavored Common Cartridge course export contains:

- 10 Canvas modules
- 23 Canvas pages
- 9 Canvas assignments: eight 10-point project assignments plus one 0-point kickoff reflection
- 80 default points
- A syllabus and one assignment group named **Femineers Evidence**
- Links from Canvas to the detailed GitHub Pages guides

## Import into Canvas

1. Create or open a new, unpublished Canvas course shell.
2. Open **Settings** and select **Import Course Content**.
3. For **Content Type**, select **Canvas Course Export Package**.
4. Choose `Stauffer-Femineers-Limitless-2026-27.imscc`.
5. Select **All content**.
6. Do not apply date shifting because assignment dates are intentionally unset.
7. Start the import and wait for Canvas to report completion.
8. If Canvas reports an issue, review the issue list before editing or publishing.

Avoid importing the package into the same course more than once. Canvas may overwrite items imported from the earlier copy.

## Updating an existing Canvas course

If this package has already been imported and instructors have edited the live course, do not re-import the full rebuilt package. A repeat import can replace previously imported content and can disrupt course-specific edits.

Update the existing items in place instead:

1. **Safety, Supplies, and Evidence Rules** — add wooden-blank inspection, needle count-in/count-out, separate needle storage, and the ordinary-floss/non-powered rule.
2. **Phase 1: Imagine the Future** — add the Future Stamp as Wearables exploration evidence, not a third final wearable.
3. **Meet the Technology** — use the four stations: Future Stamp; combined LED/conductive-thread Circuit Lab; micro:bit; NeoPixel.
4. **Prepare Your Approved Design Proposal** — require pathway technology-exploration evidence and allow the stamp symbol to inform the shared shirt-and-hat theme.
5. **Checkpoint 1: Approved Project Proposal** — require the four Wearables evidence items and captions inside the same submission; do not create a separate stamp assignment or grade stamp craftsmanship as the approval gate.
6. **Mentor Lesson-Plan Playbook** — add the September 14 setup, material separation, rotation timing, and needle-accounting procedure.

Preserve the existing assignment’s due and availability dates, points, submission types, attempts, rubrics, student submissions, and grades. Back up/export the course before any selective re-import. Keep the Phase 1 module structure and item order unchanged.

### Add Glow Up Your Badge to an existing course

Do not re-import the full package solely to add the October 13 activity. Add these items manually between Phase 1 and Phase 2:

1. Create an unpublished module named **DUSD Femineers Kickoff — Glow Up Your Badge — October 13**.
2. Add an unpublished page named **Glow Up Your Badge** using the builder/source wording and link it to `glow-up-your-badge.html`.
3. Add an unpublished, 0-point assignment named **Kickoff Reflection — Glow Up Your Badge**. Allow the normal online submission choices, omit it from the final grade, and leave the due date unset until the post-event reflection time is confirmed.
4. Require one finished-badge photo and the three short reflection answers. Excuse non-attendees or provide a non-electrical alternative; do not direct students to recreate the circuit independently.
5. Update the existing **Program Roadmap and Important Dates**, **Mentor Lesson-Plan Playbook**, and **Canvas Launch Checklist** in place.
6. Keep the new module, page, and assignment unpublished until the final physical badge kit passes the 10–12 minute novice build, 20-minute rotation, safety, rapid-reset, and 90–95% normal-success targets.

Preserve every existing module, module item, assignment, and page identifier. Do not insert the kickoff items into Phase 2; the event remains a separate, theme-neutral module.

## Intentional defaults

- Course home view: Modules
- Project modules and items: published in the package
- DUSD Kickoff module, page, and reflection: unpublished pending prototype approval
- Mentor Planning module: unpublished
- Eight graded assignments: 10 points each
- Kickoff reflection: 0 points and omitted from the final grade
- Assignment group: Femineers Evidence
- Submission choices: text entry, URL, file upload, or media recording
- Attempts: unlimited
- Due dates and availability dates: unset
- Module progress: sequential
- Page editing: teachers only
- Time zone: America/Los_Angeles

Keep the receiving Canvas shell unpublished during the audit. If the shell is already published, use a sandbox course for the import.

## Required audit before launch

1. Confirm participation year and pathway: first year = Creative Robotics, second year = Wearable Technology, and third year = selected pathway.
2. Confirm the five full workdays: September 14, November 16, December 7, January 25, and February 22.
3. Confirm the October 13 district kickoff at Griffiths, including Stauffer’s 20-minute Glow Up Your Badge station, final kit, rotation headcount, staffing, and post-event reflection time.
4. Confirm the lunch checkpoints: October 21, January 13, and February 10, plus the invitation-only December 2 Project Rescue lunch.
5. Add due dates and availability dates to the eight graded assignments. October 19 is the recommended Design Ready deadline.
6. Schedule the 0-point kickoff reflection after the event and confirm the absence/alternative policy.
7. Confirm whether the eight graded assignments remain 10 points.
8. Confirm allowed file types and media-size limits for student iPad submissions.
9. Add district-required attendance, behavior, accommodations, communication, grading, and food-reward guidance.
10. Push the matching website pages to GitHub.
11. Test every module, page, assignment, and website button in Canvas Student View.
12. Keep the Kickoff and Mentor Planning modules unpublished until their release gates are complete.
13. Publish the course only after enrollment and launch communication are ready.

## Recommended Canvas navigation

Keep visible:

- Home
- Modules
- Assignments
- Grades
- Announcements

Consider hiding Pages, Files, and Syllabus from student navigation if the district allows it and the same information is already available through Modules.

## Rebuilding the package

The included `build_canvas_course.ps1` recreates the package with stable identifiers. Rebuild before the first import. After instructors begin editing the imported course, do not re-import a rebuilt package into that same course unless overwriting the original imported items is intentional.
