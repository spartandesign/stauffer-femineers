# Stauffer Femineers Google Forms setup

The script creates four Google Forms and one private Google Sheets response hub:

- New student application
- Returning-member confirmation
- Family information and commitment
- Teacher recommendation

## Run the script

1. Sign in to the school Google account that should own the forms and responses.
2. Open [Google Apps Script](https://script.google.com/) and choose **New project**.
3. Rename the project `Stauffer Femineers Recruitment 2026-27`.
4. Delete the sample code in `Code.gs`.
5. Copy the complete contents of `StaufferFemineersRecruitment.gs` into `Code.gs` and save.
6. In the function menu, select `createRecruitmentForms`, then click **Run**.
7. Approve the requested Google Forms and Google Sheets permissions. This is your own school-account script, so Google may show an authorization confirmation screen the first time.
8. Open Google Drive and find `Stauffer Femineers 2026–2027 — PRIVATE Recruitment Responses`.
9. Open its **START HERE** tab. It contains every responder link and editor link.

Running `createRecruitmentForms` again from the same Apps Script project returns the existing links instead of making duplicate forms.

## Check before sharing

- Open each form’s **Settings** and confirm which accounts may respond under district policy.
- Keep the student, returning-member, and teacher forms limited to signed-in users unless the school approves another setting.
- Make sure the family form is accessible to the families who need it.
- Submit one test response to each form and confirm that four response tabs appear in the private spreadsheet.
- Remove the test responses before recruitment opens.
- Do not share or publish the response spreadsheet on GitHub Pages.
- Add the three student/family responder links to the recruitment site only after testing them.

## Useful functions

- `showRecruitmentLinks()` prints the saved links again.
- `updateLiveFormsForYearBasedPathways()` updates the already-created forms so first-year students are assigned Creative Robotics and second-/third-year students are assigned Wearable Technology. Run this once after pasting the latest script into the existing Apps Script project.
- `updateLiveFormsForDenimSizing()` removes the denim-shirt-size question from the first-year and family forms. Returning second-/third-year members still provide their denim size. Run this once after pasting the latest script.
- `closeRecruitmentForms()` stops all four forms from accepting responses.
- `reopenRecruitmentForms()` reopens all four forms if an extension is approved.

The custom closed message is applied by `closeRecruitmentForms()` after each form is closed. Google rejects that message when it is applied to a new form that is still accepting responses.

Google Forms colors and header artwork are adjusted manually in each form’s **Customize theme** panel after the script finishes.
