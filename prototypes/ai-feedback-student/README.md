# AI Feedback — prototype (Back Office + student PC + student mobile)

Clickable prototype of AI Feedback for universities (Kindai 地域環境統計学
exercise, teacher-in-the-loop, revise loop): the teacher sets the assignment up
in the Back Office, the student submits on PC or phone, the teacher reviews and
returns. It accompanies `PRDs/ai-feedback-university-prd.md`.

Live canvas (Claude Design artifact, comments live there):
https://claude.ai/artifact/FYtGUxxHgPhzWnENGtgLmE

The PM decisions taken in the canvas comments (18–21 Sep 2026) are consolidated,
dated and grouped by screen, in the PRD's section **C11**; the notes below and the
sticky notes on the canvas are the per-screen record.

## Layout

| Row | Boards | Size |
|---|---|---|
| PC · 日本語 | `Main` → `02-Assignment` → `03-Pending` → `04-Feedback` → `06-Resubmit` → `07-Pending2` → `08-Feedback2` → `05-Todo` | 1280 × 800 |
| PC · English | same, `-en` suffix | 1280 × 800 |
| Mobile · 日本語 | `M-Main` → `M-Assignment` → `M-Camera` → `M-Crop` → `M-Pages` → `M-Pending` → `M-Feedback` → `M-Sheet` | 375 × 812 |
| Mobile · English | same, `-en` suffix | 375 × 812 |
| Back Office · 日本語 | `T-Book` → `T-Dialog` → `T-Material` ↔ `T-Settings` → `T-Created` · `T-Courses` → `T-Course` → `T-CourseBook` · `T-Queue` → `T-Detail` → `T-List` → `T-Review` · `T-DashTopic` → `T-DashGroup` ↔ `T-DashStudent` · `T-DashAI` | 1440 × 900 |
| Back Office · English | same, `-en` suffix | 1440 × 900 |
| AI Practice · 日本語 | `P-Dialog` → `P-Source` ↔ `P-Detail` (BO, 1440 × 900) · `P-Sets` → `P-Crop` → `P-Setup` → `P-Wait` → `P-Practice` · `P-Print` (PC, 1280 × 800) · `M-PSets` → `M-PCrop` → `M-PSetup` → `M-PWait` → `M-PPractice` (mobile, 375 × 812) | mixed |
| AI Practice · English | same, `-en` suffix | mixed |
| AI Grading · 日本語 | `G-Dialog` · `G-Detail` · `G-LOs` → `G-Import` → `G-Process` → `G-Overview` → `G-Mark` · `G-Compare` (BO, 1440 × 900) | 1440 × 900 |
| AI Grading · English | same, `-en` suffix | 1440 × 900 |
| AI Grading, student side · 日本語 | `Q-Detail` → `Q-Submit` → `Q-Preview` → `Q-Result` → `Q-Done` → `Q-Review` · `Q-Chat` · `Q-Resub1` → `Q-Resub2` → `Q-Resub3` → `Q-Resub4` (PC, 1280 × 800) · `MQ-Detail` → … → `MQ-Review` · `MQ-Chat` · `MQ-Resub1` → … → `MQ-Resub4` (mobile, 375 × 812) | mixed |
| AI Grading, student side · English | same, `-en` suffix | mixed |

Every board has a 日本語 / English toggle (header). The student boards carry a
PC / Mobile / 先生（BO） pill (bottom-left) that jumps to the twin screen or into
the Back Office; the Back Office boards carry a 先生 / 生徒 switch in the left nav that jumps to the
student's screen, so a setting can be read from both sides. The DEMO pill on the
waiting screens simulates the teacher approving and returning the feedback.

## Files

- `gen.py` — the single source of truth. All copy (JA and EN), CSS, icons and
  screen builders live here. Run `python3 gen.py` to regenerate both outputs
  below.
- `project/*.dc.html` — one Design Component page per artboard (generated).
- `project/canvas.json` — the canvas index: board frames, order, sticky notes
  (generated; the notes record the PM decisions behind each screen).
- `deploy/` — the same screens as a standalone site for Railway: generated
  `public/*.html`, a hand-written `public/dc-shim.js` that replaces the canvas
  runtime, and a dependency-free Node server. See `deploy/README.md` for the
  Railway setup (Root Directory `prototypes/ai-feedback-student/deploy`).

Design language: Manabie Learner app Figma (`[Final] Learner app`), Noto Sans JP,
`#f2f2f4` background, `#395ad2` primary, 8 px cards with `0 8px 16px rgba(0,0,0,.1)`.
Mobile snap → crop → pages flow follows the unifiedapp student mock
(`jamessim-source/unifiedapp`, `CameraScreen` / `CropScreen` / `ReviewScreen`).

