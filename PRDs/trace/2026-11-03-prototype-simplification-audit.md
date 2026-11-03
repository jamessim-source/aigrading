# Simplification audit — AI Feedback prototype (gen.py, PRD v1.18 C2/C3/C6)

Scope: student PC 1–9, mobile M1–M11, teacher T1–T17, Kindai Excel X1–X5, ask-back A1–A4. AI Practice / AI Grading (P/G/Q) out of scope except where the LO boards link into them.
Evidence: README, board notes (n1–n9, MNOTES, TNOTES, XNOTES, ANOTES), builder docstrings, and screenshots of 44 boards in `audit_shots/` (served from localhost:3000, EN).

Rules the boards must still show after cutting: no basic-requirement checks · pre-submission AI feedback on by default, unlimited drafts · teacher review before return (switchable off) · optional resubmission with its own date · AI answer level 0–3 per LO · ask-back-only chat from a comment card · teacher corrections phase 1 (dismiss with reason + add missed issue) · three export shapes · teacher-only import mode · Kindai Excel trial on the AI Tutor Assignment (X boards).

---

## 1. Redundant or duplicate boards

| Pair / group | What is duplicated | Recommendation | Why (one line) |
|---|---|---|---|
| **03-Pending vs 07-Pending2** | Same `pending()` builder, `draft=2` only swaps the chip (`Awaiting feedback` → `2nd submission · Awaiting feedback`) and the received date. | **Drop 07**; show the 2nd-submission chip as a variant toggle on 03 (or mention it in n3). | No rule lives on 07; "the loop never bypasses the teacher" is already stated by 03 + 08's "2nd submission" meta line. |
| **04-Feedback vs 08-Feedback2** | Same layout; 08 adds the `Last time's ② — fixed` / `New comment` chips and drops the resubmit CTA. | **Keep both** (08 carries the resubmission-return rule). | The fixed/new chips are the only visual proof of "a returned resubmission marks what changed on the cards". |
| **M-Feedback vs M-Sheet** | One builder `m_feedback(init=0/1)`; M-Sheet is M-Feedback with sheet ② open. | **Merge** — one board, sheet opened by tapping (already works: `init` is just the initial state). | M-Sheet only exists so the canvas thumbnail shows the open sheet; the verdict strip and Ask AI link are on both. |
| **F-Chat vs MF-Chat** (and Q-Chat vs MQ-Chat) | Same `f_chat_body`, two frames. | **Keep one per device** only if the device toggle is a demo requirement; otherwise keep F-Chat, drop MF-Chat. | Same ctx card, chips, logic; the rule (ask-back only, teacher can see) is identical. |
| **T-Detail vs T-List** | T-Detail = three count cards + read-only settings; T-List = the Submission Grading table scoped to one LO; both are tabs of the same LO page (`lo_head side="course"`). | **Merge into one board**: T-List with the three counters as a header row; drop the read-only settings list (it duplicates T-Settings and T-CourseBook). | Same page, two tabs; the counters disagree today (see §3) which is what a merge would fix. |
| **T-Queue vs T-List** | Same `sg_filterbar / sg_segments / sg_table`; T-List removes LO/course/book columns. | **Keep T-Queue** (it carries the Due-date segment + Due column rule and the LO Type filter), fold T-List into the merged LO page above. | Two near-identical wide tables for one rule set. |
| **T-Book vs T-Created** | Same `book_page()`; T-Created highlights one row and shows `Unpublished`. | **Drop T-Created**; render the highlighted Unpublished row on T-Book (T-Book already shows the row as Unpublished — compare `T-Created.png`). | T5's only message ("Confirm creates it Unpublished; Publish is separate") is already on T-Material's Publish button and the tree row. |
| **T-Dialog vs T-Settings** | Same field set: T-Settings is T-Dialog read-only (`lo_dialog(edit=True)` reopens the same dialog). | **Keep T-Dialog**, drop T-Settings; mention "Settings tab = dialog read-only" in t2's note. | Answer level, pre-submission default On, teacher review, resubmission, submission methods all appear on T-Dialog. |
| **X2/X3 vs 02/04, X4/X5 vs X2/X3** | X4/X5 are declared PC twins of X2/X3 (same data, 1280 px). X2/X3 are *also* the target of the LO's pre-submission card (02, 06, M-File, M-Type → X-Feedback/X-FeedbackPC). | **Keep X1 + X2 + X3 (mobile, the trial as agreed)**, drop X4/X5 unless PC-web submission must be demoed on the AI Tutor surface; give the LO flow its own draft-feedback state instead of linking to X3 (see §2, §3). | X4/X5 carry nothing the X2/X3 notes do not; the trial is on the app. |
| **T-DashTopic vs T-DashGroup** | Same filter row, chips, Topic/LO toggle; one is Topic mode, the other LO mode of `GroupDashboard`. | **Keep both** but they could be one board with the toggle live (both already share `dash_head/dash_filter`). | Topic mode carries the per-LO counts + insight line; LO mode carries the per-student status matrix + ★ count. |
| **M-Camera → M-Crop** | Two dark boards of the unifiedapp snap flow; no AI Feedback rule on either. | **Drop M-Camera**, keep M-Crop (which already has "Add page → back to camera" and "Next"). | The page-at-a-time photographing is explained by the crop board's page counter alone. |
| **A-Idea vs A-Dialogue** | A-Dialogue repeats the locked idea in its left pane; A-Idea is the same task card + an editable textarea. | **Merge** into one board with a "lock" state toggle (locked idea → chat appears). | The lock-before-dialogue rule is the state transition itself; one board shows it better than two. |

