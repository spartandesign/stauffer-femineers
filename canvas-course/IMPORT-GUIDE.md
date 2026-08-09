# Canvas Import Guide

## Package

`Stauffer-Femineers-Limitless-2026-27.imscc`

This is a Canvas-flavored Common Cartridge course export. It contains:

- 9 Canvas modules
- 21 Canvas pages
- 8 Canvas assignments
- 80 default points total
- A syllabus and one assignment group named **Femineers Evidence**
- Buttons connecting the Canvas pages to the detailed visual GitHub Pages guides

## Import into Canvas

1. Create or open a new, unpublished Canvas course shell.
2. Open **Settings**.
3. Select **Import Course Content**.
4. For **Content Type**, select **Canvas Course Export Package**.
5. Choose `Stauffer-Femineers-Limitless-2026-27.imscc`.
6. Select **All content**.
7. Do not apply date shifting; assignment due dates are intentionally unset.
8. Start the import and wait for Canvas to report completion.
9. If Canvas reports an issue, open the issue list before editing or publishing anything.

Avoid importing the same package into the same course more than once. Canvas may overwrite items that came from the earlier import.

## Intentional defaults

- Course home view: Modules
- Student modules and their items: published within the package
- Mentor Planning module: unpublished
- Assignments: 10 points each
- Assignment group: Femineers Evidence
- Submission choices: text entry, URL, file upload, or media recording
- Attempts: unlimited
- Due dates and availability dates: unset
- Module progress: sequential
- Page editing: teachers only
- Time zone: America/Los_Angeles

The receiving Canvas course shell should remain unpublished during the audit. If the shell is already published, unpublish it or import into a sandbox first.

## Required audit before launch

1. Confirm approval for the proposed October 5 and December 7 pull-out workdays.
2. Review the Phase 2 and Phase 4 module titles after those dates are approved.
3. Add due dates and availability dates to all eight assignments.
4. Confirm whether every assignment should remain 10 points.
5. Confirm allowed file types and media-size limits for student iPad submissions.
6. Add district-required attendance, behavior, accommodations, communication, and grading language.
7. Push the latest website pages to GitHub so all Phase 5 and Phase 6 buttons work publicly.
8. Test every module, page, assignment, and website button in Canvas Student View.
9. Publish the Mentor Planning module only if students should see it; otherwise keep it unpublished.
10. Publish the course only after enrollments and launch communication are ready.

## Recommended Canvas navigation

Keep visible:

- Home
- Modules
- Assignments
- Grades
- Announcements

Consider hiding from student navigation if your district allows it:

- Pages
- Files
- Syllabus, if the same information will live in the orientation module

## Rebuilding the package

The included `build_canvas_course.ps1` recreates the package with stable identifiers. Rebuilding is useful before the first import. After instructors begin editing the imported course directly, do not re-import a rebuilt package into that same course unless overwriting the original imported items is intentional.