## Decisions embodied (2026-09-18, PM)

- To the student, the teacher gives the feedback. No AI wording on waiting or
  returned screens; no teacher name; no review-step framing.
- Teacher reviews only after the due date; nothing is returned before it.
  Files / pages / typed text are replaceable until the due date.
- No AI-use declaration, no self-check (self-report is not evidence).
- No AI "next step" card — guidance stays inside each 改善点; next steps are the
  teacher's, in their note.
- 提出の基本条件 (basic requirements) is a Back Office field on the assignment,
  separate from the rubric; the six criteria chips are the rubric criteria.
- Resubmission is a per-assignment Back Office setting, default off.
- Submission modes: file / photos of handwritten pages / typed answer
  (500-character limit, confirm before the checks run); which modes an
  assignment accepts is a Back Office setting on the AI Feedback LO.
- One feedback layout for every submission type; mobile opens a bottom sheet
  on the tapped underline; PC highlights and centres both sides.
- AI Feedback is a new LO type; the assignment is created at the LO level in
  Book → Chapter → Topic → LO.

## Back Office direction (2026-09-19, PM — overrides the V1.1 design)

The V1.1 PRD and the teacher-dashboard Figma had teachers creating classes and
assignments in a separate area, outside the LMS book/course structure. That is
overridden: AI Feedback is set up inside **Book Management**, where the teacher
already builds the course.

- **AI Feedback is one more LO type** in the Add Learning Objective dialog,
  alongside Random Activity / Learning Objective / Flash Card / Recording
  Assignment / Practice Submission / External Content. As in production
  (`DialogCreateLearningMaterial`, fields per type via `getVisibleFieldsByLMType`),
  the whole LO is created inside that one dialog — General Info, then Settings —
  and Confirm creates it **Unpublished**, highlighted in the tree. Publishing is
  a separate action; there is no "save and publish" at creation.
- The Back Office chrome follows the `manabieV5` theme and the `BookDetail`
  accordion tree from `school-portal-admin` (checked on 2026-09-19 against the
  prototype generated from that code); the nav follows the live LMS 2.0 tenant.
- **Dates** (2026-09-22, PM — supersedes the LO-level dates of 19 Sep): the
  start date, the due date and the resubmission deadline belong to the **course**,
  not the LO. They are set on production's Course Management › Books › book ›
  **Learning Objectives Availability** page (`CourseBookDetail`,
  `LOAvailabilityTable` in `school-portal-admin`'s syllabus squad), per course —
  the values are the course's study plan items' start and end, read from and
  written to the study plan backend (PM, 24 Sep) — so
  one book assigned to two courses runs on two schedules (`T-Courses` →
  `T-Course` → `T-CourseBook`). The Add LO dialog and the LO's Settings tab point
  there instead of carrying dates; resubmission stays a per-LO toggle, default
  off, with its deadline in the same course table (a proposed column, not yet
  decided by the PM). The student still sees the LO on the course tab from the
  start date, not clickable before it; submits and replaces until the due date;
  the teacher reviews after it.
- **Join by QR code**: the AI Tutor class page's existing **Share Access**
  dialog (`AIClassShare`: a QR code of the class code with Download, the code
  itself with Copy, Close) is reused for the course — a share icon on each row of
  `T-Courses` and a Share Access item in the ⋮ menu on `T-Course`. A student who scans it or
  types the code is enrolled and sees the course's LOs from their start dates.
  The course's **Student** tab on `T-Course` (production's `StudentTab`: Student
  Info, Action, search and filters, the student table) lists who is in the
  course, production's columns minus Study Plan (24 Sep: the dates on
  `T-CourseBook` auto-create the course's study plan and enrol every student,
  so the column has nothing to show a university tenant). A Joined via column
  was proposed and dropped (PM, 23 Sep). **Extend due date** (V2 proposal): a
  row action opens a dialog with this student's end date per AI Feedback LO;
  the course's dates stay. `T-CourseBook` also shows an LO added after the
  dates were set — empty Start/End with a warning line.
- **Add course**: `T-Courses` › Add course opens production's full-screen
  `DialogUpsertCourse` with `CourseForm` (course icon, Course Name, Location,
  Teaching Method, Course Type, Subject, Book); Save adds the
  course to the list with the created-successfully snackbar. Nothing in it is new
  for AI Feedback; it is where the book gets linked to a course.
- **Submission methods**: which of file / photos / typed the LO accepts, with the
  500-character limit attached to typed.