---

## 2. Steps the student or teacher must take that the rules do not require

### Student

| Boards | Step imposed | Cut / merge | What would be lost |
|---|---|---|---|
| **M-Camera → M-Crop → M-Pages → M-Read → M-Pending** (M3–M5b, M8) | Five screens from "Snap and submit" to the waiting state. The PRD requires only: photos kept in page order, and a read-check **before asking for feedback** (C3 OCR row). Nothing requires a separate crop step or a separate pages board. | Collapse to **M-Crop (with the thumbs strip = pages) → M-Read → submit**. Put "Hold to reorder / add page" on the crop board's strip. | The light-theme pages preview with big thumbnail (unifiedapp ReviewScreen shape). Cosmetic. |
| **M-Read** placement | The read-check sits in the *submission* path (CTA "Looks right · get feedback" → M-Pending, a submission). The rule puts it before the **pre-submission AI feedback**, and says "a file upload skips this step" — but M-File (photos picked from gallery) and the PC photos path (02) also skip it although they are photographed input. | Make M-Read the step between "pick/snap photos" and **"Get feedback on this draft"**, reachable from M-Pages, M-File (photos) and 02 (photos); drop it from the submit path. | Nothing — the rule is better shown. |
| **02-Assignment, M-Type: Confirm answer → Submit** | Two taps for a typed answer (Confirm, then Submit). C3 says "the student confirms the text before submitting" — a confirmation, not a separate state with an Edit button. | Make Submit itself the confirmation (a confirm dialog or the count line "2,000 chars · what you see is what is submitted"); drop the Confirm/Edit state. | The "checks run on the confirmed text" story from 18 Sep — now moot since basic checks are removed. |
| **02 / 06 / M-File / M-Type / M-Pages: pre-submission card** | The "Get feedback on this draft" button only appears **after** a file is picked (`sc-if picked`); on M-Assignment and M-Pages there is no button at all, only the card copy. | Show the button on every submit board, disabled until there is content; and make it open an **LO draft-feedback state** (a 04-Feedback variant with a "Draft 3 · not a submission" chip and no teacher note) instead of X-Feedback(PC). | The "least dev effort" link into the AI Tutor feedback snap. That link is the Kindai Excel trial's path, not the LO's. |
| **06-Resubmit** | A whole board for "upload again". The rule: "The second submission screen is a plain upload with the previous feedback reachable from the feedback-received list." | Merge into 02 as a state: header chip `Second submission · Due Nov 20`, Submit label `Submit second draft`, and the returned Nov 13 feedback as the first row of "Feedback you have received so far". | A separate board for the second due date. The chip already carries it. |
| **05-Todo** | A To-do board placed *after* 08-Feedback2 in the row, whose only AI Feedback content is the `Awaiting resubmission · by Nov 20` and `Awaiting feedback` chips. | Keep but move between 04 and 06 (it is the state between return and resubmission), or fold the two chips into Main's LO row and drop. | Overdue-in-red and "items appear once their start date has passed" — both C3 rows, but both could be shown on Main. |
| **A-Idea → A-Dialogue → A-Revise → A-Rate** | Four screens for first idea → dialogue → revision/reflection → teacher rating. | **Two student boards** (idea+dialogue merged, see §1; A-Revise kept because the four-field storage rule needs the revision + reflection side by side) **+ A-Rate**. Alternatively A-Rate becomes a mode of T-Review (same left info panel, right-hand evidence list). | Nothing of the rules: lock, questions-only, four stored fields, criteria version, Unrated ≠ 0 all survive. |
| **F-Chat (board 9)** | Separate board for the ask-back chat. | Keep (it is the only place "ask-back only", the pinned comment context, and "teacher can see this" are shown); but it should carry the LO's **answer level** chip (0–3), not a fixed "Ask-back only" pill, since the chat follows the LO's level (C3). | — |

