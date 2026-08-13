/**
 * Stauffer Femineers 2026–2027 recruitment form builder.
 *
 * Run createRecruitmentForms() once from a standalone Google Apps Script
 * project owned by the school account that should own the forms and responses.
 * The script creates four Google Forms and one private response spreadsheet.
 */

const RECRUITMENT = Object.freeze({
  year: '2026–2027',
  theme: 'Limitless: Designed by Her',
  window: 'August 18–September 4, 2026',
  dueDate: 'September 4, 2026',
  capacity: 50,
  siteUrl: 'https://spartandesign.github.io/stauffer-femineers/recruitment.html',
  roadmapUrl: 'https://spartandesign.github.io/stauffer-femineers/program-roadmap.html',
  propertyKey: 'STAUFFER_FEMINEERS_RECRUITMENT_2026_27',
});

const CLOSED_FORM_MESSAGE =
  'Recruitment is currently closed. Please contact a Stauffer Femineers mentor through the school’s approved communication method.';

const PATHWAY_PLACEMENT =
  'PATHWAY OPTIONS: First-year Femineers complete Creative Robotics in teams of two. Second-year Femineers complete Wearable Technology individually. Third-year Femineers choose Creative Robotics or Wearable Technology.';

const DENIM_SIZE_RULE =
  'DENIM SIZING: A denim-shirt size is required from second-year members and third-year members choosing Wearable Technology. It is not needed for first-year members or third-year members choosing Creative Robotics.';

const PULL_OUT_COMMITMENT =
  'SCHOOL-DAY COMMITMENT: Students will be pulled from regular classes for five full workdays in Room 14 from 8:00 a.m.–2:41 p.m. Students also attend three Wednesday lunch checkpoints in Room 14 from 12:29–12:59 p.m. Students must check with teachers, collect assignments and notes, and complete all missed work by each teacher’s deadline.';

const WORKDAYS = Object.freeze([
  'Monday, September 21, 2026 — Imagine the Future',
  'Monday, November 9, 2026 — Design What’s Next',
  'Monday, December 7, 2026 — Build & Test',
  'Monday, January 25, 2027 — Build the Future',
  'Monday, February 22, 2027 — Step Into the Future',
]);

const LUNCH_CHECKPOINTS = Object.freeze([
  'Wednesday, October 21, 2026 — Design Ready checkpoint',
  'Wednesday, January 13, 2027 — Restart Ready checkpoint',
  'Wednesday, February 10, 2027 — Gala Path checkpoint',
]);

const EVENTS = Object.freeze([
  'October 13, 2026 — District Femineers Kickoff at Griffiths',
  'March 1, 2027 — Stauffer Gala in the Stauffer Library',
  'March 18, 2027 — Evening District Femineers Gala at Downey High with guest speakers and Culinary Arts hors d’oeuvres',
]);

const SHIRT_SIZES = Object.freeze([
  'Youth Small (YS)',
  'Youth Medium (YM)',
  'Youth Large (YL)',
  'Adult Small (AS)',
  'Adult Medium (AM)',
  'Adult Large (AL)',
  'Adult XL (AXL)',
  'Adult 2XL (A2XL)',
  'Other / not sure — mentor follow-up needed',
]);

/**
 * Creates the four forms and their shared private response spreadsheet.
 * If this function has already completed, it returns the existing links instead
 * of creating duplicate forms.
 */
function createRecruitmentForms() {
  const properties = PropertiesService.getScriptProperties();
  const saved = properties.getProperty(RECRUITMENT.propertyKey);

  if (saved) {
    const existing = JSON.parse(saved);
    logRecruitmentLinks_(existing, 'Recruitment files already exist.');
    return existing;
  }

  const responseHub = SpreadsheetApp.create(
    `Stauffer Femineers ${RECRUITMENT.year} — PRIVATE Recruitment Responses`
  );
  const startSheet = responseHub.getSheets()[0];
  startSheet.setName('START HERE');
  prepareStartSheet_(startSheet);

  const familyForm = buildFamilyForm_(responseHub.getId());
  const familyUrl = familyForm.getPublishedUrl();
  const newStudentForm = buildNewStudentForm_(responseHub.getId(), familyUrl);
  const returningForm = buildReturningMemberForm_(responseHub.getId(), familyUrl);
  const teacherForm = buildTeacherRecommendationForm_(responseHub.getId());

  const links = {
    createdAt: new Date().toISOString(),
    responseSpreadsheet: {
      id: responseHub.getId(),
      url: responseHub.getUrl(),
    },
    newStudent: formLinks_(newStudentForm),
    returningMember: formLinks_(returningForm),
    familyCommitment: formLinks_(familyForm),
    teacherRecommendation: formLinks_(teacherForm),
  };

  writeStartSheet_(startSheet, links);
  properties.setProperty(RECRUITMENT.propertyKey, JSON.stringify(links));
  SpreadsheetApp.flush();
  logRecruitmentLinks_(links, 'Recruitment files created successfully.');
  return links;
}