- **Pre-submission checklist**: on the LO's own page (opened from the tree, as a
  regular LO is opened to author its questions), extracted from the teacher's own
  material (the brief, the marking criteria) and editable, every condition
  carrying the source it came from. Conditions gate the submission; the rubric
  criteria shape the comments. Neither carries a score.
- **Teacher in the loop**: a toggle. On, the draft waits for the teacher to
  review, edit and return it. Off, feedback is returned automatically after the
  due date. Either way the student is never told AI was involved.
- **Two homes**: Book Management sets the LO up (tree, dialog, content page).
  Processing submissions — the queue across LOs, an LO's overview, its
  submissions, review and return — lives under **Course › Submission Grading** (`ToReviewListPage`), production's
  existing home for submissions waiting on the teacher, in its format: tabs, filter
  bar, status segments with counts, the wide table, and the grading-detail layout.
  AI Feedback statuses use the marking tones: Not Reviewed / In Review / Returned /
  Sent Back, plus a secondary chip (Auto-returned, Resubmitted).
- **Dashboard** (2026-09-20, PM): the AI Feedback overview is fitted into
  production's `GroupDashboard` and `StudentDashboard`, not given a page of its
  own. Group, Topic Dashboard mode (production's default, where the Dashboard
  menu lands): production's chapter / topic / average score / completion table,
  only for topics with an AI Feedback LO, with one added AI Feedback column —
  the LO with its start and due dates, submitted / waiting / returned counts,
  ★ count, and one tagged insight line (missed / going well / worth showing /
  submissions) read by an LLM pass over the submissions and their draft
  feedback along the rubric, the LLM's top-priority one shown; no expansion,
  quotes or counts behind it (PM: the teacher checks the submissions
  themself, the line only alerts). Filters opens production's panel plus AI
  Feedback start / due date ranges. Group, LO Dashboard mode: the student × LO
  matrix alone (an overview paper built from the PRD was tried block by block
  and removed or merged, PM). In the matrix an AI Feedback LO shows
  the submission status per student in the marking tones, a highlighted cell
  adding the teacher's few-word reason and opening that submission,
  and its header reads Submitted / Waiting / Returned plus a ★ count of
  submissions the teacher highlighted as examples for the class (set from the
  review screen's "Highlight for class"; the Submission Grading tables mark
  those rows with the star and carry a working "Highlighted only" option
  inside Filters (PM: under Filters, not a chip in the bar),
  and the student's returned screen carries a star line in the teacher's note
  card). Two insight panels below the matrix (comments by rubric criterion,
  requirements that stopped a submission) were removed (PM: not required).
  Student: AI Feedback LOs sit in the expanded LO rows with their status where a
  score would be, and the inner table gains three feedback columns — Status
  (the status chip, its secondary chip and the date it was reached; Completed
  for unscored LOs sits here too), the flagged criteria (those that drew an
  improvement comment, marked when fixed on resubmission), and a link into
  the review — with the ★ reason under the LO name (a separate AI Feedback
  paper below the table was merged into these rows, PM; a comment-count
  column was tried and dropped).

## AI Grading fitted in (2026-09-30, PM)

The Paper Submission LO from the AI Grading prototype
(`claude.ai/artifact/Y4bgKxLmeTo86Zi8cBBzvn`, US-1 to US-8) is drawn as the
Session 7 check-up quiz — sat on paper in class, scanned on the copier,
bulk-imported, AI-marked, reviewed and returned — so it sits beside the AI
Feedback and AI Practice LOs on the same surfaces:

- **Book Management (T1, T2, G1, G2).** The quiz row carries the purple pencil
  disc and the 紙提出物 chip; the Add LO type menu lists 紙提出物（AI採点）as
  NEW; the dialog has Paper Count, Manual Grading fixed On, the approval
  switch, the NEW Allow student to submit switch (default Off), Score to Pass /
  Capped Score / Password. The LO's Content tab (in Book Management, PM 30 Sep)
  has one upload area for the Question and Answer PDFs and the flat question
  list beside the sheet, draft until SAVE, and (PM 30 Sep) an optional
  Rubrics card: criteria with weights AI generates from the uploaded
  materials, as an editable list (edit, delete, add, weights must total
  100%), generated on demand or at Process time with a switch.
- **Submission Grading (T9, G3–G7).** The Learning Objectives tab is live, with
  paper and feedback LOs and their progress (a paper LO opens its submission
  list); ⋯ opens Bulk Import Submissions
  (layout, upload, counts) → the background job and the editable result table
  with the rows that need attention → the Overview matrix (approval workflow,
  Teacher / Admin view, per-question scores, course average) → the marking
  review overlay (students, the scan with the AI's ○ / ✕, per-question ○ △ ✕,
  Confirm and Next).
