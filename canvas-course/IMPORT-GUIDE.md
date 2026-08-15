# Canvas Import Guide

## Package

`Stauffer-Femineers-Limitless-2026-27.imscc`

This Canvas-flavored Common Cartridge course export contains:

- 9 Canvas modules
- 22 Canvas pages
- 8 Canvas assignments
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

## Intentional defaults

- Course home view: Modules
- Student modules and items: published in the package
- Mentor Planning module: unpublished
- Assignments: 10 points each
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
2. Confirm the five full workdays: September 21, November 9, December 7, January 25, and February 22.
3. Confirm the lunch checkpoints: October 21, January 13, and February 10, plus the invitation-only December 2 Project Rescue lunch.
4. Add due dates and availability dates to all eight assignments. October 19 is the recommended Design Ready deadline.
5. Confirm whether every assignment remains 10 points.
6. Confirm allowed file types and media-size limits for student iPad submissions.
7. Add district-required attendance, behavior, accommodations, communication, grading, and food-reward guidance.
8. Push the matching website pages to GitHub.
9. Test every module, page, assignment, and website button in Canvas Student View.
10. Keep Mentor Planning unpublished unless students should see it.
11. Publish the course only after enrollment and launch communication are ready.

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