/** Logs the existing form and spreadsheet links without creating anything. */
function showRecruitmentLinks() {
  const links = getSavedRecruitmentLinks_();
  logRecruitmentLinks_(links, 'Saved recruitment links:');
  return links;
}

/** Closes all four forms. Run this after recruitment ends. */
function closeRecruitmentForms() {
  setAllFormsAcceptingResponses_(false);
}

/** Reopens all four forms if a deadline extension is approved. */
function reopenRecruitmentForms() {
  setAllFormsAcceptingResponses_(true);
}

/** Backward-compatible shortcut for the current live-form update. */
function updateLiveFormsForYearBasedPathways() {
  return updateLiveFormsForFiveWorkdaysAndLunchCheckpoints();
}

/** Backward-compatible shortcut retained for copies using the earlier function name. */
function updateLiveFormsForThirdYearChoiceAndPulloutDates() {
  return updateLiveFormsForFiveWorkdaysAndLunchCheckpoints();
}

/**
 * Updates the four existing live forms without changing their public links.
 * Run this once after replacing Code.gs with this version.
 */
function updateLiveFormsForFiveWorkdaysAndLunchCheckpoints() {
  const links = getSavedRecruitmentLinks_();
  const newStudentForm = FormApp.openById(links.newStudent.id);
  const returningForm = FormApp.openById(links.returningMember.id);
  const familyForm = FormApp.openById(links.familyCommitment.id);
  const teacherForm = FormApp.openById(links.teacherRecommendation.id);
  const scheduleText = pullOutScheduleText_();
  const lunchText = lunchCheckpointScheduleText_();

  replaceRecruitmentRulesInDescription_(newStudentForm, [PATHWAY_PLACEMENT, PULL_OUT_COMMITMENT, scheduleText, lunchText]);
  replaceRecruitmentRulesInDescription_(returningForm, [PATHWAY_PLACEMENT, DENIM_SIZE_RULE, PULL_OUT_COMMITMENT, scheduleText, lunchText]);
  replaceRecruitmentRulesInDescription_(familyForm, [PATHWAY_PLACEMENT, DENIM_SIZE_RULE, PULL_OUT_COMMITMENT, scheduleText, lunchText]);
  replaceRecruitmentRulesInDescription_(teacherForm, [PATHWAY_PLACEMENT]);

  newStudentForm.setConfirmationMessage(
    'Thank you for applying to Stauffer Femineers. Your first-year pathway is Creative Robotics. A family member must also submit the family commitment form before your application is complete: ' +
      links.familyCommitment.responderUrl
  );
  updateCommitmentQuestion_(newStudentForm, 'Confirm each program commitment.', [
    'I reviewed all five pull-out workdays, three lunch checkpoints, and events with my family.',
    'I understand that I must check with teachers, collect assignments and notes, and complete missed classwork by each teacher’s deadline.',
    'I will share robotics responsibilities with my partner and rotate roles.',
    'I am willing to design, build, code, test, document, clean up, and present.',
    'I understand that space is limited and an application does not guarantee placement.',
  ]);

  upsertMultipleChoiceQuestion_(
    returningForm,
    ['Current pathway preference', 'Your assigned returning-member pathway', 'Your 2026–2027 pathway'],
    'Your 2026–2027 pathway',
    [
      '2nd year — Wearable Technology',
      '3rd year — Creative Robotics',
      '3rd year — Wearable Technology',
    ],
    'Second-year members complete Wearable Technology. Third-year members choose either pathway.'
  );
  updateParagraphQuestionIfPresent_(
    returningForm,
    [
      'What is one new skill or leadership contribution you want to develop?',
      'What wearable-technology skill or leadership contribution do you want to develop?',
      'What pathway-specific skill or leadership contribution do you want to develop?',
    ],
    'What pathway-specific skill or leadership contribution do you want to develop?',
    ''
  );
  updateCommitmentQuestion_(returningForm, 'Confirm each returning-member commitment.', [
    'I reviewed all five pull-out workdays, three lunch checkpoints, and events with my family.',
    'I will check with teachers, collect assignments and notes, and complete missed classwork by each teacher’s deadline.',
    'I will complete the project requirements for my confirmed pathway.',
    'I will participate in designing, building, programming, testing, documenting, cleanup, and presentation.',
    'I understand that confirmation is required for roster planning.',
  ]);
  upsertListQuestion_(
    returningForm,
    ['Denim-shirt size', 'Denim-shirt size — Wearable Technology only'],
    'Denim-shirt size — Wearable Technology only',
    SHIRT_SIZES.concat(['Not needed — 3rd-year Creative Robotics']),
    'Second-year members and third-year members choosing Wearable Technology provide a denim size. Third-year Robotics members select “Not needed.”'
  );
  returningForm.setConfirmationMessage(
    'Your returning-member confirmation and pathway response were received. A family member must also submit the family commitment form before your confirmation is complete: ' +
      links.familyCommitment.responderUrl
  );

  upsertMultipleChoiceQuestion_(
    familyForm,
    ['Student application type', 'Student participation year and assigned pathway', 'Student participation year and pathway'],
    'Student participation year and pathway',
    [
      '1st year — Creative Robotics',
      '2nd year — Wearable Technology',
      '3rd year — Creative Robotics',
      '3rd year — Wearable Technology',
    ],
    'First- and second-year pathways are assigned. Third-year members choose either pathway.'
  );
  updateCommitmentQuestion_(familyForm, 'Please confirm every family commitment.', [
    'We understand the pathway rules and have confirmed the student’s pathway above.',
    'We reviewed all five pull-out workdays, three lunch checkpoints, and the additional events.',
    'We understand that the student must check with teachers, collect assignments and notes, and complete missed work by each teacher’s deadline.',
    'We will communicate attendance conflicts as early as possible.',
    'We understand that projects require safe tool use, cleanup, documentation, and public presentation.',
    'We understand that space is limited to 50 students and submitting forms does not guarantee placement.',
  ]);
  updatePageBreakHelpText_(
    familyForm,
    'Schedule and attendance',
    'All five workdays are in Room 14 from 8:00 a.m.–2:41 p.m. Snack is 9:38–9:51 a.m.; lunch is 12:29–12:59 p.m.\n\n' +
      WORKDAYS.join('\n') +
      '\n\nWednesday lunch checkpoints — Room 14, 12:29–12:59 p.m.:\n' +
      LUNCH_CHECKPOINTS.join('\n') +
      '\n\nAdditional events:\n' +
      EVENTS.join('\n')
  );

  deleteQuestionIfPresent_(newStudentForm, 'Denim-shirt size');
  deleteQuestionIfPresent_(familyForm, 'Denim-shirt size');
  console.log('All four live recruitment forms now use five pull-out workdays, three lunch checkpoints, and the updated Gala information.');
  logRecruitmentLinks_(links, 'Updated live form links:');
  return links;
}

