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
| Back Office · 日本語 | `T-Book` → `T-Dialog` → `T-Material` ↔ `T-Settings` → `T-Created` · `T-Courses` → `T-Course` → `T-CourseBook` · `T-Queue` → `T-Detail` → `T-List` → `T-Review` · `T-DashTopic` → `T-DashGroup` ↔ `T-DashStudent` | 1440 × 900 |
| Back Office · English | same, `-en` suffix | 1440 × 900 |

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
  `LOAvailabilityTable` in `school-portal-admin`'s syllabus squad), per course, so
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
  `T-Courses` and a Share Access button on `T-Course`. A student who scans it or
  types the code is enrolled and sees the course's LOs from their start dates.
  The course's **Student** tab on `T-Course` (production's `StudentTab`: Student
  Info, Action, search and filters, the student table) lists who is in the
  course, with one proposed column, **Joined via** — QR code / code entered with
  the join time, or added manually with who added them.
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

## Publishing

The canvas is a Claude Design artifact. To republish after editing `gen.py`,
regenerate, then publish `project/canvas.json` and the changed `project/*.dc.html`
to the artifact URL above (the index must be merged onto the live copy first,
because viewers can move notes and boards on the page).
