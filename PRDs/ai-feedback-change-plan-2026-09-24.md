# AI Feedback — change plan from the 24 Sep AI Direction Discussion

**Source:** Weekly AI Direction Discussion, 24 Sep 2026 — [Notes by Gemini](https://docs.google.com/document/d/1y04oYHnmQ1vFHW5JXALpB6ycbevCn1j6TqNYbOv6Jzw/edit) (quick notes, full notes and the full transcript, all read). Attendees: James Sim, Bunsuke Itamura, Koki Misawa, Trieu Le Hong; Takuya Homma invited, did not attend.
**Against:** `PRDs/ai-feedback-university-prd.md` v1.6 and the prototype [S20] (Version 159).
**Status of this document:** a plan for the PM to confirm. Where the meeting reached alignment, the change is listed as *to do*; where it left the call to the PM, the options are listed with a recommendation. Nothing in Parts A–C of the PRD has been changed yet on the strength of the meeting; the meeting's facts are recorded in the PRD's Section 1.5.4 with provenance.

---

## 0. In one screen

| # | What the meeting aligned on | What it changes for AI Feedback | Size | When |
|---|---|---|---|---|
| 1 | **Scoring and tabulation are allowed inside the AI Feedback format** (Bunsuke, Koki; James agreed) | Reverses the PRD's "scoring is architecture, not a gap" position (C2, C3, C12 P7/P9). Feedback stays primary; a score becomes an optional secondary; several questions per LO as tabs | Large | Direction now; **V1 (Kindai trial) stays feedback-only** unless the PM decides otherwise (§1) |
| 2 | **One engine** — the AI Marking engine generates comments for feedback, grading and marking; the LOs and UIs stay separate | Confirms C2/C7; C7 should name the engine and the split (engine shared, LO type and UI distinct) | Small | PRD edit now |
| 3 | **Course and book UX refactor is a separate project stream** (James with Carlo's team; Canvas as the reference) | Out of this PRD's scope; T6–T8 keep production's flow on purpose. Koki's asks become that stream's input | Medium (other stream) | Stream to open; not gating the trial |
| 4 | **Dates: UI as drawn, backed by an auto-created study plan** — no new date table, study plan concept hidden for universities, no sequencing on the UI, complex remote-school setups via CSV, book-level access dates to go | Confirms W11 and extends it: the data model for C7, the per-student extension path (V2), and a **V1 fallback without dates** if the study plan work does not fit the trial | Medium | Data model now; **PM decision: V1 with or without dates** (§4) |
| 5 | **Dashboards: Score + Status per LO row, no Max score; submission history behind the ▾; blank where a metric does not apply; three statuses and key metrics per LO type** | Redraw T14 (LO Dashboard matrix) and T15 (Student Dashboard); T13 (Topic) stays a summary. Koki sends mockups | Medium | Redraw after Koki's mockups (this week) |
| 6 | **LO-type restructuring** on Monday 28 Sep; the weekly reflection is the **same AI Feedback LO type, renamed**, with a typed answer | C5 and C10.3 wording; no new LO type. Prepare the AI Feedback LO's requirements for Monday | Small | Monday |
| 7 | QR on the course for students to join (Koki) | Already drawn on 23 Sep (T6 row icon, T7 ⋮ › Share Access) | Done | — |

Action items the notes record: **James** — refactor the course/book UX with Carlo's team; **the group** — enable tabulation and scoring in the feedback interface; **Koki** — adjust the group and student dashboard designs and send them to James; **the group** — discuss the LO restructuring on Monday.

---

## 1. Scoring and tabulation inside AI Feedback

**What was said.** Koki: a university homework set as AI Feedback *"still needs score"*. Bunsuke: *"you should add a score here for feedback… I think we should allow for tabulation in feedback, and we should add scoring"*; but *"the main thing is feedback; scoring is secondary"*, and merging the grading and feedback UIs *"will look fairly clunky"*. Koki on timing: *"for short time I think this is totally fine, I'm thinking about what the future will look like"*. Recorded decision: **Integration of tabulation and scoring in feedback — aligned.**

**What it changes.**

| Where | Today | Change |
|---|---|---|
| PRD C2 "Scoring is not in scope here, and that is the architecture rather than a gap" | Scoring belongs to AI Grading/Marking only; the 11 Sep weight removal is "settled" | Rewrite: **feedback is the primary output; a score is an optional secondary output of the same LO**, off by default. Keep: AI Grading/Marking remain the scoring products for tests and homework sets; AI Feedback is the essay/report LO. The weight removal stays correct for V1 (no score) and is revisited when the score is on |
| PRD C3 rows "Instructor edits the draft — there is no score", "Model is replaced — no score to re-validate" | Assert no score | Add the conditional: *when the LO's score is off* (V1). Add rows for the score-on state (below) |
| PRD C12 P7 / P9 | Engine contract and scoring go to the AI Grading PRD | P7 stands (the contract is still AI Grading's). P9 stands (one feature). Add P12: scoring inside the feedback LO is allowed as an optional secondary; V1 off |
| PRD C10.0 / dashboards | Score columns blank for feedback LOs | Score column shows the score when the LO has one, blank when not (see §5) |
| Prototype T2 / T4 | Settings: window, resubmission, methods, requirements, teacher review | Add a **採点 / Score** switch, default off, with the scale (e.g. 0–100 or the rubric's 0–5 per criterion) — a proposal board, not V1 |
| Prototype T12 review screen | Comments, note, approve / send back | When score is on: a score field beside the note, AI-suggested against the rubric, teacher-editable — proposal |
| Student returned screen (PC 4/7, mobile) | Teacher's note + comment cards | When score is on: the score under the note — proposal |
| Tabs (several questions per LO) | One question, one answer per LO | Design direction only: Q1 / Q2 / Q3 tabs on the LO's content, the submission and the review screen. **Not V1.** Kindai's exercises and reflections are one question each |

**Decision for the PM.** V1 = the Kindai trial (preprod 1 Oct, release 5 Oct, live 6 Nov). Recommendation: **V1 ships feedback-only as drawn**; the PRD changes its language now so the architecture does not forbid a score, and the score switch and tabs are drawn as V2 proposal boards for the Monday LO discussion. Reason: Koki himself called the current design fine for the short term, the trial's professor keeps scoring with himself [S16], and adding a score touches the review screen, the student screens, the engine output and both dashboards at once.

**Open questions it creates (for C11.9):** whose score is it — AI-suggested and teacher-confirmed, or teacher-entered only; one score per LO or per criterion (the Kindai six-dimension 0–5 rubric suggests per criterion); does a resubmission replace the score or add a second one; does a scored feedback LO feed the same score columns AI Marking feeds.

---

## 2. One engine, separate LOs

**What was said.** Bunsuke: *"we should not use different engines for feedback, grading and marking; this should all be the same… marking itself is the engine right now, so we should keep reusing that."* Koki: *"the UI is the difference, right?"* — agreed. Bunsuke: *"the LO will be two different LOs because the UIs are very different."* James: for a scoring set that needs deep feedback on one essay question, *"extend the marking or grading UX… this can be linked from a specific question"* rather than merge the two UIs.

**What it changes.** Nothing in scope. C7's first paragraph should say it plainly: **the comment-generation engine is the AI Marking engine, shared by AI Marking, AI Grading's feedback and AI Feedback; the AI Feedback LO type and its UI are distinct.** Add the "deep feedback linked from a grading question" idea to the AI Grading PRD's inheritance list (C12), not here.

---

## 3. Course and book UX refactor — a separate stream

**What was said.** Koki: get to the course's dashboard *"without going through the book"*; course home → group dashboard, add LOs from the course, assign an LO to a class (*"doesn't mean that you assign the entire course"*), a QR on the course; *"refer to the Canvas UX… they have the start date, due date, a list of modules, and you assign the class."* James: *"to refactor the UX for course and book I will take that as a separate project, to work with Carlo's team… I was using the existing flow so we don't get confused what's new and what's old."* Recorded decision: **Refactoring course and book user experience — aligned, separate stream.**

**What it changes.**
- PRD C2 out-of-scope gains a line: the Course › Book UX refactor (course home, modules, class targeting) is a separate stream; this PRD reuses production's Course Management, Book Management and Submission Grading as they are.
- PRD C11.10 gets the reason T6–T8 look like production: deliberate, so the AI Feedback additions are visible against the old flow.
- Prototype: **no change**. The QR is done (T6 row icon, T7 ⋮ › Share Access).
- A one-page brief for the new stream, owner James, partner Carlo's team, inputs: (a) course home = the group dashboard, (b) add an LO from the course, (c) assign an LO to a class or a person (Canvas "assign to"), V1 for everyone, (d) start/due per module, (e) QR on the course, (f) hide "study plan" for universities and show one date table (§4). Reference: Canvas modules; Moodle for per-student overrides.

---

## 4. Dates — the study plan backend, one table on the UI

**What was said.** Koki: *"front end you can make it look like one table, but back end you refer to a different table… you still need the study plan table because you have to be able to change at the individual level."* Bunsuke: *"basically the start/end date here becomes an auto-created study plan in the back end… I think that's better."* Koki: *"your design UI is okay… I'm talking about the data structure."* Both: no new date table (*"definitely not"*); remove the ability to change the sequence on the UI (study plan follows the book); keep complex remote-school splits (one book, nine study plans by joining month) in CSV, not UI; Bunsuke wants the **book-level access start/end dates removed** so there is one date concept. On V1: James — the due date *"was just a talking point, not firm"*; Koki — *"in that case you can release without having due date, because that refactoring takes time… V1 fine, V2 build due date on the study plan structure."* Per-student extension: common in higher education (Canvas, Moodle), *"should not be built in the core structure"*, lives at the student level of the study plan. Recorded decisions: **Reuse study plan structures for submission dates; remove sequencing from the UI; UI optimised for the university's one-to-one structure.**

**What it changes.**

| Where | Change |
|---|---|
| PRD C7 (the To-do date layer) | Already says the dates are the study plan's (W11). Add the model: **saving dates on T8 creates or updates one study plan per course × book automatically**; the study plan's sequence equals the book's; the UI never shows the word "study plan" to a university tenant; per-class dates = one study plan per course (already how two courses on one book work); per-student extension = the study plan's individual level, edited from the Student tab (V2); remote-school multi-pattern splits stay in Study Plan Management and CSV |
| PRD C3 "Due date differs per student or per class" | Add the per-student extension path and mark it V2 |
| PRD C3 rows that depend on dates (start → To-do, due → overdue and refused, extend the due date, resubmission due) | Add the **V1-without-dates fallback** so the PM can choose: the LO appears on the course tab and To-do when published; no overdue state; the teacher reviews at any time; a late submission is accepted; resubmission has no deadline. Five rows change if the fallback is chosen |
| PRD D blocker "course-level submission window drawn but not decided" | Split into: (a) data model — decided today, study plan; (b) V1 with or without dates — PM; (c) Resubmission Due — becomes one more study-plan-item date, still a proposal |
| Backlog for the study plan owner (not this PRD) | Remove sequence editing from the study plan UI; remove the book-level access dates (Bunsuke) — needs an owner and a migration note |
| Prototype T8 | Stands as drawn (Koki). Optional: a small "detail set-up" entry for per-student extension on the Student tab, marked V2 |

**Decision for the PM: does V1 carry dates?** Two paths.
- **A. V1 with dates**, as drawn, on an auto-created study plan. Keeps the 17 Sep To-do decision intact (start populates the To-do, due goes red). Cost: the TL must confirm the auto-create and the T8 write-through fit before 5 Oct.
- **B. V1 without dates**, as Koki suggested. Cheapest; the trial's professor sets deadlines in class. Cost: the To-do fills with every published LO (the 17 Sep problem), no overdue state, late submissions accepted, and the LO Availability page is not used by the trial.
Recommendation: **ask the TL to size A this week; choose B only if A does not fit the trial.** The dates were the answer to a real To-do problem, and the study plan tables already exist.

---

## 5. Dashboards — Score + Status, history behind the ▾

**What was said.** Koki: put the feedback LO in the existing rows of the group and student dashboards; *"define three statuses, then pick key metrics"*, and the same per-LO-type metrics are needed for quizzes and tests. Bunsuke: change the LO-type header and what each cell shows; *"show it for the ones that are relevant and blank for the ones that are not"*; latest and max score are *"not relevant for everything"*; on the group dashboard the ▾ under a score opens all submissions with dates and scores — *"it should be the same"* for feedback. Koki: *"we just need score and status; we don't need max"*; the topic dashboard is *"just a quick link"*, the yellow LO matrix is what people look at. Koki sends cleaned-up mockups today or tomorrow; James applies the principles.

**What it changes.**

| Board | Today | Change |
|---|---|---|
| T14 Group Dashboard, LO mode (the matrix) | Per LO: status chip + secondary chip, ★ reason | Header per LO carries its type; cell = **Status** (Not submitted / Waiting / Returned, plus Resubmitted) and **Score** (blank while the LO has no score); the ▾ opens the submission history (date, status, score per attempt) as the score cells do today |
| T15 Student Dashboard | Columns Learning Objective · Latest Submission · Latest Score · Highest Score · Status · Flagged criteria · View | Drop **Highest Score**; keep one **Score** column (blank for feedback until a score exists) and **Status**; history behind the ▾; keep Flagged criteria as the feedback LO's key metric |
| T13 Group Dashboard, Topic mode | Production table + the AI Feedback column with counts and the insight line | Keep as a summary and quick link; nothing new |
| PRD C10.0, C4 (T13–T15), C11.5–C11.6 | Describe the current columns | Update to the Score + Status rule and the ▾ history; record "blank where not applicable" as the rule for every LO type |

**Sequence.** Wait for Koki's mockups (promised this week), then redraw T14 and T15 in one pass and republish; update the PRD in the same commit.

---

## 6. LO-type restructuring and the weekly reflection

**What was said.** Bunsuke: *"in conjunction we're trying to refactor all the LO types, so we can discuss next Monday"*; AI Feedback is *"not necessarily paper based… you might have typed responses directly into the LMS."* James: weekly reflections are typed, not paper, *"just a weekly reflection — separate"* from Lenosity. Bunsuke: *"so we just need to rename it, but it's the same LO."* James: *"same."*

**What it changes.**
- PRD C5: the weekly reflection is **an AI Feedback LO with the typed method on**, shown to students under its own name; no second LO type.
- PRD C10.3: add that the reflection view reads the same LO type; the 2–3-criterion reflection rubric stays Prof. Yasumoto's to author.
- Prototype: none. The typed path (500 characters, confirm, checks) already exists on PC and mobile.
- **For Monday's LO discussion, bring the AI Feedback LO's requirements on the new type model:** its own type and To-do icon; submission methods file / photos / typed as per-LO settings; dates from the study plan, none on the LO; teacher review and resubmission as per-LO switches; an optional score (§1) and optional tabs (§1) as V2; how a renamed instance (reflection) is represented without a new type.

---

## 7. What to do, in order

| When | Who | Action |
|---|---|---|
| Now | James | Confirm this plan's two decisions: V1 scoring (§1, recommended off) and V1 dates (§4, recommended A pending TL sizing) |
| This week | James | PRD edits that need no further decision: C2 scoring language and the separate-stream exclusion (§1, §3); C7 engine statement and the study plan data model (§2, §4); C5 / C10.3 reflection wording (§6); C11.9 new questions; D blocker split |
| This week | TL (via Trieu) | Size the auto-created study plan + T8 write-through for the 5 Oct release; size the dashboard column changes |
| This week | Koki → James | Dashboard mockups; then T14 / T15 redrawn and republished, PRD C10.0 updated (§5) |
| Mon 28 Sep | Group | LO-type restructuring — bring §6's list; agree how score and tabs enter the AI Feedback LO (§1) |
| After Monday | James | Draw the V2 proposal boards: score switch (T2/T4), score on the review screen (T12) and the student's returned screen, tabs for several questions; publish as a separate row on the canvas so V1 stays readable |
| Next 2 weeks | James + Carlo's team | Open the Course & Book UX refactor stream with the brief in §3 |
| Study plan owner | TBD | Backlog: remove sequence editing from the UI; retire the book-level access dates |

**Not changed by this meeting:** the resubmission flow (demonstrated, no objection), teacher review before return, the basic-requirements check, the Kindai trial dates, the AI Grading PRD as the home of the engine contract, and the 23 Sep boards T6–T8 as the UI for dates.