### Teacher

| Boards | Step imposed | Cut / merge | What would be lost |
|---|---|---|---|
| **T-Created (T5)** | A page the teacher never navigates to on purpose: Confirm lands on T-Material; T5 is reached "from the breadcrumb". | Drop (see §1). | A thumbnail showing the highlighted Unpublished row. |
| **T-Settings (T4)** | Read-only copy of T-Dialog. | Drop (see §1). | The per-course windows list ("one line per course this book is assigned to") — move that line into T-Dialog's pointer block. |
| **T-Courses → T-Course → T-CourseBook (T6–T8)** | Three boards to reach the one table that carries a rule (start / due / **resubmission date** per LO per course). T-Courses and T-Course are unchanged production pages (the notes say so: "Nothing on this board is new for AI Feedback"). | Keep **T-CourseBook** only; put Share Access / QR, the Reference-library tab and the V2 Extend-due-date dialog in its note or as overlays on T-CourseBook. If the Reference library (P2) must stay visible, keep T-Course with that tab open and drop T-Courses. | Join-by-QR (not in the C2/C3 rule set), Add course dialog, the Student tab. |
| **T-Detail (T10)** | An Overview tab with three counters and a read-only settings list the teacher already has on T-Dialog and T-CourseBook. | Merge into T-List (see §1). | The "Review (8)" CTA — put it on the Not Reviewed segment of the table. |
| **T-DashAI (T16)** beside T-DashTopic / T-DashGroup / T-DashStudent | A fourth dashboard whose AI Feedback data model is the **AI Tutor's** (feedback snaps, assignment Started/Completed, likes/dislikes), not the LO's. Its only C-rule is the **export shapes** dialog. | Move the export dialog (three shapes, data dictionary, period/filters/rubric version stamp) to **T-Queue** (an Export button beside Filters) or T-DashGroup, and drop T-DashAI from the LO story (keep it in the X trial row if the trial's logs must be shown). | The thread-viewer drawer (teacher reads a student's chat) — but the versions line on T-DashStudent plus the review screen can link to the same thread. |
| **T-DashTopic (T13) + T-DashGroup (T14) + T-DashStudent (T15)** | Three dashboards. C6.7 requires: counts per LO, ★ count, status per student, versions line with draft-check count. | Keep **T-DashGroup** (status matrix, ★) and **T-DashStudent** (versions line + draft-check count); fold T-DashTopic's counts + insight line into T-DashGroup's LO header (it already shows Submitted / Waiting / Returned + ★). | The topic-table shape and the one insight line per LO. |
| **T-Review: "Approve changes (v2)"** | A phase-2 action on a phase-1 board. | Keep the pending-changes counter; grey the button or remove it (the note can say "phase 2"). | Nothing in phase 1. |
| **T-Material: Generate rubric + Publish + Evaluation items** | Fine — one board, keep. | — | — |
| **T-Import (T17)** | Fine — the one board for the teacher-only mode. | Keep. | — |

---

## 3. Inconsistencies between boards