- **Course Management and dashboards.** T8 shows the paper LO's icon; its
  scores already sit in the score columns on T14 / T15.

- **Student web and app (Main, M1, To-do 8, Q1–Q12; 30 Sep, PM).** The
  student side of the same LO, from `jamessim-source/aigradingv1`
  (`apps/frontend/src/screens/student`, the deprecated SPA that is the
  acceptance spec): the quiz row on the course tab and in To-do (shown only
  because the LO's Allow student to submit is On — G1 now has it On) →
  assignment details (instructions, submission details, the three steps) →
  Take Photo / Upload with the photo tips and the two analysis errors
  (Wrong assessment, Photo unclear — DEMO) → the pages carousel, Add More up to
  5 photos or 1 PDF, Confirm & Analyze with the analyzing progress → the
  analysis results (the AI's ○ / ✕ on the sheet, the question breakdown in
  green / amber / red with one line of AI feedback per question against the
  LO's answer key (PM 30 Sep, in place of the question tag), the total; read-only — the student never edits a score,
  PM 30 Sep, so the source's self-marking mode is not carried) → Submit to Teacher → submitted (the AI's
  8/10, awaiting teacher review) → returned (the teacher's △ on Q5 from G7,
  9/10, the changed row labelled, teacher feedback). The student's sheet is
  the one the teacher marks on G7; the 9/10 is the score on T14 / T15. The
  source's My Classes and Add Class by QR / code are not carried — the LMS
  course and the course QR (T6) already do that.

- **Grading operations from the Correspondence proposal deck (30 Sep, PM).**
  From the Kindai Correspondence AI Feedback proposal (slides 10–15, 23,
  27–30): confidence triage on G6 (Needs review / Likely fail / Likely pass
  boxes that filter, a threshold preset that re-buckets rows, Confirm likely
  passes with the spot checks held out, verdict / reason / confidence per
  row, the false-pass counter); evidence highlighting on G7 (a transcript
  mode with met / needs review / missing colouring, key and rubric beside
  each answer, AI notes on split verdicts and similar answers, the verdict
  and confidence in the header); `G-Compare`, every answer to one question
  side by side in three columns with similar answers flagged; and on the
  student side the strengths / to improve / suggested fix summary with Ask
  AI on Q4, Q6 and the mobile pair, plus the Ask AI chat (`Q-Chat`,
  `MQ-Chat`) guided along the textbook, visible to the teacher. Confidence,
  thresholds and evidence highlighting are in development on the deck;
  the values shown are illustrative.
- **Returned for resubmission and version 2 (30 Sep, PM).** The other
  branch from the submitted state: G7 gains Return for resubmission; the
  student gets the request with the deadline and Q5 flagged (`Q-Resub1`),
  ticks last time's comments and photographs the rewritten page
  (`Q-Resub2`), checks the revision — what changed, the AI's criteria
  check, the history — and submits version 2 (`Q-Resub3`), then reads the
  returned version 2 with the submission history (`Q-Resub4`); the same on
  mobile (`MQ-Resub1`–`MQ-Resub4`). The pass branch (Q6) stays as the main
  story; both are reachable from the DEMO pills on Q5.

Not drawn: the Question Tag master and CSV book import (Master Data), the
paper LO's rows in the Submissions tab, the student's row on the Overview
matrix as an app submission, a teacher-feedback field on the marking review
(the returned result shows one, from the source). Student self-marking is
out by decision, not omission (PM, 30 Sep).

## AI feedback before submission (2026-09-29, PM)

A per-LO switch, 提出前のAIフィードバック / AI feedback before submission, default
off, as a fourth Settings block in the Add LO dialog (T2) and a row on the
LO's Settings tab (T4). On, the helper states that the student gets AI feedback
on a draft and can revise before submitting, that it is not teacher-reviewed
and does not count as a submission. The student-side flow is not drawn yet.

## AI Practice fitted in (2026-09-24, PM)

The Similar Questions Practice feature (`jamessim-source/AIpractice`: `README.md`,
`docs/prototype-plan.md`, `docs/c10-finalized-logic.md` — the PRD's C10 as the PM
decided it — the `contract/openapi.yaml` + `mock-service/seed.py` mock, and Koki's
clickable prototype on branch `prototype`) is drawn as one more LO in the same
Kindai statistics course, so every existing surface shows it beside the AI
Feedback LO rather than in a separate demo:

- **Book Management (T1, T2, P1–P3).** Topic 7-1 gains 第7回 類題演習（相関分析）,
  a plain LO with `ai_practice = true`, linked to the Session 7 lecture-slides
  PDF LO. The Add LO type menu lists 類題演習 LO (NEW); the dialog's Settings
  block is the required **Linked source LO** picker fed by the book's eligible
  LOs, with the empty-state copy, the hidden-fields note (no max score, pass
  score, manual grading, AI Tutor or password) and the flag / tenant-setting
  gate (`Syllabus_BackOffice_AIPractice` + `syllabus.ai_practice.is_enabled`).
  The source LO's Settings tab carries **Available as practice source** —
  locked with the reason once students have sets — and **Linked by**; the tree
  marks it 演習の元. The practice LO's own page shows only the linked source LO
  in Settings (PM, 24 Sep; a "Visible to students as" paper was drawn and
  removed the same day), plus a dashboard button; the set count, the start-only availability, and the facts that it
  has no completion status, mastery, delete or override are recorded in the
  board's note.
- **Course Management (T8).** The practice LO row is listed with empty date
  cells: whether a practice LO has a start/due-date concept is unconfirmed
  (PM, 27 Sep), so no date is shown for it anywhere — T8, T13, P3.
- **Dashboards (T13–T15).** Topic mode: under 7-1's feedback LO, the practice
  LO in the same shape (PM, 27 Sep) — name, no date line, two chips
  (students with sets, students who completed their sets), one insight naming the
  source question with the lowest accuracy. **Rule (PM, 27 Sep): when there is not going to be something, do
  not state it** — no "no due date", "no completion status", "not printed"
  or hidden-fields notes on any board; the absences are recorded in the
  sticky notes and the PRD instead. LO mode: a practice column whose cells show the set count
  and a score with its accuracy bar — Latest Score is correct / answered across
  the student's sets, Highest Score the best single set — and the Latest /
  Highest Score toggle is live when a practice LO is in view (PM, 28 Sep). Student Dashboard: the practice
  row shows 途中 with its sets line, no score, and a link into the group view.
- **AI Dashboard (T16, `T-DashAI`, 6 Oct).** Production's AI Tutor Dashboard
  (`Dashboard/modules/ai-dashboard` on the `backoffice` branch: Add Student, the
  Lens / start / end date form, the overview cards, Student Usages with the Chat
  History Overview in the expanded row) with AI Feedback **as the Back Office code has
  it** (PM, 6 Oct: the AI feedback code is not linked to the LO; replace with what is
  actually available). There, AI Feedback is the AI Tutor's feedback snap (graph type
  FEEDBACK beside Snap-to-ask), optionally tied to an AI Tutor Assignment (title,
  subject, overall question, acceptance criteria, publish + due date; Started / Snaps /
  Completed). The board adds: production's Feedbacks generated card plus the
  assignment's analysis, two per-student columns (feedback snaps, assignment status),
  the student's feedback snaps under the chat history, and **View → a drawer with the
  thread** in the learner app's AI Feedback format (PM screenshots, 6 Oct): an
  Extracted text / Feedback toggle — the work as read with numbered teal / red markers
  and dashed underlines, then a Summary card and numbered per-criterion cards (quote,
  comment, Ask AI). No like / dislike or comments — the PM confirmed the feedback flow
  has none. Counts only, no rates.