/** Removes denim sizing from the first-year and shared family forms. */
function updateLiveFormsForDenimSizing() {
  const links = getSavedRecruitmentLinks_();
  const newStudentForm = FormApp.openById(links.newStudent.id);
  const returningForm = FormApp.openById(links.returningMember.id);
  const familyForm = FormApp.openById(links.familyCommitment.id);

  deleteQuestionIfPresent_(newStudentForm, 'Denim-shirt size');
  deleteQuestionIfPresent_(familyForm, 'Denim-shirt size');
  addTextToDescription_(returningForm, DENIM_SIZE_RULE);
  addTextToDescription_(familyForm, DENIM_SIZE_RULE);

  console.log('Denim sizing is limited to returning members whose pathway is Wearable Technology.');
  logRecruitmentLinks_(links, 'Updated live form links:');
}

function buildNewStudentForm_(spreadsheetId, familyUrl) {
  const form = FormApp.create(
    `Stauffer Femineers ${RECRUITMENT.year} — First-Year Student Application`,
    false
  );

  configureForm_(
    form,
    [
      `${RECRUITMENT.theme}`,
      `Applications are open ${RECRUITMENT.window}. Membership is capped at ${RECRUITMENT.capacity} students.`,
      PATHWAY_PLACEMENT,
      PULL_OUT_COMMITMENT,
      pullOutScheduleText_(),
      lunchCheckpointScheduleText_(),
      'No previous engineering, coding, or robotics experience is required. We are looking for curiosity, persistence, collaboration, student voice, and commitment—not only top grades or prior experience.',
      `Review the program first: ${RECRUITMENT.siteUrl}`,
      `A family member must also complete the family commitment form: ${familyUrl}`,
    ].join('\n\n'),
    'Thank you for applying to Stauffer Femineers. Your assigned first-year pathway is Creative Robotics. A family member must also submit the family commitment form before your application is complete: ' + familyUrl,
    true,
    spreadsheetId
  );

  addIdentitySection_(form, false);

  form.addPageBreakItem()
    .setTitle('Imagine a possibility')
    .setHelpText('There are no “correct” project ideas. We want to hear what genuinely interests you.');

  form.addMultipleChoiceItem()
    .setTitle('Your assigned first-year pathway')
    .setChoiceValues(['Creative Robotics — all first-year Femineers'])
    .setHelpText('Select the statement to confirm that you understand your pathway assignment.')
    .setRequired(true);

  addParagraph_(
    form,
    'What interests you about building an interactive invention with sensors, lights, movement, craft materials, and programming?',
    'Use specific details. Prior robotics or coding experience is not required.',
    true
  );
  addParagraph_(
    form,
    'Name a future problem, opportunity, career, community, or creative idea you would like to explore.',
    '',
    true
  );
  addParagraph_(
    form,
    'What might your robotics team design, build, or investigate?',
    '',
    true
  );

  form.addPageBreakItem()
    .setTitle('How you learn and contribute')
    .setHelpText('Specific examples help mentors understand how you approach challenges and teamwork.');

  addParagraph_(
    form,
    'Describe a time something was difficult but you kept working, asked for help, or tried a different approach.',
    '',
    true
  );
  addParagraph_(
    form,
    'What makes you a helpful robotics partner or team member? Give one example.',
    '',
    true
  );

  form.addPageBreakItem()
    .setTitle('Commitment and sizes')
    .setHelpText('Review these items with your family before submitting.');

  addCommitmentCheckbox_(form, 'Confirm each program commitment.', [
    'I reviewed the five workdays, three lunch checkpoints, and events with my family.',
    'I understand that I must arrange and complete classwork missed during school-day sessions.',
    'I will share robotics responsibilities with my partner and rotate roles.',
    'I am willing to design, build, code, test, document, clean up, and present.',
    'I understand that space is limited and an application does not guarantee placement.',
  ]);

  addSizeQuestions_(form, false);

  form.addMultipleChoiceItem()
    .setTitle('Family commitment form status')
    .setChoiceValues([
      'My family already submitted it.',
      'My family will submit it by September 4.',
      'We need a paper copy or mentor assistance.',
    ])
    .setHelpText(familyUrl)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Would a mentor follow-up help you participate successfully?')
    .setChoiceValues(['No follow-up requested', 'Yes, please contact me through a school-approved method'])
    .setRequired(true);

  addParagraph_(
    form,
    'Optional follow-up note',
    'Do not include private medical information. A family member may share necessary information through the school’s approved process.',
    false
  );

  publishForm_(form);
  return form;
}