**Pre-submission feedback vs the X boards (the biggest one)**
- `02-Assignment`, `06-Resubmit`, `M-File`, `M-Type` → "Get feedback on this draft" / "Open" open **X-FeedbackPC / X-Feedback**: a different assignment (`Session 9 Regression`, due 11/20, crumb `AI Tutor · Assignments`), a different rubric (`Processing`, `Excel skills` instead of the LO's six chips), no verdict strip, no `Strength / Question / To-do` badges, no criterion tag, plain `Ask AI` links (no ask-back level), and a header that says **"AI Feedback · Result"** to the student although n1's rule is "no AI in any student-facing label". Its CTA "Upload a fixed version (version 2)" goes to **X-UploadPC**, not back to 02. The draft list on 02 says `3 points to work on` but X3 shows 1 teal + several numbered cards from another course.
- `X-Upload` / `X-UploadPC` copy: **"AI check required before submitting"** — contradicts the rule (pre-submission feedback is optional, unlimited, "not a submission"); and the X note on "submit the final the way your teacher asks" contradicts the LO's own Submit button one card below on 02.
- `M-Assignment` and `M-Pages` show the pre-submission card **without** the button; `02 / 06 / M-File / M-Type` show it only once a file is picked.
- `06-Resubmit`'s "Feedback you have received so far" still lists only Draft 1 / Draft 2 (Nov 9–10); the returned Nov 13 feedback — which n5 and the card footer say "will be listed here too" — is missing. Draft counter stays `Draft checks: 2` after a resubmission.

**Read-check**
- `M-Read` CTA says "get feedback" but leads to `M-Pending` (a submission). `M-File` (photos from gallery) and `02` (Choose photos of your work) skip the read-check entirely although C3 applies it to all photographed input. `M-Pages` → M-Read, but `TO_PC["M-Read"]` = 02-Assignment, which has no equivalent.

**Two Ask AI chats**
- `Q-Chat` (AI Grading, explains, chips "Show me another example") vs `F-Chat` (ask-back only, chips "Just tell me the answer"): same `chatin`, same bubbles, same "Your teacher can see this dialogue" line, same header title **"Ask AI"**, but different rule and no level chip on Q-Chat. The rule is one chat with the LO's answer level (0–3); the prototype has two products' chats with hard-coded behaviour. The link label also differs: `Ask AI (asks you back)` on 04 / M-Sheet / 08 vs `Ask AI` on X3 / X5 / Q4–Q6.
- `MF-Chat` back arrow → `M-Sheet`; `F-Chat` back arrow → `04-Feedback` (not 08 when opened from there).

**Counters that disagree for the same LO**
- `T-Detail`: Submitted **12/30**, Not Reviewed **8**, Returned **3/30**; `T-List` (same LO, next tab): All **5**, Not Reviewed **3**, In Review 1, Returned 1; `T-Review` pager: **3 / 12**; `T-DashGroup` header and `T-DashTopic` column carry their own numbers again. One LO, four sets of counts.
- `T-DashAI` counts "Feedbacks 3 / Assignment Completed" per student — a third status vocabulary (Started / Completed) next to the marking tones (Not Reviewed / In Review / Returned / Sent Back) and the student chips.

**Status chip vocabulary (student side)**
- `Main`: `Not submitted · due Nov 13` · `03`: `Awaiting feedback` · `04` header: `Returned · Nov 13` · `05-Todo`: `Awaiting resubmission · by Nov 20` and `Awaiting feedback` · `06` header: `Second submission · Due Nov 20, 23:59` · `07`: `2nd submission · Awaiting feedback` · `08`: `Returned · Nov 21`. Date formats alternate between `due Nov 13`, `by Nov 20`, `Due Nov 20, 23:59`, `· Nov 13`. The teacher's `Resubmitted` secondary chip has no student twin.
- `M-Sheet` shows the verdict (`✓ Needs work`) inside the sheet; `04` shows it only in the right-hand strip, not on the cards; `T-Review` shows it on each comment. Three placements for one verdict.

**Criteria chips vs verdict strip**
- `02` "What the comments cover" = six grey chips; `04` "Verdict per criterion" = the same six as a 2-column table; `T-Material` = numbered evaluation items + rubric list; `X3` = criteria as teal/red numbered chips (`Processing`, `Excel skills`) that are not the six. The Kindai criterion names on X3 (`Excel skills`) collide with the LO's criteria while belonging to a different rubric.

**Buttons**
- Primary submit: `Submit this work` (02) / `Submit` (M-Pages, M-Type) / `Submit second draft` (06) / `Get AI feedback` (X2, X4, primary blue) / `Get feedback on this draft` (02 card, neutral). The X boards make draft feedback the primary action; the LO boards make Submit primary. Both are right for their surface, wrong side by side.
- Resubmit: `Revise and resubmit` (04) vs `Upload a fixed version (version 2)` (X3/X5) vs the resubmission branch of Q-Resub — three names for "next version".

**Teacher side**
- `T-Dialog` has the AI answer level and the pre-submission default; `T-Detail`'s settings list omits both (Window / Resubmission / Submission / Teacher review only).
- `T-Review` breadcrumb `Course / Submission Grading / Session 7 exercise report`; `A-Rate` sits under the same breadcrumb but with a different layout (levels 1–3 + Unrated per criterion) while the LO's rule is verdict-only, no level — fine for ask-back mode, but nothing on A-Rate says it is the ask-back mode of the same LO type.
- Device pill: `T-Settings` / `T-Dialog` jump to `Main`; `X-Assign` jumps to `X-Upload`; the 02 card jumps to X3 — the student twin of a Back Office setting is sometimes the LO and sometimes the AI Tutor assignment.
- Mobile has **no** resubmission boards: `TO_MOBILE["06-Resubmit"]` = M-Assignment, `["07"]` = M-Pending, `["08"]` = M-Feedback (no fixed/new chips on mobile).

---

## 4. Recommended simplified flow

### Student (PC) — keep 5 (from 9)
- **Keep:** `Main` (LO row + due chip; absorb To-do's chips) · `02-Assignment` (one submit board with three modes; pre-submission card with the button always visible; second-submission chip as a state) · `03-Pending` (teacher-review wait; `2nd submission` chip as a variant) · `04-Feedback` (verdict strip, ★ line, Ask AI link; add a **draft-feedback variant** with a `Draft 3 · not a submission` chip and no teacher note — this replaces the link into X3) · `08-Feedback2` (fixed/new chips) · `F-Chat` (ask-back only, with the LO's answer-level chip).
- **Merge:** `06-Resubmit` → into 02 (state); `05-Todo` → into Main (chips) or keep as the one non-LO board.
- **Drop:** `07-Pending2`.

### Student (mobile) — keep 6 (from 11)
- **Keep:** `M-Main` · `M-Assignment` · `M-Crop` (with the pages strip) · `M-Read` (moved before "Get feedback on this draft"; reachable from file-photos too) · `M-Pending` · `M-Feedback` (sheet opens on tap; drop M-Sheet) · `MF-Chat` only if the device toggle must work.
- **Merge:** `M-File` + `M-Type` → states of M-Assignment (mode cards expand in place).
- **Drop:** `M-Camera`, `M-Pages`, `M-Sheet`.

### Teacher — keep 8 (from 17)
- **Keep:** `T-Book` (with the Unpublished highlighted row) · `T-Dialog` (answer level 0–3, pre-submission On by default, teacher review toggle, resubmission toggle, submission methods) · `T-Material` (evaluation items → rubric, no requirements paper, Publish) · `T-CourseBook` (start / due / **resubmission** dates per course) · `T-Queue` (Due segment + Due column, LO-type filter, **+ the three-shape Export dialog moved here**) · `T-Review` (verdict per comment, Dismiss with reason, Add a missed issue, pending-changes counter; grey out "Approve changes (v2)") · `T-DashGroup` (status matrix + ★; absorb the Topic-mode counts/insight line) · `T-DashStudent` (versions line with draft-check count) · `T-Import` (teacher-only mode).
- **Merge:** `T-Detail` + `T-List` → one LO submissions board (counters above the table) — or drop both since T-Queue already is the table; `T-DashTopic` → into T-DashGroup; `T-Courses` + `T-Course` → into T-CourseBook's note (or keep T-Course alone for the Reference-library tab).
- **Drop:** `T-Created`, `T-Settings`, `T-DashAI` (its export dialog moves to T-Queue; the thread viewer is linked from T-DashStudent's versions line).

### Kindai Excel trial — keep 3 (from 5)
- **Keep:** `X-Assign` (AI Tutor Assignment, .xlsx/.pptx, Generate by AI) · `X-Upload` · `X-Feedback`. Fix the copy "AI check required before submitting".
- **Drop:** `X-UploadPC`, `X-FeedbackPC` (twins), and **remove every link from the LO boards (02/06/M-File/M-Type) into X3** — the LO's draft feedback is the 04 variant above.

### Ask-back — keep 3 (from 4)
- **Merge:** `A-Idea` + `A-Dialogue` → one board (lock → chat appears). **Keep** `A-Revise`, `A-Rate` (or A-Rate as a mode of T-Review).

### Net
Current 46 in-scope boards (9 + 11 + 17 + 5 + 4) → **25** (6 + 6 + 9 + 3 + 3 with F-Chat/MF-Chat counted once each), every C2/C3/C6 rule still visible, and the one structural error fixed: the LO's pre-submission feedback no longer demos as the AI Tutor's Excel result.
