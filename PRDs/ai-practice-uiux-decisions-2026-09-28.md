# Similar Questions Practice LO — UI/UX decisions and open questions

Compiled 28 Sep 2026 from the **Riso practice questions grooming** (28 Sep; James Sim, Trieu Le Hong, John Paoletto, Cuong Hoang, Qisheng Zhang, Giang Nguyen — [Gemini notes and transcript](https://docs.google.com/document/d/16V6UqmPRWEJ4Fy5VbGSbe0ZW0S6j6XTSp1yrpqiHeZU/edit?tab=t.j30sprsjnpix)) and the PM's decisions on the clickable prototype ([S20], comment threads 24–28 Sep, recorded in `ai-feedback-university-prd.md` C11.11).

Meeting outcomes are marked **(meeting)**; prototype-comment decisions are marked **(PM, date)**. Nothing here changes the AI Practice PRD's C10 rules by itself — the open questions are the PM's to close.

---

## 1. Decided

### Loading screen (widget flow, steps 1–8) — meeting
- **Cards removed from steps 5–8.** The loading page keeps the new format (circle animation, step text, check-mark pop, highlighted Mana icon from John's HTML/MD) but does not show the OCR result cards; passing OCR data from the web view to native was too much risk for the one-week window. John updates the PRD.
- **History button removed** from the loading screen (demo scope; can be revisited for production).
- **OCR failure** reverses the flow back to the camera view.
- The web view is already loaded by step 5 (OCR), so the animation covers the web-view load and adds no extra wait.
- English versions of the four step texts are owed (John); Japanese→English readability to be checked.

### The Similar Questions Practice LO — meeting + PM
- **A new LO type modelled on AI Feedback**, created in Book Management; **linked one-to-one to a source LO** (a PDF LO). Many-to-one was raised as a possible later extension.
- Students reach it through the course (same structure as any LO) and create practice sets from the linked PDF.
- **At set creation the student chooses the count per source question**; the maximum per question is the **minimum remaining stock across the selected source questions**; the stated maximum is shown, stock totals are never shown.
- **Question selection is sequential in database order, the same for every student** (as the widget does it), not random.
- **Sets accumulate**: every additional set draws **unused** questions from the bank.
- **Continue**: a half-finished set can be resumed from the current position (backend tracks the current section).
- **Retry from scratch is allowed once a set is completed**, as a second attempt on the **same** questions; attempts are stored and shown on the dashboards. No retry mid-set — that is "continue".
- **Print / PDF is available at any point for any generated set**, finished or not **(PM, 24 Sep; confirmed in meeting)**; the sheet is questions and options only.
- **Set status "Done" means the student finished the set**, not that generation finished; the status chip is optional; History is a record, not clickable.
- **Back Office practice LO page (P3)**: Settings shows **only the linked source LO**; the "Visible to students as" section was removed **(PM, 24 Sep)**.
- **Copy rule: when something is not going to exist, do not state it** **(PM, 27 Sep)** — no "no due date", "no completion status", "not printed", hidden-field notes on any board.
- **No dates shown for a practice LO anywhere** (T8 row with empty date cells, no date on T13/P3) because the date concept is unconfirmed — see open question 5 **(PM, 27 Sep)**.

### Dashboards — meeting + PM
- **Topic Dashboard (T13)**: under the topic's feedback LO, the practice LO block shows exactly two counts — **students with sets X of N** and **students who completed all their own sets Y of N** — plus a one-line insight naming the lowest-scoring source question (nice-to-have). The ad hoc widget line and the sets / answered / correct chips were removed **(PM, 27–28 Sep)**.
- **Scores follow the existing Latest Score / Highest Score semantics** rather than a new combined metric: latest = the latest set (latest attempt), highest = the maximum across all sets and attempts; the Back Office already lets the teacher step back through earlier submissions with the arrow buttons. James updates the prototype (done: T14 toggle live, T15 highest score).
- **LO Dashboard (T14)**: the Latest / Highest Score toggle is live whenever a practice LO is in view **(PM, 28 Sep)**.
- **Student Dashboard (T15)**: Latest Score shown plainly as `6/8` (no "correct" label), Highest Score added **(PM, 28 Sep)**.
- Student-level stats sit in the existing score columns with the completion date as the "submission" date.

### Platform
- Tenant-level config for R1 vs database fallback (R4) already exists (front/back tenant configs); Cuong links the LT ticket into development.
- The prototype is for technical grooming; **Qisheng finalises the real UX/UI in Figma by end of week** (stats formats such as "5 correct" to be redesigned with proper components). Technical grooming follows the week after.

---

## 2. Open questions

| # | Question | Raised by | Owner / next step |
|---|---|---|---|
| 1 | **Retry vs new set: same or different questions?** Proposal on the table: retry a completed set = the same questions; create a new set on the same source questions = different (unused) questions. | Trieu, John | James to confirm with Nou |
| 2 | **What happens when the bank runs out** for a source question (e.g. 7 in stock, student wants a third set of 5)? Original requirement: tell the student there are no more questions; alternative raised: recycle earlier ones. | Trieu | James to confirm with Nou |
| 3 | **Sequential vs random selection.** Sequential (DB order, same for everyone) is decided for now; Trieu proposed random picks to avoid cursor tracking, Qisheng noted a changed order can help consolidation. Depends on the teacher use case of assigning specific PDF questions — must the similar questions be identical across students? | Trieu, Qisheng | James to confirm with Nou / the school |
| 4 | **Dashboard score logic across multiple sets and retries** — exactly what Latest and Highest mean once a student has several sets each with several attempts, and how the Back Office lets a teacher see the earlier ones. Prototype currently shows latest = correct/answered across sets so far, highest = best single set; to be aligned with the decided semantics above. | Trieu | James to define; Cuong to show the existing BO screen |
| 5 | **Does a practice LO have a start/due-date concept at all?** Unconfirmed; no date is shown anywhere until decided. | James (PM, 27 Sep) | AI Practice PRD |
| 6 | **Mobile PDF: native preview/print or direct download?** James is fine with direct download; Qisheng prefers letting the student choose where to save and wants native iOS/Android components instead of a custom page — Android support to be verified. | Qisheng | Qisheng to check native components |
| 7 | **One-to-one or many-to-one link** between a practice LO and source LOs — scoped 1:1; complexity of many-to-one to discuss. | James | James + Cuong |
| 8 | **Set status wording/design** — "Done" was read as "generation done"; keep the optional status chip and how to label it. | Qisheng | Figma (Qisheng) |
| 9 | **Stats presentation** ("5 correct", accuracy bars) — proper components and formats. | James | Figma (Qisheng) |
| 10 | **Insight one-liner** on the lowest-scoring question — nice-to-have; plain count or LLM-ranked insight like AI Feedback's. | James | AI Practice PRD |
| 11 | **Should a practice LO ever appear in Submission Grading?** Prototype keeps it out (nothing to review). | — | AI Practice PRD |
| 12 | **Loading screen English text** and readability of translated step labels. | Qisheng | John |

---

## 3. Next steps from the meeting
- John — update the PRD's loading-page design (no cards, new format) and supply the English loading-page text.
- Qisheng — finalise similar-questions and student-dashboard UX/UI in Figma by end of week; verify native PDF preview/print on iOS/Android.
- Cuong — link the tenant-config LT ticket into development.
- James — confirm questions 1–4 with Nou; update the prototype for the score semantics (done, V174–V176); technical grooming next week.