function buildReturningMemberForm_(spreadsheetId, familyUrl) {
  const form = FormApp.create(
    `Stauffer Femineers ${RECRUITMENT.year} — Second-/Third-Year Confirmation`,
    false
  );

  configureForm_(
    form,
    [
      `${RECRUITMENT.theme}`,
      `Returning members must confirm by ${RECRUITMENT.dueDate}. Prior membership does not automatically reserve a place.`,
      PATHWAY_PLACEMENT,
      DENIM_SIZE_RULE,
      PULL_OUT_COMMITMENT,
      pullOutScheduleText_(),
      lunchCheckpointScheduleText_(),
      `Review the program: ${RECRUITMENT.siteUrl}`,
      `A family member must also complete the family commitment form: ${familyUrl}`,
    ].join('\n\n'),
    'Your returning-member confirmation and pathway response were received. Second-year members complete Wearable Technology; third-year members may choose either pathway. A family member must also submit the family commitment form before your confirmation is complete: ' + familyUrl,
    true,
    spreadsheetId
  );

  addIdentitySection_(form, true);

  const returningStatus = form.addMultipleChoiceItem()
    .setTitle('Are you returning to Stauffer Femineers for 2026–2027?')
    .setRequired(true);

  const returningSection = form.addPageBreakItem()
    .setTitle('Confirm your returning place')
    .setHelpText('Complete this section if you want to return for 2026–2027.');

  form.addMultipleChoiceItem()
    .setTitle('Your 2026–2027 pathway')
    .setChoiceValues([
      '2nd year — Wearable Technology',
      '3rd year — Creative Robotics',
      '3rd year — Wearable Technology',
    ])
    .setHelpText('Second-year members complete Wearable Technology. Third-year members choose either pathway.')
    .setRequired(true);

  form.addSectionHeaderItem()
    .setTitle('Build on your experience');

  addParagraph_(
    form,
    'What is one skill, habit, or project lesson you are bringing back?',
    '',
    true
  );
  addParagraph_(
    form,
    'What pathway-specific skill or leadership contribution do you want to develop?',
    '',
    true
  );

  form.addPageBreakItem()
    .setTitle('Commitment and updates');

  addCommitmentCheckbox_(form, 'Confirm each returning-member commitment.', [
    'I reviewed all five workdays, three lunch checkpoints, and events with my family.',
    'I will arrange and complete classwork missed during school-day sessions.',
    'I will complete the project requirements for my confirmed pathway.',
    'I will participate in designing, building, programming, testing, documenting, cleanup, and presentation.',
    'I understand that confirmation is required for roster planning.',
  ]);

  addSizeQuestions_(form, true);

  form.addMultipleChoiceItem()
    .setTitle('Family commitment form status')
    .setChoiceValues([
      'My family already submitted it.',
      'My family will submit it by September 4.',
      'We need a paper copy or mentor assistance.',
    ])
    .setHelpText(familyUrl)
    .setRequired(true);

  addParagraph_(
    form,
    'Optional scheduling, participation, or support follow-up',
    'Do not include private medical information. Use the school’s approved process for confidential information.',
    false
  );

  const notReturningSection = form.addPageBreakItem()
    .setTitle('Thank you for letting us know')
    .setHelpText('Complete this brief section if you are not returning this year.');

  // When a returning student finishes the section above, submit instead of
  // continuing into the not-returning section.
  notReturningSection.setGoToPage(FormApp.PageNavigationType.SUBMIT);

  form.addMultipleChoiceItem()
    .setTitle('Please confirm your roster update.')
    .setChoiceValues(['I am not returning to Stauffer Femineers for 2026–2027.'])
    .setRequired(true);

  addParagraph_(
    form,
    'Optional: Is there anything you would like the mentors to know?',
    'You may leave this blank.',
    false
  );

  returningStatus.setChoices([
    returningStatus.createChoice('Yes, I want to return.', returningSection),
    returningStatus.createChoice('No, I am not returning this year.', notReturningSection),
  ]);

  publishForm_(form);
  return form;
}

