# AI Feedback LO — prioritized changes to the prototype and PRD (3 Nov 2026)

## Context

James asked for the five client documents to be read as data points for scoping **general** requirements, and for a prioritized list of changes to the LO prototype (`prototypes/ai-feedback-student/gen.py`, 163 generated pages) and the PRD (`PRDs/ai-feedback-university-prd.md`, now v1.16).

All five were read in full:

| # | Source | Client / segment | What it is |
|---|---|---|---|
| S31 | DLSC teacher-only trial spec, draft v1, 24 Oct (already in PRD 1.9 / C11.16) | Kindai Correspondence (Civil Law, Prof. Fukuda) | Teacher-only, KULeD-centred: bulk import, review queue, per-question findings, comment draft, corrections → criteria versions, textbook quote check, KPI log |
| S33 | Okayama Gen-AI Project — Product Team Brief (Claude Doc, rev 17) | Okayama Prefecture via Z会, two high schools, 1,284 users, live Jan 2027 | Socratic ask-back dialogue: first idea locked → questions → revised explanation → reflection; teacher rating against versioned criteria; roles, SSO, exports, Japan-resident data; prompt/model version logged per dialogue |
| S34 | Ask-Back AI for Universities memo, 30 Oct | University GTM (Meijo, Chuo, Showa Women's, Kindai Correspondence, Juntendo…) | Answer dial 0–3 per assignment; LTI 1.3, GakuNin SSO, Word submission, assignment templates; process-record view, TA role, class summary; pilot KPIs |
| S28 (updated) | Kindai Applied Sociology requirements doc, now with the 10/22 client meeting | Kindai Sociology stats course, 150 students, 11/6 → 1/31 | Trial dates fixed (mid survey 11/13, report 11/20, logs 12/17, final survey ~1/28, final report 2/18); PC submission and PPTX "in development"; QR class join; **thesis trial with ~3 teachers in Dec (format/structure feedback on finished theses)**; Excel written questions: advise only when asked how to think; flexible contract form |
| S35 | AI Feedback demo tenant requirements (Kyushu Sangyo), 20 Oct | Kyushu Sangyo, Practical Japanese (writing), handwritten 400-character essays | Teacher types the evaluation items (a 12-item checklist); AI must generate a rubric that keeps the items 1:1 (no merging/dropping); feedback uses that rubric as-is; per-item ✓/― + comment + overall; handwritten OCR errors must not be flagged as typos; resubmit and BO view nice-to-have |

Pattern across the five: every client wants (1) its own criteria kept verbatim and applied per item, (2) a per-item verdict plus one overall comment, (3) control over how much the AI gives away, (4) the teacher seeing versions, chat and feedback without the student "completing", (5) exports with IDs, and (6) three of five want teacher corrections to change the criteria going forward. These are the general requirements; the rest is per-client.

Priority key: **P0** = blocks a decision or the running Kindai trial; **P1** = general requirement hit by ≥2 clients, belongs in the LO version (v2.5 Dec / unified Assignments Q1 2027); **P2** = one client or later; **P3** = platform, no prototype work.

## A. PRD changes (file: `PRDs/ai-feedback-university-prd.md`)

| Pri | Change | Where | Source(s) |
|---|---|---|---|
| **P0** | **Rule which PRD owns teacher-only / ask-back modes.** C11.16 already asks who owns the DLSC track; S33 and S34 add a second teacher-rated, student-dialogue product on the same engine. Decide: AI Feedback PRD owns the *LO surface and the engine's modes* (feedback, ask-back, teacher-only import); AI Grading owns scoring. Record in A2 and E1; close C11.16's opening question | A2, E1, C11.16 | S31, S33, S34 |
| **P0** | **Fold in the 10/22 Kindai meeting** as Background 1.8 additions: dates, thesis trial (3 teachers, Dec), PC submission + PPTX "in development" as said to the client, QR class join, written-question advisory rule, flexible contract; U26 updated (full implementation decision path: 2/5 pre-brief → 2/10 主任会議 → 教授会 2/17–2/20) | 1.8, 1.7 (U26), E2 | S28 |
| **P0** | **Add S33–S35 to Background** (1.11 Okayama, 1.12 university ask-back memo, 1.13 Kyushu Sangyo demo) with provenance, plus source-index rows S33–S35 | 1.x, Appendix | S33, S34, S35 |
| **P1** | **C3 new rule: criteria fidelity.** Teacher-entered evaluation items are stored as a structured list; Generate by AI writes one rubric criterion per item in the teacher's order and numbering, never merges or drops; regeneration with more files replaces, not ignores (the 3a bug). Feedback uses the LO's rubric as-is; the learner side never regenerates | C3, C11.3 | S35 #1–3, Slack 3a, S31 F6, S33 criteria config |
| **P1** | **C3 new rule: feedback shape.** Per criterion: verdict (flag / no issue — Kyushu's ✓/―, DLSC's severity, Kindai's teal/red), quoted passage, comment; one overall comment (praise → biggest issue → next step). No score unless the scoring product asks for it. Define the verdict vocabulary once (Env-level) | C3, C5 | S35 #6, S31 F3, S28 Q2 |
| **P1** | **C3 new rule: answer level per LO** (0 ask-back only · 1 hints and where to look · 2 pattern on another topic · 3 full explanation), default 1; tenant can cap. Kindai's "advise only when asked how to think" = level 1; Okayama = 0–1; the Gem "never the finished work" = ≤2. Applies to the feedback cards *and* the Ask AI chat (chat inherits the LO's instruction) | C3, A2 (Tenant-level) | S34 dial, S33, S28 10/22, S28 Q3 |
| **P1** | **C3 new rule: OCR uncertainty is never the student's error.** Handwritten or photo input: low-confidence reads are shown as unconfirmed in Extracted text and excluded from typo/格式 findings; the student may correct the read before feedback (Okayama's confirm step). Add to the error-path row C3 still lacks | C3 (error paths) | S35 #5, S33 image input, S31 F3 |
| **P1** | **C2: move "instructor corrections → criteria version → re-run" from KIV to phased-in.** Three clients now ask for it (DLSC F5/F6, Okayama versioned criteria, S34). Phase 1 = dismiss reason + "add missed issue" captured and shown to the teacher; phase 2 = criteria version + re-run. Keep "no retro-tag of past comments" | C2, C3 (rubric-edited row), C11.9 Q3 | S31, S33, S34 |
| **P1** | **C2: graduation theses are no longer excluded outright.** Kindai asks for Dec feedback on *format and structure* of finished theses with ~3 teachers. Scope it as "structure/format feedback against a department template", not content; record as a Want with owner | C2, 1.8, U-row | S28 10/22 §7 |
| **P1** | **A1 tracking metrics = the KPI log every client asked for:** pre-check done, versions per student, chat turns, criterion flag counts per version, teacher accept/dismiss/edit, copy-as-is vs edited (where a draft is pasted elsewhere), review time, usage rate per class. Define the events once; exports read from them | A1, C7 | S28 2-2, S31 F8, S33 usage, S34 KPIs |
| **P1** | **C7 export spec: one module, three shapes** — chat/feedback CSV (done, `PRDs/samples`), per-criterion results CSV, usage CSV; every export stamped with period, filters, criteria version; a data dictionary file; IDs = tenant user ID, names optional (DLSC drops them) | C7, C11.13 D6 | S28 D, S31 F9, S33 exports, S34 research export |
| **P1** | **C9 / C2: student submission on PC web is a Must for universities** (Kindai 10/22 "in development", Okayama browser-only, DLSC/S34 Word). State the surface (learner web) and formats incl. Word; PPTX as-is stays Want | C2, C9.1 | S28, S33, S34 |
| **P2** | **Reference library at course level** (textbook / lecture PDFs, procedure manual) feeding grounding (Kindai Q4/T2), deterministic quote checking (DLSC F7), "point back to materials" (Okayama). One entity, two uses; rights to load texts = open item | C2, C7, C11.15 T11 | S28, S31, S33 |
| **P2** | **Tone and guardrail presets per tenant**: friendly-TA / concise-no-AI-mention / plain-text-for-external-LMS; "sounds like AI" check (Kindai Q7); no mention of AI to students where the client requires it (DLSC, Kindai) — reconcile with A3's responsibility rule | C3, A3 | S28 Q1–Q7, S31 F4, S33 |
| **P2** | **Teacher-only import mode** (DLSC F1/F2): bulk ZIP/CSV of submissions keyed by an external ID, batch queue by due date, "done elsewhere" status. Record as a mode of the LO (students absent), effort from C11.12's CSV import | C2, C11.16 K1–K2 | S31 |
| **P2** | **Ask-back dialogue mode** (Okayama): first idea locked → dialogue → revised explanation → reflection, stored as separate fields under one task ID; prompt and model version logged per dialogue; teacher rating with criteria version, "unrated ≠ zero". Record as a mode; decide build-on-LMS vs separate after the bid | C2, C11.16 (new K-rows) | S33 |
| **P2** | **C8: cost/latency gates** — thinking level low on both agents (done), $0.35/student hosting target (S32), "use without limits" clause (S33) → state caps and their lesson effect; model retirement 19 Nov | C8, C11.15 T12/T16 | S33, S32 |
| **P3** | **Platform notes**: LTI 1.3, GakuNin/Google/Microsoft SSO with roster check, board-of-education tenant hierarchy and roles, Japan residency / no-training terms, contract-end deletion. No prototype; list under E/C7 as dependencies with owners | C7, E2 | S33, S34 |

