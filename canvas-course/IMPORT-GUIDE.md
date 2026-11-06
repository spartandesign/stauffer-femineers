# Canvas Import Guide

**Revision: September 23, 2026 — available-supplies plan for September 24.**

Use `Stauffer-Femineers-Limitless-2026-27.imscc`. This revision is prepared for the unused course shell. It replaces the previous day-one directions while retaining the later program, dates, assignment identifiers, points, and submission options.

## What the revised course contains

- 10 modules, 23 pages, and 9 assignments; 80 points across the year.
- Orientation and Phase 1 are published in the package: 8 pages and Checkpoint 1.
- The other 8 modules and all their pages and assignments are unpublished drafts. Release later phases as needed; keep Mentor Planning unpublished.
- Thursday uses felt LED practice, standalone micro:bit blocks, and Hummingbird Bit exploration. Paper/digital Future Stamp design and an observed NeoPixel preview replace unavailable hardware activities.
- Checkpoint 1 accepts actual practice/observation evidence, a proposal, and approved/provisional/revise-hold mentor status. Deferred tests have a named owner and a supervised test window.
- The revised student guide, mentor plan, and both four-page studio packets are linked from the appropriate course pages.

The website and imported Canvas pages are separate copies. Later website edits do not automatically change Canvas page or assignment text.

## Prepare the unused shell

1. Open the intended Femineers course and confirm its name. Keep it unpublished during setup.
2. If the shell is already empty, import directly; no reset is necessary.
3. If it contains only the old unused course, export a content backup first through **Settings → Export Course Content → Course → Create Export**, then download the result. This saves any instructor edits you may want later.
4. To replace that old course completely, use **Settings → Reset Course Content** if your district permits it. Read the confirmation before proceeding: a reset permanently removes content, changes the course ID/URL, and removes course-level LTI tools. Canvas retains course details and enrollments and leaves the resulting course unpublished. Update saved course links afterward. If Reset is unavailable or the shell has school-managed integrations that must be retained, ask the Canvas administrator for an empty shell or an approved cleanup route.
5. Do not simply import a second full copy over the old course to simulate a clean start. Previously imported content may be overwritten while manually added content can remain.

This route is for the confirmed unused shell. If that changes and student work has been submitted, stop the reset workflow and update content in place. A course export does not back up student submissions or grades.

Official guidance: [Reset course content](https://community.instructure.com/en/kb/articles/661144-how-do-i-reset-course-content), [export a course](https://community.instructure.com/en/kb/articles/660734-how-do-i-export-a-canvas-course).

## Import the revised package once

1. In the empty, unpublished course, open **Settings → Import Course Content**.
2. Choose **Canvas Course Export Package** as the content type.
3. Select `Stauffer-Femineers-Limitless-2026-27.imscc` from this folder. Keep the `.imscc` extension; do not unzip it for import.
4. Select **All content**.
5. Leave date adjustment off. Due and availability dates are intentionally unset in the package.
6. Click **Add to Import Queue** (or **Import** in the older interface).
7. Wait for completion and inspect any issues before publishing.
8. Review the receiving course settings after import, including its name, time zone, visibility, enrollment, and any district-specific settings.

Official guidance: [Import a Canvas course export package](https://community.instructure.com/en/kb/articles/660728-how-do-i-import-a-canvas-course-export-package).

## Check before students use it

1. **Modules:** verify there is one orientation module and one September 24 module, followed by the unpublished later modules. There should be no duplicate old course content.
2. **Day-one flow:** Phase 1 still has four items in order: overview; Meet the Technology; Prepare Your Design Proposal; Checkpoint 1: Project Proposal + Mentor Review.
3. **Evidence:** verify paper/digital symbol, felt practice, physical-board/simulator labels, observed NeoPixel preview, actual Robotics input/output types, and deferred tests. Do not require a wooden-stamp or physical-NeoPixel photo on Thursday.
4. **Mentor resources:** open the backup mentor plan and the revised Wearables and Robotics PDFs. Print 20 Wearables sets and 11 Robotics sets; each set is four pages/two duplex sheets. These are studio tools, not extra homework or separately graded worksheets.
5. **Completion window:** set Checkpoint 1 to the approved school-time deadline and arrange supervised catch-up. The package does not invent a due time or late penalty.
6. **Robotics submissions:** assignments remain individual Canvas assignments. Each partner can submit/link the shared technical packet with their own reflection unless you deliberately configure a Canvas group assignment first.
7. **Student View:** check the visible orientation pages, all four Phase 1 items, linked guides, and submission options. Confirm that later and mentor-only pages/assignments do not appear through Modules, Pages, or Assignments. Unpublishing just a module is insufficient; the package also unpublishes its resources.
8. **Safety and readiness:** physically test the available kits and firmware, confirm actual sensor types, match batteries to holders, rehearse reset routines, and count needles. Remote package validation does not certify the equipment.
9. **Schedule:** confirm the September 24 Thursday bells: 8:00–2:41 in Room 14, snack 9:25–9:38, lunch 12:42–1:12. Keep the later Monday workdays and Wednesday lunch checkpoints as shown in the course map.
10. **Local policies:** add the school’s contact information, attendance, accommodations, grading, and communication requirements; check iPad file/media submission limits.
11. Publish the course after the import and Student View checks pass.

## Release later phases

- Later lesson and assignment content is retained. Publish each later module **and its pages/assignment** when that phase is ready; then test it in Student View.
- Phase 2 retains the recommended October 19 Design Ready deadline and October 21 lunch review. Set actual Canvas dates to approved supervised work windows.
- Before dependent construction, revisit any provisional September proposals and complete their deferred technology/safety checks.
- Keep October 13 Glow Up Your Badge unpublished until the exact physical kit passes its existing mentor prototype, novice-build timing, safety, repeatability, and reset gates. Its reflection stays 0 points and omitted from the final grade.
- Keep both Mentor Planning pages and their module unpublished.
- Keep Home, Modules, Assignments, Grades, and Announcements visible. Consider hiding Pages and Files from navigation if the district allows it, while retaining access to required items through Modules. The package does not set course-navigation permissions.

## Rebuild and verification

Run `build_canvas_course.ps1` from this folder. The builder writes the `.imscc` package and its SHA-256 checksum, checks XML and resource references, and uses stable identifiers. It aligns page, assignment, and item publication states with module release states.

Do not repeatedly re-import into a course after instructors or students begin using it. Make later live-course changes in place. A locally validated package still needs the Canvas import and Student View checks above.