function buildFamilyForm_(spreadsheetId) {
  const form = FormApp.create(
    `Stauffer Femineers ${RECRUITMENT.year} — Family Information and Commitment`,
    false
  );

  configureForm_(
    form,
    [
      `${RECRUITMENT.theme}`,
      'Please complete one family form for each student applying or confirming a returning place.',
      PATHWAY_PLACEMENT,
      DENIM_SIZE_RULE,
      PULL_OUT_COMMITMENT,
      pullOutScheduleText_(),
      lunchCheckpointScheduleText_(),
      `Recruitment window: ${RECRUITMENT.window}. Program capacity: ${RECRUITMENT.capacity} students.`,
      'This is recruitment planning material, not emergency or medical documentation. Do not enter confidential medical details. Continue to use the school’s required forms and reporting processes.',
      `Program information: ${RECRUITMENT.siteUrl}`,
    ].join('\n\n'),
    'Thank you. Your family information and commitment form was received. This form supports recruitment planning and does not by itself confirm placement.',
    false,
    spreadsheetId
  );

  form.addSectionHeaderItem()
    .setTitle('Student and family information');

  form.addTextItem()
    .setTitle('Student full name')
    .setRequired(true);

  form.addListItem()
    .setTitle('Student grade for 2026–2027')
    .setChoiceValues(['6', '7', '8'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Student participation year and pathway')
    .setChoiceValues([
      '1st year — Creative Robotics',
      '2nd year — Wearable Technology',
      '3rd year — Creative Robotics',
      '3rd year — Wearable Technology',
    ])
    .setHelpText('First- and second-year pathways are assigned. Third-year members choose either pathway.')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Family member full name')
    .setRequired(true);

  addEmailItem_(form, 'Family email address', true);

  form.addMultipleChoiceItem()
    .setTitle('Preferred school-approved contact method')
    .setChoiceValues(['Email', 'Phone call', 'Text message', 'Other school-approved method'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('Phone number, if phone or text is preferred')
    .setRequired(false);

  form.addPageBreakItem()
    .setTitle('Schedule and attendance')
    .setHelpText(
      'All five workdays are in Room 14 from 8:00 a.m.–2:41 p.m. Snack is 9:38–9:51 a.m.; lunch is 12:29–12:59 p.m.\n\n' +
      WORKDAYS.join('\n') +
      '\n\nWednesday lunch checkpoints — Room 14, 12:29–12:59 p.m.:\n' +
      LUNCH_CHECKPOINTS.join('\n') +
      '\n\nAdditional events:\n' +
      EVENTS.join('\n')
    );

  addCommitmentCheckbox_(form, 'Please confirm every family commitment.', [
    'We understand the pathway rules and have confirmed the student’s pathway above.',
    'We reviewed all five workdays, three lunch checkpoints, and the additional events.',
    'We understand that the student must arrange and complete missed classwork.',
    'We will communicate attendance conflicts as early as possible.',
    'We understand that projects require safe tool use, cleanup, documentation, and public presentation.',
    'We understand that space is limited to 50 students and submitting forms does not guarantee placement.',
  ]);

  form.addPageBreakItem()
    .setTitle('Sizes and participation follow-up');

  addSizeQuestions_(form, false);

  form.addMultipleChoiceItem()
    .setTitle('Dietary, accessibility, or participation follow-up')
    .setChoiceValues([
      'No private follow-up requested',
      'Please contact our family through the preferred school-approved method',
    ])
    .setHelpText('Do not enter confidential medical details on this form.')
    .setRequired(true);

  addParagraph_(
    form,
    'Optional planning note',
    'Keep this general. Use the school’s required confidential process for medical or protected information.',
    false
  );

  addCommitmentCheckbox_(form, 'Family acknowledgement', [
    'I am the student’s parent/guardian or authorized family member, and the information above is accurate to the best of my knowledge.',
  ]);

  publishForm_(form);
  return form;
}

function buildTeacherRecommendationForm_(spreadsheetId) {
  const form = FormApp.create(
    `Stauffer Femineers ${RECRUITMENT.year} — First-Year Candidate Recommendation`,
    false
  );

  configureForm_(
    form,
    [
      `Recommendations are due ${RECRUITMENT.dueDate}.`,
      PATHWAY_PLACEMENT,
      'Please recommend first-year candidates for Creative Robotics who show curiosity, persistence, creativity, collaboration, responsibility, or who would especially benefit from a hands-on engineering community—including students who may not nominate themselves.',
      'This is not a grade check. Do not include grades, disability information, medical information, or other protected details.',
      `Program information: ${RECRUITMENT.siteUrl}`,
    ].join('\n\n'),
    'Thank you. Your recommendation was received and will be used as one source of context. A recommendation does not guarantee or prevent placement.',
    true,
    spreadsheetId
  );

  form.addTextItem()
    .setTitle('Recommending teacher name')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Student full name')
    .setRequired(true);

  form.addListItem()
    .setTitle('Student grade for 2026–2027')
    .setChoiceValues(['6', '7', '8'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('Course or connection to the student')
    .setRequired(true);

  const qualities = [
    'Curiosity',
    'Creativity',
    'Persistence',
    'Collaboration',
    'Responsibility',
    'Problem solving',
    'Leadership potential',
    'Would benefit from encouragement',
    'May not self-nominate',
    'Interest in design, making, art, science, math, or technology',
  ];
  const qualityValidation = FormApp.createCheckboxValidation()
    .setHelpText('Select at least one observed quality.')
    .requireSelectAtLeast(1)
    .build();
  form.addCheckboxItem()
    .setTitle('Which qualities have you observed?')
    .setChoiceValues(qualities)
    .setValidation(qualityValidation)
    .setRequired(true);

  addParagraph_(
    form,
    'Give one specific example of an observed quality.',
    'Use a professional, school-appropriate observation.',
    true
  );
  addParagraph_(
    form,
    'How might this student contribute to or benefit from Femineers?',
    '',
    true
  );

  form.addMultipleChoiceItem()
    .setTitle('Observed follow-through')
    .setChoiceValues(['Emerging', 'Developing', 'Consistent', 'Strong', 'Not enough information'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Observed collaboration')
    .setChoiceValues(['Emerging', 'Developing', 'Consistent', 'Strong', 'Not enough information'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('Would you encourage this student to apply?')
    .setChoiceValues(['Yes', 'Yes, with a mentor follow-up', 'Unsure'])
    .setRequired(true);

  addParagraph_(
    form,
    'Optional school-based support or encouragement strategy mentors should discuss with you',
    'Do not include confidential medical or protected information.',
    false
  );

  addCommitmentCheckbox_(form, 'Professional acknowledgement', [
    'I confirm that this recommendation reflects school-appropriate observations and does not include grades or protected information.',
  ]);

  publishForm_(form);
  return form;
}

function configureForm_(form, description, confirmationMessage, requireSignIn, spreadsheetId) {
  // Keep each setting on its own line so a Google execution error identifies
  // the exact setting that needs attention.
  form.setDescription(description);
  form.setIsQuiz(false);
  form.setCollectEmail(requireSignIn);
  form.setLimitOneResponsePerUser(requireSignIn);
  form.setAllowResponseEdits(true);
  form.setProgressBar(true);
  form.setShowLinkToRespondAgain(false);
  form.setPublishingSummary(false);
  form.setShuffleQuestions(false);
  form.setConfirmationMessage(confirmationMessage);
  form.setDestination(FormApp.DestinationType.SPREADSHEET, spreadsheetId);
}

function publishForm_(form) {
  form.setPublished(true);
  form.setAcceptingResponses(true);
}

function addIdentitySection_(form, returning) {
  form.addSectionHeaderItem()
    .setTitle('Student information')
    .setHelpText('Use your school account. The form records the signed-in email address.');

  form.addTextItem()
    .setTitle('Student full name')
    .setRequired(true);

  form.addListItem()
    .setTitle('Grade for 2026–2027')
    .setChoiceValues(['6', '7', '8'])
    .setRequired(true);

  form.addTextItem()
    .setTitle('Student ID, if your school asks for it')
    .setRequired(false);

  if (returning) {
    form.addTextItem()
      .setTitle('Previous Femineers year or years')
      .setRequired(true);
    form.addMultipleChoiceItem()
      .setTitle('This will be my Femineers participation year')
      .setChoiceValues(['2nd year', '3rd year'])
      .setRequired(true);
  }
}

function addEmailItem_(form, title, required) {
  const validation = FormApp.createTextValidation()
    .setHelpText('Enter a complete email address, such as name@school.org.')
    .requireTextIsEmail()
    .build();
  form.addTextItem()
    .setTitle(title)
    .setValidation(validation)
    .setRequired(required);
}

function addParagraph_(form, title, helpText, required) {
  const item = form.addParagraphTextItem()
    .setTitle(title)
    .setRequired(required);
  if (helpText) item.setHelpText(helpText);
  return item;
}

function addSizeQuestions_(form, includeDenim) {
  form.addListItem()
    .setTitle('Femineers T-shirt size')
    .setChoiceValues(SHIRT_SIZES)
    .setRequired(true);
  if (includeDenim) {
    form.addListItem()
      .setTitle('Denim-shirt size — Wearable Technology only')
      .setChoiceValues(SHIRT_SIZES.concat(['Not needed — 3rd-year Creative Robotics']))
      .setHelpText('Second-year members and third-year members choosing Wearable Technology provide a denim size. Third-year Robotics members select “Not needed.”')
      .setRequired(true);
  }
}

function addCommitmentCheckbox_(form, title, statements, requireAll) {
  const mustSelectAll = requireAll !== false;
  const item = form.addCheckboxItem()
    .setTitle(title)
    .setChoiceValues(statements)
    .setRequired(true);

  if (mustSelectAll) {
    const validation = FormApp.createCheckboxValidation()
      .setHelpText('Select every statement to continue.')
      .requireSelectExactly(statements.length)
      .build();
    item.setValidation(validation);
  }
  return item;
}

function addPlacementToDescription_(form) {
  addTextToDescription_(form, PATHWAY_PLACEMENT);
}

function pullOutScheduleText_() {
  return [
    'FIVE FULL-DAY PULL-OUT WORKDAYS — Room 14, 8:00 a.m.–2:41 p.m.',
    WORKDAYS.join('\n'),
  ].join('\n');
}

function lunchCheckpointScheduleText_() {
  return [
    'THREE WEDNESDAY LUNCH CHECKPOINTS — Room 14, 12:29–12:59 p.m.',
    LUNCH_CHECKPOINTS.join('\n'),
    'Students submit the required Canvas deliverables, demonstrate progress, receive a readiness status, and identify the next action.',
  ].join('\n');
}

function replaceRecruitmentRulesInDescription_(form, currentRules) {
  const obsoleteRules = [
    'PATHWAY PLACEMENT: First-year Femineers complete Creative Robotics in teams of two. Second- and third-year Femineers complete Wearable Technology individually. Students do not choose between the pathways.',
    'DENIM SIZING: A denim-shirt size is required only from second- and third-year Wearable Technology members.',
    'SCHOOL-DAY COMMITMENT: Students will be pulled from regular classes for all six workdays in Room 14 from 8:00 a.m.–2:41 p.m. Students must check with teachers, collect assignments and notes, and complete all missed work by each teacher’s deadline.',
    [
      'SIX FULL-DAY PULL-OUT WORKDAYS — Room 14, 8:00 a.m.–2:41 p.m.',
      'Monday, September 21, 2026 — Imagine the Future',
      'Monday, October 5, 2026 — Prototype the Future',
      'Monday, November 2, 2026 — Design What’s Next',
      'Monday, December 7, 2026 — Build & Test',
      'Monday, January 11, 2027 — Build the Future',
      'Monday, February 22, 2027 — Step Into the Future',
    ].join('\n'),
  ];
  let description = form.getDescription() || '';
  obsoleteRules.concat(currentRules).forEach(function (rule) {
    description = description.split(rule).join('');
  });
  description = description.replace(/\n{3,}/g, '\n\n').trim();
  form.setDescription([description].concat(currentRules).filter(Boolean).join('\n\n'));
}

function addTextToDescription_(form, text) {
  const description = form.getDescription() || '';
  if (!description.includes(text)) form.setDescription(description + '\n\n' + text);
}

function deleteQuestionIfPresent_(form, title) {
  const item = form.getItems().find((candidate) => candidate.getTitle() === title);
  if (item) form.deleteItem(item);
}

function updateMultipleChoiceQuestion_(form, oldTitle, newTitle, choices, helpText) {
  const item = findQuestionByTitle_(
    form,
    FormApp.ItemType.MULTIPLE_CHOICE,
    [oldTitle, newTitle]
  ).asMultipleChoiceItem();
  item.setTitle(newTitle).setChoiceValues(choices).setHelpText(helpText).setRequired(true);
}

function upsertMultipleChoiceQuestion_(form, acceptedTitles, newTitle, choices, helpText) {
  const match = form.getItems(FormApp.ItemType.MULTIPLE_CHOICE).find(function (item) {
    return acceptedTitles.indexOf(item.getTitle()) !== -1;
  });
  const item = match ? match.asMultipleChoiceItem() : form.addMultipleChoiceItem();
  item.setTitle(newTitle).setChoiceValues(choices).setHelpText(helpText).setRequired(true);
  return item;
}

function upsertListQuestion_(form, acceptedTitles, newTitle, choices, helpText) {
  const match = form.getItems(FormApp.ItemType.LIST).find(function (item) {
    return acceptedTitles.indexOf(item.getTitle()) !== -1;
  });
  const item = match ? match.asListItem() : form.addListItem();
  item.setTitle(newTitle).setChoiceValues(choices).setHelpText(helpText).setRequired(true);
  return item;
}

function updateParagraphQuestion_(form, oldTitle, newTitle, helpText) {
  const item = findQuestionByTitle_(
    form,
    FormApp.ItemType.PARAGRAPH_TEXT,
    [oldTitle, newTitle]
  ).asParagraphTextItem();
  item.setTitle(newTitle).setHelpText(helpText);
}

function updateParagraphQuestionIfPresent_(form, acceptedTitles, newTitle, helpText) {
  const match = form.getItems(FormApp.ItemType.PARAGRAPH_TEXT).find(function (item) {
    return acceptedTitles.indexOf(item.getTitle()) !== -1;
  });
  if (match) match.asParagraphTextItem().setTitle(newTitle).setHelpText(helpText);
}

function updatePageBreakHelpText_(form, title, helpText) {
  const match = form.getItems(FormApp.ItemType.PAGE_BREAK).find(function (item) {
    return item.getTitle() === title;
  });
  if (!match) throw new Error(`Could not find page section in "${form.getTitle()}": ${title}`);
  match.asPageBreakItem().setHelpText(helpText);
}

function updateCommitmentQuestion_(form, title, statements) {
  const item = findQuestionByTitle_(form, FormApp.ItemType.CHECKBOX, [title])
    .asCheckboxItem();
  const validation = FormApp.createCheckboxValidation()
    .setHelpText('Select every statement to continue.')
    .requireSelectExactly(statements.length)
    .build();
  item.setChoiceValues(statements).setValidation(validation).setRequired(true);
}

function findQuestionByTitle_(form, itemType, acceptedTitles) {
  const match = form.getItems(itemType).find(function (item) {
    return acceptedTitles.indexOf(item.getTitle()) !== -1;
  });
  if (!match) {
    throw new Error(
      `Could not find question in "${form.getTitle()}": ${acceptedTitles.join(' / ')}`
    );
  }
  return match;
}

function formLinks_(form) {
  return {
    id: form.getId(),
    responderUrl: form.getPublishedUrl(),
    editorUrl: form.getEditUrl(),
  };
}

function prepareStartSheet_(sheet) {
  sheet.clear();
  sheet.setFrozenRows(3);
  sheet.setColumnWidth(1, 210);
  sheet.setColumnWidth(2, 560);
  sheet.getRange('A1:B1').merge();
  sheet.getRange('A1')
    .setValue(`Stauffer Femineers ${RECRUITMENT.year} Recruitment Hub`)
    .setFontSize(18)
    .setFontWeight('bold')
    .setFontColor('#ffffff')
    .setBackground('#33286b');
  sheet.getRange('A2:B2').merge();
  sheet.getRange('A2')
    .setValue('PRIVATE: Do not publish this spreadsheet or student responses on GitHub Pages.')
    .setFontWeight('bold')
    .setFontColor('#9c2d2d')
    .setBackground('#fde2df');
  sheet.getRange('A3:B3')
    .setValues([['Resource', 'Link']])
    .setFontWeight('bold')
    .setFontColor('#ffffff')
    .setBackground('#6341c6');
}

function writeStartSheet_(sheet, links) {
  const rows = [
    ['Recruitment landing page', RECRUITMENT.siteUrl],
    ['Program roadmap', RECRUITMENT.roadmapUrl],
    ['New student — responder link', links.newStudent.responderUrl],
    ['New student — editor link', links.newStudent.editorUrl],
    ['Returning member — responder link', links.returningMember.responderUrl],
    ['Returning member — editor link', links.returningMember.editorUrl],
    ['Family commitment — responder link', links.familyCommitment.responderUrl],
    ['Family commitment — editor link', links.familyCommitment.editorUrl],
    ['Teacher recommendation — responder link', links.teacherRecommendation.responderUrl],
    ['Teacher recommendation — editor link', links.teacherRecommendation.editorUrl],
    ['Recruitment window', RECRUITMENT.window],
    ['Maximum confirmed members', RECRUITMENT.capacity],
  ];
  sheet.getRange(4, 1, rows.length, 2).setValues(rows);
  sheet.getRange(4, 1, rows.length, 1).setFontWeight('bold');
  sheet.getRange(4, 2, 10, 1).setFontColor('#0b57d0').setFontLine('underline');
  sheet.getRange(4, 1, rows.length, 2).setWrap(true).setVerticalAlignment('top');
  sheet.getRange(4, 1, rows.length, 2).applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY);
  sheet.getRange(rows.length + 5, 1, 1, 2).merge();
  sheet.getRange(rows.length + 5, 1)
    .setValue('Before sharing: open each form’s Settings, confirm who may respond, verify that the family form is accessible to families, test one submission, and keep response access limited to authorized staff.')
    .setWrap(true)
    .setFontWeight('bold')
    .setBackground('#fff2cc');
}

function getSavedRecruitmentLinks_() {
  const saved = PropertiesService.getScriptProperties().getProperty(RECRUITMENT.propertyKey);
  if (!saved) {
    throw new Error('No saved recruitment setup was found. Run createRecruitmentForms() first.');
  }
  return JSON.parse(saved);
}

function setAllFormsAcceptingResponses_(accepting) {
  const links = getSavedRecruitmentLinks_();
  const formEntries = [
    links.newStudent,
    links.returningMember,
    links.familyCommitment,
    links.teacherRecommendation,
  ];
  formEntries.forEach(function (entry) {
    const form = FormApp.openById(entry.id);
    form.setAcceptingResponses(accepting);
    if (!accepting) {
      // Google only accepts a custom closed message after the form is closed.
      form.setCustomClosedFormMessage(CLOSED_FORM_MESSAGE);
    }
  });
  console.log(accepting ? 'All recruitment forms are open.' : 'All recruitment forms are closed.');
}

function logRecruitmentLinks_(links, heading) {
  console.log(heading);
  console.log('Private response spreadsheet: ' + links.responseSpreadsheet.url);
  console.log('New student responder form: ' + links.newStudent.responderUrl);
  console.log('Returning-member responder form: ' + links.returningMember.responderUrl);
  console.log('Family commitment responder form: ' + links.familyCommitment.responderUrl);
  console.log('Teacher recommendation responder form: ' + links.teacherRecommendation.responderUrl);
}