## B. Prototype changes (file: `prototypes/ai-feedback-student/gen.py`; publish to artifact FYtGUxxHgPhzWnENGtgLmE; push branch + main for Railway)

| Pri | Board(s) | Change | Reuse | Source(s) |
|---|---|---|---|---|
| **P1** | `T-Dialog` (BO, create AI Feedback LO) | Add **Evaluation items** as a structured list (numbered rows, add/remove, ★ key item) above the rubric block; "Generate by AI" produces one rubric criterion per item in order; helper text "items are kept 1:1". Keep the free rubric block as the generated output | `field()`, `tchip`, rubric block in `t_dialog`; X1's attachments list | S35 #1–2, S31 F6, S33 |
| **P1** | `T-Settings` (BO, LO settings) | Add **AI answer level** segmented control 0–3 with one-line definitions, default 1; add **Verdict style** (flag/ok · strength/improve) read-only hint; keep teacher review, resubmission, pre-check toggles | `st_chip`, settings rows in `t_settings` | S34, S33, S28 |
| **P1** | `04-Feedback`, `M-Feedback`, `T-Review` | Feedback cards get a **per-criterion verdict column** (✓ flag / ― ok) in the criterion chip, one **overall comment** card on top in praise → issue → next step order; the review screen shows the same verdicts the teacher can flip. Markers stay | `.ad-fcard`/`.xcard` chip pattern, `ov_card` | S35 #6, S31 F3, S28 Q2 |
| **P1** | `M-Pages` → new `M-Read` (mobile) and `02-Assignment` (PC) | **Read-check step** for photos/handwriting: Extracted text with low-confidence spans dashed and marked "unconfirmed"; tap to correct; "Looks right → Get feedback". Dev note: unconfirmed spans are excluded from typo findings | X3's Extracted text tab, `.xul` markers | S35 #5, S33 image input |
| **P1** | `T-DashStudent` (BO) | Per student × LO: **versions timeline** (v1…vN with time, criterion flags per version, chat turns), pre-check done chip without "complete", open thread drawer (reuse T16's `ad_viewer`) | `ad_viewer`, `ad_fb` data, T16 expanded row | S28 2-2 A, S31 F2/F3, S33 history detail |
| **P1** | `T-Queue` (BO) | Add **batch / due-date view**: group by LO due date, "Due this week" filter, per-row criterion-flag count and status chips incl. "Returned elsewhere" (for the KULeD case) | existing filters block in `t_queue` | S31 F2, S28 |
| **P1** | `T-DashAI` export dialog → `T-DashGroup`/`T-DashStudent` | Export menu with **three shapes** (chat + feedback · per-criterion results · usage), period + criteria-version stamp line, "data dictionary included" note; keep the fixed-columns pattern | `ad_export` dialog | S28 D, S31 F9, S33, S34 |
| **P2** | `T-Review` | **Correct the AI**: dismiss with reason (not an issue · too strict · wrong criterion · wrong location), "add a missed issue" (select text → criterion → note); a "pending criteria change" chip on the LO; rubric shows **version n** | review comment list, `tchip` | S31 F5, S33, S34 |
| **P2** | `T-Course` → new `T-Library` (BO) | **Course reference library** tab: lecture PDFs / textbook / procedure manual with "used for grounding" and "quote check" toggles; LO dialog picks from it | T-Material pattern | S28 T2/Q4, S31 F7, S33 |
| **P2** | `02-Assignment` (PC) | Make the PC submission board carry **Excel / Word / PPTX / photos** choices with the same "sheets read" list as X2, so the PC web path is visible | X2's `x_upload` list, `_xfile` | S28 10/22, S33, S34 |
| **P2** | new `A-Idea` → `A-Dialogue` → `A-Revise` (mobile + PC) | **Ask-back mode** boards for Okayama/university memo: first idea locked, AI questions, revised explanation + reflection, teacher rating panel with criteria version. Only if the bid proceeds; draw after the PRD mode is accepted | `Q-Chat` chat UI, `04-Feedback` layout | S33, S34 |
| **P2** | new `T-Import` (BO) | **Teacher-only bulk import** of submissions (ZIP/CSV keyed by external ID, named batch, auto-run, unreadable list) — reuse `G-Import` from AI Grading rather than a new design | `G-Import` | S31 F1 |
| **P3** | — | SSO/LTI/roles: no boards; a note on the index page only | — | S33, S34 |

Not proposed: a separate thesis board (scope first), voice input/output (Okayama-only), KULeD comment draft screen (DLSC-only; a plain-text "copy comment" action on `T-Review` covers it if K4 is accepted).

## C. Order of execution

1. PRD P0 rows (ownership ruling text as a decision proposal for James; Background 1.8 update; 1.11–1.13 + S33–S35).
2. PRD P1 rules in C3/C2/A1/C7/C9 — each written as a rule with Env/Tenant label, not as client quotes.
3. Prototype P1 boards in the listed order (T-Dialog items → T-Settings level → feedback verdicts → read-check → DashStudent versions → Queue batch view → export shapes), one commit each, screenshots via the existing Playwright scripts in the scratchpad, republish the artifact per board, push branch + main.
4. PRD P2/P3 rows and prototype P2 boards after James confirms the mode decisions (teacher-only, ask-back).

## Verification

- `python3 gen.py` writes 163+ pages with no exception; headless Chromium screenshots of each changed board (JA + EN) show the new elements; `pageerror` list empty.
- Railway: changed pages present on `main` under `prototypes/ai-feedback-student/deploy/public`.
- PRD: change-log row v1.17; every new Background line carries source + date; no meeting text lands in Parts A–C except as a rule James has decided; readiness-gate section D re-checked for the new C3 rows.