- **Student PC (Main, 05-Todo, P4–P9)** and **mobile (M-Main, P10–P14).** The
  LO list and To-do gain the ✦ practice card (set count only, no completion
  chip). The practice screen follows Koki's prototype trimmed to the PRD
  rules: StatBox (問題数 / 正解数, rounds of 10), selectable set rows each with a
  print icon (a generated set can be printed at any point, finished or not —
  PM, 24 Sep), the ＋ row into the crop, and the CTA that follows the
  selected set (print for a finished set; resume with print beside it for an
  unfinished one). Crop reuses the Mana AI frames relabelled
  演習をつくる →; 切り取った範囲 shows the detected questions with a per-question
  slider capped by the shallowest remaining stock and the live total, and the
  DEMO pill shows NO_MATCH (*Please ensure your crop contains the question in
  full and try again.*) before any count is chosen. The wait state is for
  creation only (retrieval, not generation). Practice is the AI Tutor web
  app's MCQ module: one attempt per question, explanation, 次へ, round end.
  Print renders question and options only — never the source question or the
  stock.

## Publishing

The canvas is a Claude Design artifact. To republish after editing `gen.py`,
regenerate, then publish `project/canvas.json` and the changed `project/*.dc.html`
to the artifact URL above (the index must be merged onto the live copy first,
because viewers can move notes and boards on the page).
