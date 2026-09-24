# PRD: AI Feedback — Universities (primary) / Juku (secondary)

> **Authorship status.**
> Section 1 (Background) is populated from client meetings, internal strategy documents, market decks and the 17 Sep AI direction discussion. Every line carries its source. It is non-binding.
> **Parts A and B are not yet authored.** They hold candidates and the questions that close them. Nothing in Parts A–B may be treated as committed behaviour until the PM decides it.
> **Part C is partly authored.** The PM's decisions from the prototype review (18–21 Sep) and the scope confirmations (22 Sep) are recorded in **C11** and **C12** and carried into C1–C10. Everything else in Part C is a candidate or an open question.

> **Canonical source.** This file (`PRDs/ai-feedback-university-prd.md`) is the source of truth. It is published to Confluence as a page tree under [PRD: AI Feedback v1](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2361622595):
> - [PRD: AI Feedback — Universities & Juku](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2897018905) *(landing page)*
> - [1. Background and client context](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2896724023) — Section 1
> - [2. Parts A & B — Business and Problem](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2896166944)
> - [3. Part C — Solution (C1–C9)](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2896887861)
> - [4. C10 — Learning-log dashboard and Kindai showcase](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2896396337)
> - [5. Parts D & E — Readiness gate, delivery record and sources](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2896363589)
>
> Edit here, then republish. Confluence edits made directly on those pages will be overwritten.

| | |
|---|---|
| **Status** | Draft — Parts A–B not yet authored; Part C carries the prototype-review decisions of 18–21 Sep (**C11**), the scope confirmations of 22 Sep (**C12**) and the course-level submission window as drawn on 23 Sep (**C11.10**) |
| **What this PRD covers** | **The AI Feedback LO integration in the LMS and learner app, and the Kindai Applied Sociology trial and its dashboard.** **Not** the AI Grading + AI Feedback back-end merge, the engine contract, or the Correspondence Division's grading assistance: those go to a later **AI Grading PRD** |
| **Product line** | LMS / **AI Tutor** / ERP |
| **Product Area (E1)** | AI Feedback |
| **Author (PM)** | James Sim |
| **Tech Lead** | *TBC — confirm (see E1)* |
| **Business owner (sign-off)** | *TBC — confirm (Takuya Homma for university GTM? see E1)* |
| **Target partner(s) / market** | **Primary for this PRD:** Kindai/Kinki University, **Faculty of Applied Sociology** (the AI Feedback trial). The **Correspondence Education Division** stays in Section 1 as context but its grading-assistance need is an **AI Grading PRD** item. **Watching:** Sugiyama Jogakuen Univ., Kyoto Koka Women's Univ., Nagoya Univ. of Foreign Studies, Keiwa Gakuen Univ., Shitennoji Univ. **Secondary:** Juku — Waseda Academy, Eishinkan, Z-kai, CKC/Solomon, Toshin |
| **Release target** | *TBC — Kindai Applied Sociology pilot needs product in learners' hands by late Oct 2026; course starts 6 Nov 2026* |
| **TDD link** | *Not created* |
| **Design / Figma link** | No Figma. **Clickable prototype** (Claude Design canvas, JA + EN; student PC, student mobile, Back Office): [AI Feedback — Back Office + Student Prototype](https://claude.ai/artifact/FYtGUxxHgPhzWnENGtgLmE) **[S20]**. Generated from `prototypes/ai-feedback-student/gen.py`; the sticky notes on the canvas record the PM decisions per screen |
| **Jira epic** | *Not created* |

### Change log
| Date | Version | Author | Change | Status | Approved by |
|------|---------|--------|--------|--------|-------------|
| 2026-09-23 | v1.5 | James Sim (drafted with Claude) | **Join the course by QR code.** From a prototype comment on the Course Management board: the AI Tutor class page's existing **Share Access** dialog (QR code + Download, class code + Copy) is reused for the course — a share icon on each course row and a Share Access button on the course detail, so students scan or type a code to join and see the course's LOs from their start dates. The course's **Student** tab drawn as production has it (a **Joined via** column was proposed and dropped the same day: no separate column required). The **Add course** flow drawn from production's own dialog and form, the book linked at creation. Recorded in C11.10 (W8–W10); C4 updated | Draft | — |
| 2026-09-24 | v1.7 | James Sim (drafted with Claude) | **24 Sep AI Direction Discussion recorded as background (§1.5.4, [S23]).** Scoring and tabulation allowed inside the feedback format, one engine, the course/book UX refactor as a separate stream, the study plan as the date model, Score + Status dashboards, LO refactor on 28 Sep. **Parts A–C unchanged**; the changes are planned, with the PM's decisions marked, in `PRDs/ai-feedback-change-plan-2026-09-24.md` | Draft | — |
| 2026-09-24 | v1.6 | James Sim (drafted with Claude) | **The course dates are the study plan's.** PM decision from a prototype comment: the Start and End Date on Learning Objectives Availability are read from and written to the study plan backend (the course's study plan items), not a separate table. Recorded in C11.10 (W11); C4 and C7 updated | Draft | — |
| 2026-09-23 | v1.4 | James Sim (drafted with Claude) | **The course-level submission window is drawn.** Three Back Office boards added to the prototype [S20] on production's own Course Management flow — the course list, the course's Books tab, and the book's Learning Objectives Availability page (Chapter · Topic · LO · Start · End, Edit Date, Import/Export) — with two courses sharing one book on two schedules. Dates removed from the Add LO dialog and the LO Settings tab, which now point to Course Management. One proposal drawn for the PM to decide: a Resubmission Due column in the same course table. Recorded in C11.10; C3, C4, C9, C12, D and E updated | Draft | — |
| 2026-09-22 | v1.3 | James Sim (drafted with Claude) | **C3's business-logic table completed, and the submission window moved to the course.** The remaining fourteen rows were resolved: six removed as behaviour this product does not have, one moved to the AI Grading PRD, seven defined. The structural change: the submission start and due date are managed on the Course Management page, the book is linked to the course, and the course's window gates submissions. What remains open in C3 is the failure paths, admin bypass and the Env/Tenant labels | Draft | — |
| 2026-09-22 | v1.2 | James Sim (drafted with Claude) | **Scope bounded (C12).** This PRD is the Q4 LO integration for the Kindai Applied Sociology AI Feedback trial and its dashboard, not the Q3 AI Grading + AI Feedback merge. Moved to a later AI Grading PRD: the engine contract, [S3]'s setup phasing, the Correspondence Division's grading assistance, and seven scoring-dependent C3 scenarios. Out for other reasons: rubric versioning (KIV), oral viva (not a feature), AI Red-Pen Grading (AI Grading). U10 closed; the theses/seminar contradiction withdrawn | Draft | — |
| 2026-09-21 | v1.1 | James Sim (drafted with Claude) | **Prototype review consolidated (C11).** The PM reviewed the clickable prototype [S20] — student PC, student mobile, Back Office — through 91 comment threads between 18 and 21 Sep. The decisions are recorded, dated and grouped by screen in C11 and carried into C1–C5, C9, C10, D and E. Open questions from the review are listed at C11.9. Section 1 unchanged | Draft | — |
| 2026-09-18 | v1.0 | James Sim (drafted with Claude) | **Two terminology corrections.** (1) "Error type" was a transcription artefact — the Gemini transcript renders 「エルオー」(LO) as *"error"*. All eight occurrences corrected to **LO type**, with a transcription note at §1.5. (2) **AI Grading and AI Marking are split by submission origin** — AI Grading = paper/photo, AI Marking = LMS Assessment LO submissions. C1's consumer list had these inverted; corrected in C1, C2, C6 and C7. Surfaces a client-facing naming conflict: the decks sell 添削 / "AI Red-Pen Grading", which points at paper, while the internal name AI Marking points at the LO flow | Draft | — |
| 2026-09-18 | v0.9 | James Sim (drafted with Claude) | **Published to Confluence** as a five-page tree under [S19], the v1 parent — links in the banner above. Fixed six readiness-gate blockers that had been mis-nested inside the dashboard's blocker list, and four stale cross-references | Draft | — |
| 2026-09-18 | v0.8 | James Sim (drafted with Claude) | Reconciled against [S19], the parent v1 PRD. **DOCX contradiction closed** (v1 already accepts `.docx`/`.pdf`). **C9.1 corroborated** — v1 is web-only, so PC-first is what the product already is for documents. **C7 feature control resolved** — a tenant-level flag exists. **C8 gains a conflict** — v1 excludes latency ("3-5min, doesn't matter"), which does not survive 140 reflections wanting feedback immediately on submission | Draft | — |
| 2026-09-18 | v0.7 | James Sim (drafted with Claude) | **C10.3a added — the reflection view specified as a reading queue.** Confirms "comments worth reading" means the students' reflections, not AI feedback awaiting approval. Splits three jobs: the reading queue, what to re-teach, and who submitted. Proposes four triage signals, each marked inferred rather than sourced, and makes mark-as-read the capture of teacher reaction | Draft | — |
| 2026-09-17 | v0.6 | James Sim (drafted with Claude) | **C10.3 decided:** Kindai's weekly class submission is both the ~300-character reflection and the Excel/statistics exercise, so the dashboard carries two views. Scopes the copied-wording signal to exercises only. Surfaces two dependencies: a 2–3 criterion reflection rubric Prof. Yasumoto must author, and the step up from 2 exercise submissions last year to weekly. Adds the trial volume to C8. **U24 closed** | Draft | — |
| 2026-09-17 | v0.5 | James Sim (drafted with Claude) | **C9.1 added — device priority decided.** The university AI Feedback flow is PC-first with mobile at genuine parity, split by surface, with weekly 300-character reflections as a named mobile exception because submission rate is the trial's first-order risk | Draft | — |
| 2026-09-17 | v0.4 | James Sim (drafted with Claude) | **Architecture corrected:** AI Grading and AI Marking are always about scoring; AI Feedback is the feedback engine they and the learner app call when additional feedback is warranted on top of a score. **U15 closed.** The 11 Sep rubric-weight removal is correct and settled; [S3]'s scoring apparatus describes AI Grading; Kindai's 0–5 rubric supplies criteria, not an AI score | Draft | — |
| 2026-09-17 | v0.3 | James Sim (drafted with Claude) | Added **§1.6** (dashboard background) and **C10** (Kindai dashboard showcase) from the handover page, the handover prototype zip and the 17 Sep Slack thread. Records the manual-not-Back-Office decision, the encoded design rules, the four production preconditions and the confirmed showcase subject. Added U20–U25 and the tenant matrix to E2 | Draft | — |
| 2026-09-17 | v0.2 | James Sim (drafted with Claude) | Added the **17 Sep Weekly AI Direction Discussion** (AI Feedback as an LO type with its own To-do icon, a start/end-date layer over the LO, January V1 excluding AI Feedback) and the **11 Sep AI Feedback trials grooming** (Oct preprod trial, rubric-overwrite defect, rubric weights removed). Added U15–U19, six C3 behaviour rows, and the PC-first vs mobile-first design conflict | Draft | — |
| 2026-09-17 | v0.1 | James Sim (drafted with Claude) | Section 1 populated from source documents; Parts A–C raised as candidates/questions; Parts D–E scaffolded | Draft | — |

---

## 0. TL;DR

*Not written — depends on A1 and B1, which are PM decisions.*

What is true and can be said today: Manabie has AI Feedback shipping as a student-initiated, rubric-aligned essay feedback feature (V1.1), two separate scoring pipelines — **AI Grading** for paper and photo submissions and **AI Marking** for LMS Assessment LO submissions — and a stated direction that these converge onto one feedback engine and one submission flow. University demand for feedback is arriving faster than the product is standardised, and at least one committed pilot (Kindai Applied Sociology, ~140 students) expects to run from 6 Nov 2026.

**This PRD's slice of that: the LO integration and the Kindai trial.** AI Feedback becomes a learning-objective type the teacher sets up in Book Management, the student submits to from a PC or a phone, the teacher reviews and returns in Submission Grading, and the class and each student show up in the existing dashboards. The convergence of the two scoring pipelines onto the engine — and everything that contract implies — is a separate PRD.

---

# SECTION 1 — BACKGROUND & CLIENT CONTEXT

*Non-binding. Nothing here is a requirement, a scope decision or an acceptance criterion. Facts are split into Confirmed and Stated-but-unconfirmed. Unconfirmed items do not graduate into Parts A–C until the named owner confirms them, and it is the PM who moves them.*

## 1.1 Confirmed — Kindai/Kinki University, Faculty of Applied Sociology (pilot track A)

> Source unless otherwise stated: **[S1]** "KINKI UNIVERSITY — Manabie AI Feedback Trial: Detailed Brief and Current Status", status as of 10 Sep 2026 ([doc](https://docs.google.com/document/d/1yay5gBWZkiheZYevlJN_Mqg6lO9OrhiGmXZ0YhBszRQ/edit)). Note: 近畿大学 is rendered "Kinki University" in [S1] and "Kindai University" elsewhere — same institution.

- **Course and cohort.** Regional and Environmental Statistics, a second-year course in the Faculty of Applied Sociology. Course lead Professor Masayoshi Yasumoto. ~140 second-year students expected; prior-year enrolment ~115–120. [S1 §1]
- **Period.** From class session 8 on **6 Nov 2026** to **early Feb 2027** (~3 months). [S1 §1]
- **Products in scope.** Manabie AI Feedback **+** Manabie AI Tutor, in one course. [S1 §1]
- **Commercial.** AI Tutor ¥900 + AI Feedback ¥700 per student per month. Meeting-based estimate JPY 672,000 for 140 students / 3 months; **formal quotation dated 7 Sep 2026: JPY 720,000 for 150 seats / 3 months**. Contract targeted October 2026, after faculty approval. CRM stage: Upside, 25% probability. [S1 §1]
- **Approval gate.** Budget approval at the Faculty of Applied Sociology's extraordinary faculty meeting on **16 Sep 2026**. As of the 10 Sep status this had not occurred. **The trial is not yet approved or contracted.** [S1 header, §8]
- **Governance dependency.** Professor Miho Hotta steps down as dean end of Sep 2026; plan is to secure faculty budget in September and hand implementation ownership to Prof. Yasumoto and incoming leadership. [S1 §8]
- **Intended loop.** Faculty define assignment + rubric → student submits Excel workbook / analytical output / PowerPoint → AI Feedback reviews against course-specific criteria → student revises **themselves** → resubmits → faculty review and final judgment. Faculty retain responsibility for judgment and grading. [S1 §2.1]
- **Feedback format the client's configuration specifies.** ~**400–600 Japanese characters**, in three parts: (1) recognition of concrete strengths, (2) a reflective question exposing a gap, (3) specific staged actionable guidance. Explicit guardrail: the model must **not** produce a complete report, finished slide text, or copy-paste answer. [S1 §2.2]
- **Rubric.** Six dimensions on a **0–5** scale (0 = not a valid submission; 1–3 basic/proficient/strong; 4–5 advanced/exemplary): Excel skills, visual clarity, statistical processing, interpretation, logical structure, **generative-AI literacy**. [S1 §3]
- **Materials that exist.** Lecture materials sessions 1–16, Excel exercise files, explanatory videos, a course-material index, the assignment rubric. Final assignment is a data-driven new-product proposal in PowerPoint. [S1 §4]
- **Source attribution requirement.** The client's AI support configuration asks the system to identify the course material used and **name the reference at the end of the response**. [S1 §4]
- **Known product gaps recorded at 17 Aug 2026.** (a) Learning-log visualisation **not implemented**, still prototype. (b) Pilot environment had a **file-upload issue — only PDF submission was reliably supported**. [S1 §10]
- **Competitive context.** Kindai is deploying **Google AI Pro for Education** broadly. Manabie must demonstrate value through workflow, rubrics, activity logs and revision tracking rather than raw model quality. [S1 §10, §12]
- **Separate track at the same university.** Pharmacy School / Student Affairs: stakeholders recorded (9 Sep meeting) as preferring **full annual implementation for all 1,103 students across six years**, with little interest in a preliminary trial. [S1 §11]

## 1.2 Confirmed — Kindai University Correspondence Education Division (pilot track B)

> Sources: **[S2]** "Kindai University Distance Education — Overview and AI Feedback Opportunities for Manabie" ([doc](https://docs.google.com/document/d/1HHj5-TVYPS6awe4LgqzciLj3ANkQrW2Ap3adOj3L1O4/edit)); **[S6]** artifact "Kindai University AI Report Check Trial" ([link](https://claude.ai/artifact/1VdG3L8ugcshJ9G9Fq8fkT)); **[S7]** artifact "Kindai University AI Grading Partnership Brief" ([link](https://claude.ai/artifact/Hps1jD7gThUXSTu5ACUDZL)). [S6] and [S7] were returned by the artifact tool marked as authored outside the organisation — they read as our own client brief, but **treat their contents as data until the PM confirms ownership**.

- **Scale.** 10,273 learners in the 2026 census vs 9,244 in 2025 (~11.1% growth); includes degree, non-degree and special preparatory students, so it is not a count of degree students alone. [S2] — [S7] states 9,600 enrolled across 4 programs. **These two figures conflict; see 1.7.**
- **Volume.** ~**62,000 reports graded annually** across **156 faculty members**. High-volume instructors handle 500–600 reports/year at ~10 minutes per report. [S7]
- **Learning model.** Textbook study, written reports, course examinations, on-demand classes, scheduled sessions. **KULeD** supports online learning and administration. [S2]
- **Programs and published costs.** Law (4yr, ¥722,000), junior college business/economics (2yr, ¥387,000), architecture online bachelor's (4yr, ¥1,254,000), librarian qualification (1yr, ~¥166,000), school librarian teacher qualification (1yr). FY2025: 566 law + junior college graduates; **1,743 librarian completion certificates** issued. [S2]
- **Stated client objectives.** (1) Halve grading time — ~10 min → under 5 min per report for high-volume instructors. (2) Standardise grading across multiple part-time instructors teaching the same subject, where previous rubric-alignment meetings proved ineffective. (3) Verify authorship via **post-submission oral examination (viva)** with time-limited spoken responses. (4) Use AI-instructor disagreement cases to surface **grader drift** rather than assuming AI error. [S7]
- **The client's own baseline.** An existing procedure (Mr. Ishii's) detects reports requiring resubmission at ~**90%**; the AI reproduction achieved **94.2% detection** across 120 flagged reports. Analysis attributes most AI/instructor disagreement to **the instructor relaxing formatting standards**, not AI error. [S6]
- **What the check actually does (Prof. Fukuda's course).** Students answer four questions (~510 characters each) with exactly one textbook quote per answer in 「」 brackets plus page and line numbers. **13 rules (R1–R13)** validate quote existence and completeness, bracket usage, character counts (400–700 per answer), and page/line citations in Arabic numerals. Rules map to eight submission notes (①–⑧) given to students. [S6]
- **Student-facing prize.** A pre-submission self-check could have eliminated **85 of 241 reports (36%)** that required resubmission. [S6]
- **Integration constraint.** The client operates a **fully in-house LMS (KULeD)** and requires **API-based ingest and write-back with no manual movement of reports between systems**. [S7]
- **Pricing preference.** **Per-student flat pricing ¥700–1,800/month**, explicitly preferred over per-report metering. [S7]
- **Trial design proposed.** Validate accuracy on **240 historical reports from one subject** with no live students, measured against the instructor's verdicts and the existing 90% baseline. Four-week plan: W1 port the procedure and reproduce verdicts for 241 reports; W2 review disagreements with Prof. Fukuda and refine rules; W3 add comment drafts + similarity checking and measure review time; W4 report outcomes and demo the student pre-submission check. [S6][S7]
- **Competitive exposure.** The client is actively evaluating other vendors **specifically for the oral viva feature**. The strongest differentiating gap identified was the **rubric lifecycle** — conversational extraction, multi-instructor governance, versioned re-runs. [S7]
- **Entry-point recommendation in [S2]** (Manabie's own proposal, not a client commitment): start with one or two **librarian qualification** courses, because reports for Information Services Theory and Information Resource Organization Theory must be submitted and accepted before students can apply for the corresponding practical classes. **[S2] itself states this bottleneck "must be confirmed with the university."**
- **Risk the client-facing analysis raises.** A better-written report can conceal weak understanding; a short unfamiliar follow-up question answered **without AI** is more informative than judging the polished report alone. [S2]

## 1.3 Confirmed — internal design and strategy inputs

> Source: **[S3]** "AI Feedback for Higher Education: Implementation Design", 10 Sep 2026, Internal Use Only — Confidential Draft, audience Manabie Product / Higher Ed BD / FDE ([doc](https://docs.google.com/document/d/1Cz-0CMbQM35NAUh5fUB0g6iq9Q-L_9EzbrnH_u8HyxQ/edit)). This is an internal design paper, **not an approved specification**.

- **Core design principle asserted.** Ask instructors to **select and approve, not to create**. Four substitutions: ① write a rubric → approve an inferred rubric; ② write a model answer → anchor on past high-scoring student submissions; ③ write feedback text → extract the instructor's voice from past comments; ④ grade every submission → grade only the first five and approve thereafter. [S3 ch.1]
- **Why.** Only 26.5% of universities have a campus-wide AI environment; half report none. CSU distributed ChatGPT Edu to ~500,000 people and saw a **0.7% voluntary training completion rate**. [S3 §1.1]
- **Evidence cited for rubric calibration.** Zero-shot LLM grading reaches human agreement below **QWK 0.30**; calibration with explicit evaluation criteria raises agreement to **0.64–0.82**. Xie et al. (2024) "Grade Like a Human" improved MAE 4.78 → 3.38 and correlation 0.45 → 0.60 by iteratively refining a rubric from a small number of human-graded samples. [S3 §1.2]
- **Upload priority claimed.** 1st assignment instructions; 2nd past graded submissions + scores (10 works, stable at 20, diminishing beyond; ideally ≥3 per score band); 3rd syllabus (often auto-retrievable from course code); 4th lecture slides. **Slides do not convey grading criteria** — they enable reference-linked feedback and out-of-scope detection only. [S3 ch.2]
- **Proposed setup flow and time budget.** Step 0 course registration 2 min; 1 assignment registration 3 min; 2 upload past submissions 5 min; 2' upload materials 3 min; 3 review inferred rubric 5–10 min; 4 review trial grading 10 min; 5 operation **30 seconds per approval**; 6 semester-end report 5 min. **Initial setup total ≤30 minutes.** Next assignment in the same course needs only steps 1 and 5. [S3 ch.3]
- **Three output layers.** Student: criterion-level evaluation with quoted passages, references to course materials, one-or-two-item feedforward, draft history. Instructor: approval card (criterion scores, highlighted passages, editable draft in the instructor's voice, confidence, one-line "why this score"), class-wide pattern summary, list of students needing interviews, time-saved figure. Institution: assessment consistency report, anonymised rubric bank. [S3 ch.4]
- **Display principle asserted.** Students always see the **instructor-finalised grade**; the preliminary AI assessment is never shown as a grade before instructor confirmation. Draft-stage feedback is labelled "learning support", not a grade. [S3 §4.1]
- **Quality mechanisms proposed.** Anchor stratification + order randomisation; independent per-criterion evaluation with distribution correction; confidence routing (review-all default for high-stakes, low-confidence-only for low-stakes); instructor voice model tracked by weekly edit distance; grounding in course materials with week/page references; learning from correction diffs; **attention audit — inject known-incorrect assessments at 1–2% and require ≥80% instructor detection**; model-agnostic storage schema. [S3 ch.6]
- **Cold-start handling proposed.** No past submissions → instructor grades first five, system switches at the sixth. Past submissions without scores → 10 pairwise comparisons (~5 min). No syllabus → rubric from instructions + past submissions, with mandatory level-description confirmation. Existing rubric → upload and skip inference, but still run trial grading because existing rubrics commonly diverge from actual grading. TAs grading → TA first reviewer, instructor final reviewer. [S3 ch.7]
- **Regulatory frame cited.** MEXT notice for universities and technical colleges (July 2023) leaves generative-AI handling to each university; the K–12 guidelines explicitly list "conducting learning assessment based on generative AI output without teacher judgment" as inappropriate. The **EU AI Act classes AI that assesses learning outcomes as high-risk**, requiring human oversight, logging and documentation **from December 2027**. Third-party content in slides sits under Copyright Act Article 35, but whether AI processing falls within "the process of teaching" is **not settled** — legal review required before deployment. [S3 ch.8]
- **Integration tiers proposed.** Tier 0 = class code + CSV/zip, completable by an instructor alone with no LMS-administrator request (PoC). Tier 1 = SSO + **LTI 1.3** (retrieve assignments/deadlines/submissions, write back grades), usable with Manaba, Moodle, Canvas and Google Classroom. Accepted inputs: PDF, Word, text, images of handwritten work with a transcription-fidelity confidence score. Syllabus retrieval targets UNIVERSAL PASSPORT, GAKUEN, CAMPUS PLAN. [S3 ch.9]
- **Explicitly excluded in [S3].** Graduation theses, seminar theses and specialised open-ended writing — ambiguous criteria, few anchors, high stakes, so the four substitutions do not hold. [S3 ch.5]
- **Pilot gate proposed.** At 8 weeks, expand only if all four hold: setup ≤30 min, approval rate in the 70–85% healthy range, **agreement ≥0.7 QWK** against the instructor's past scores, and instructor intent to continue. [S3 ch.10]

## 1.4 Confirmed — market and GTM positioning (business-authored decks)

> Sources: **[S4]** university proposal deck, Sept 2026 ([slides](https://docs.google.com/presentation/d/1gqjE_yRlDlzJB5hjn8abfi5kprtxzn7v9OIZbewlsDA/edit)); **[S5]** juku/cram-school proposal deck, Sept 2026 ([slides](https://docs.google.com/presentation/d/1tR4TP07-QMEkflpVng4dSA1CDGwbVCPuxK7N-f9_x1M/edit)). Both are sales collateral. Their model-case numbers are labelled by the decks themselves as **hypothetical, not measured**.

**University market (S4):**
- 18-year-old population 740,000 by 2040 (from ~1.10m in 2025, ▲33%); entrants ~640,000 → ~460,000.
- **46.2%** of private universities under-enrolled (275/596) FY2026; 118 institutions below 80% fill.
- 51,000 university dropouts (FY2024, 2.00%); 23% of reasons were decreased motivation / poor academic performance.
- **92.2%** of university students already use generative AI, while **50.4%** of institutions have done nothing about university-wide introduction and 49.6% offer no faculty support; the hardest problem reported is "implementing guidelines in practice" (85.8%).
- Faculty time on educational activities has risen 23.7% (2002) → 30.1%; research time down to 32.1%.
- Central Council for Education report (Feb 2025) proposes reduced subsidies for under-filled universities and a new evaluation system including **learning outcomes** — records demonstrating "what was learned" will be required.
- Deck model case (hypothetical): first-year Academic Writing, 300 students / 2 instructors + 4 TAs, 800-char report weekly. 20 min → **6 min** per report of faculty/TA time; 2 weeks → **next day** return; **0 → 2** revisions.
- Positioning stated: **does not replace the university's existing LMS**; AI can be enabled/disabled per course; faculty final decision is the default; score display selectable (none / levels only / numeric); audit log of who checked, corrected and returned what.

**Juku market (S5):**
- 46 cram-school bankruptcies in 2025 (record; ~90% small schools under ¥10m capital); minimum wage guideline ¥1,176 (FY2026, +¥55); **53.6%** of university entrants via School Recommendation / Comprehensive Selection; **73.7%** generative-AI usage among high-school students.
- Deck model case (hypothetical): 120 students' personal statements across 3 branches / 3 instructors. 30 min → **8 min** per review; 1 week → **next day**; **1 → 3** revisions. Second case: EIKEN writing, 150 students / 20 student-instructors, unified on EIKEN's four aspects (Content · Organization · Vocabulary · Grammar), instructor check 3 min/essay.
- Juku-specific control asserted: **headquarters registers grading criteria, evaluation points and materials once**, so red-pen standards stay consistent as branches increase; change history retained in an audit log.

## 1.5 Confirmed — the 17 Sep AI direction discussion and adjacent product meetings

> **Where the notes live.** The **Weekly AI Direction Discussion of 17 Sep 2026, 10:00 GMT+8** ran in Google Meet and was minuted by **Gemini, not Circleback** — [Notes by Gemini](https://docs.google.com/document/d/1pzUZxU-vZbiNQGfSRBRvu-cqq2uwoweHm9hhTaIO9Is/edit) (quick notes + full notes + full transcript). Attendees: **James Sim, Bunsuke Itamura, Koki Misawa, Trieu Le Hong. Takuya Homma was invited but did not attend** (struck through on the invite). A separate **Takuya / James 1:1** ran the same day at 15:00 GMT+8 and *was* captured by Circleback (`zZo5BHAbqxVjjutrqFeRy`); it covers university GTM rather than app architecture. Both are recorded below and cited separately.

### 1.5.1 Weekly AI Direction Discussion, 17 Sep 2026 — **this is the session that decides how AI Feedback sits in the learner app**

> Source: **[S8a]** Notes by Gemini, as above. Quotes are from the verbatim transcript.

**The unifying decision.** The meeting was an app-redesign review of Koki Misawa's demo, whose stated purpose was merging LMS, AI Tutor, AI Feedback and the J-Prep/study-plan app into **one application navigation**: an **assignment tab**, a **to-do tab** (based on Takuya's B2C app 1.0), and a **course tab**. Koki: *"how we can merge the all the experience into one app… as well as how we can beat the Monoxa."*

> **Transcription note — "error" in this transcript means "LO".** The Gemini transcript renders 「エルオー」(LO) as *"error"*, and sometimes as *"arrow"*, throughout. It is a speech-to-text artefact, not a product concept: there is no "error type" in the learner app. The transcript itself gives the proof — Koki says *"you can have a separate errors right"* and Bunsuke answers in the same exchange *"I think we should have like an all-in-one **LO**… I think we should have a PDF **LO**. We should have a video **LO**"*; elsewhere the same word is transcribed *"if you have one **arrow**, you have one card here"*. **Quotes below are corrected to [LO] in square brackets.** Anyone re-reading the raw notes should apply the same substitution.

**AI Feedback is an LO type in the learner app, and it needs its own icon.** Koki: *"we need to divide the [LO] type further like PDF [LO]s, video [LO]s, quiz [LO]s, you know, AI feedback, you know, AI flash card… so that we can visually see on the to-do list what student needs to be done."* This is the concrete form of the "everything under the LO structure" position from 2 Jul.

**The load-bearing problem raised, and the decision taken — how AI Feedback reaches the student's To-do.**
- Koki stated the problem: *"AI feedback like whenever teacher create should move into [to-do] but… all of things are preset, right? In this case it can be weird — you have all the AI feedback as a to-do, it seems weird."* And more precisely: *"if you do that you have whole semester AI feedback here when teacher publish before the semester, then you have like let's say 20 set of the AI feedback it comes here, it gets too messy. To-do list is something that you want to define what you do right now."*
- Koki also noted the gap: *"we don't have like due functionality on [LO]s."*
- James proposed the mechanism: *"the due date for this specific to-do page should probably be kind of like our customization over the LO. So we don't use the whatever existing LO functions. We have to build on top of that for AI feedback."* And: *"we'll still have the due date function on the AI feedback, it's just only used for this to-do page."*
- Landed on **start + end dates**: James — *"if it's a start date then it will show here based on when it already has passed the start date."* Koki — *"start date is something it shows up on to-do"*, plus an **overdue state**: *"if over should have red color here. Overdue design."*
- **Recorded as an aligned decision in the Gemini notes:** *"Integration of Start and Due Dates for To-Do Populating — the team aligned on utilizing start and due date parameters for AI feedback items to control when tasks populate the student's to-do list."*

**Why the To-do matters more than it looks.** Koki: *"in Japan the most important thing for kids is get them follow the to-dos… whenever kids maintain their schedule they can get good grades… So KPI is pretty simple. You get them follow the to-dos."* And on the teacher's changed role: *"teacher work is set up the curriculum and then get the student to follow that's it"* — question-answering and correct/incorrect marking *"already replaced by AI"*.

**The due-date design problem that is explicitly unsolved.** Koki: *"due date is different per person… you come on Monday and [another student] comes on Tuesday, then your due date is Monday, theirs is Tuesday"*, and per-class variation for group teaching. He was blunt that this has failed before: *"previously we have this idea, study plan is meant to be built for that, and we fail… we couldn't design well, it's not easy."* Provisional lean: *"it's easier that teacher can just set it on the spot for targeted student."* James: *"I think simpler the better. Yeah, even though it's more work."* Teacher's own view of due dates to come from the course dashboard / study plan, not a new screen.

**Other decisions aligned in the same session:**
- **V1 launch in January covers PDF-based practice functionality only.** AI Feedback is *not* in that V1 scope.
- **Self-snap course** for ad-hoc snaps, with subject filters from a predefined subject master list plus AI auto-mapping — chosen over forcing students to pick a course (Bunsuke objected to the added friction; Koki wanted categorisation so a maths teacher's dashboard isn't a mixed-subject feed).
- **This initiative is UI/UX information-hierarchy reorganisation, not backend change.** Bunsuke, on the study-stats page: *"I already got feedback from many clients that they never use this because they don't care about the amount of time they spend."*
- Duolingo-style cards and logo across all age groups; mastery **crowns** (silver >80%, gold 100%) with dynamic progress-bar colour.
- Notifications move to the top/home page; study record reorganised into filterable course stats plus one unified activity timeline, with hints, solutions and practice questions given distinct icons.
- Remote schools will not use TOC; their AI activities default to the timeline view.
- Back-office course names (e.g. "Middle School Grade 1 Mathematics") to be distinct from student-facing names (e.g. "Mathematics").

**PC/web requirement stated for AI Feedback specifically.** Koki: *"most important thing is you need to be able to upload PDF and such kind of stuff for AI feedback, because most of the university student they use PC, they never use smartphone to upload… most of the AI feedback should come from PDF document."* Plus web snap via screenshot or local-file upload (attributed to Takuya). **Note this cuts against the existing V1.1 PRD's mobile-first framing — see C9.**

**Action items from this meeting:**
| Owner | Action |
|---|---|
| Koki Misawa | **Create demo of the start/due-date functionality**, showing how the parameters affect the student to-do list |
| Bunsuke Itamura | **Propose LO structure** — refactor LO types into distinct categories (dedicated PDF and video LO types) |
| Koki Misawa | Update self-snap course structure + subject filtering; finalise back-office mock (EOD); push changes to GitHub |
| Trieu Le Hong | Push the team to finalise domain setup (company business risk) |
| The group | Reorganise study record; build subject mapping system; implement flash cards with AI-generated practice questions |
| JPE | Convert design to Duolingo style |

### 1.5.2 AI Feedback trials grooming, 11 Sep 2026 — current build state

> Source: **[S15]** [Notes by Gemini](https://docs.google.com/document/d/1G_fvpln_a_oLdxXyD6XBRIBKTIxZViwEvuP1DRD76HQ/edit). Attendees: James Sim, John Paoletto, Thi Thu Giang Nguyen, Cuong Hoang.

- **The AI Feedback trial is confirmed to proceed in the pre-release (preprod) environment in October** — bug fixes locked down ahead of a **trial starting 1 October**, with the **release targeted 5 October**.
- **Open defect — teacher rubrics are being destroyed.** Teacher-created rubrics are passed through the **rubric agent** instead of going straight to the **feedback agent**; the agent restructures categories and wording into its own UI format, **erasing the teacher's original work**. Agreed fix: teacher-generated rubrics bypass the rubric agent entirely. *This is the single most important open item for anything claiming a "rubric lifecycle" differentiator.*
- **Rubric weights are being removed because AI Feedback does not use scoring.** *Correct and settled — see C2: scoring belongs to AI Grading and AI Marking, and weights belong to a scoring product.*
- Open defect: AI-generated feedback **number bubbles appear out of sequence, overlapped, or mid-word** on small PDFs; referenced words should be fully underlined and numbers sequential.
- Feedback-generation validation errors involve LangSmith technical/logic issues that **could take up to a month** to resolve.
- Drag-and-drop UI latency causing jumping — fix is optimistic rendering. The non-functional "current questions" bar to be removed.
- Formatting + rubric display fixes estimated at **1 developer day + 0.5 QA days**.
- **AI Feedback dashboard responsibilities moved back to the AI Grading team** (James's decision).
- Trial content delivery is limited to **one page of content from Takuya**, to be delivered by sales/PS. Resource concern raised by Cuong for the October release involving Kindai.
- Image quality issue: artifact-design compression degrades images below RAG usability; resolution is to embed via plain HTML without compression.

### 1.5.3 Takuya / James 1:1, 17 Sep 2026 — university GTM and product direction
- "AI feedback is getting traction across multiple universities; the priority is building a **standardized, versatile workflow that can serve different use cases without rebuilding from scratch each time**." (meeting summary; Takuya in transcript: *"we want to make it as versatile as possible… as general, but like specific about this AI feedback workflow as possible"*)
- Kindai has **two separate tracks**: a small social studies pilot targeting **mid-October** start, and the correspondence course (~**9,000** students) **focused on grading**; the correspondence meeting is **18 Sep**.
- On **the learner app / unified app**: James — *"that topic came up when discussing the unified app… putting everything underneath should be built purposefully for just that use case, the simple block. Everything else is just a front end layer of UI/UX."* Takuya asks whether grading/feedback will be part of the unified app experience; James: *"grading and feedback should be part of it."*
- On the **current prototype's feedback behaviour**: James — *"There is feedback in this prototype, but this feedback doesn't go to the teacher, it's just automatically returned to the student… I don't think it's meant to be this way… we discussed before that it needs to still be teacher given, right? Assignment."*
- On **dashboards in the app**: *"the dashboards are consolidated to a group or individual… one student view would give you an overview of all the different interactions they had, scores they had across the different products"* — so a Kindai teacher dashboard would be integrated into existing group/individual dashboards rather than built ad hoc. Timeline judged too short for first week of October; **late October considered feasible**.
- On **coexistence**: *"even with this unified app, I don't think we can kill like university LMS, for example Canvas or Moodle… we need to coexist."* Takuya proposes reframing Manabie's LMS for universities as **"AI drill / AI practice"** rather than LMS, since universities already run an LMS.
- On **feedback grounded in materials**: Takuya — feedback should be able to say *"please refer back to this textbook, 47 pages"* / *"teacher's materials, slide page X"*; James — *"the digitized assignment needs to follow certain numbering… given that they've uploaded it for creating the feedback assignment."*
- On **Kindai submission format**: *"red pen [grading] is more for elementary, junior high, potentially high school… not for Kindai. Kindai is, I think most of the submissions gonna be PDF."*
- On **accuracy posture**: Takuya — *"90, 95% accuracy is fine"*; on disclaimers — *"we never say like it's 100% accurate."*
- On **content**: universities increasingly want to import existing digital content; content digitization, content mapping and RAG named as key. Content generation to be part of onboarding new clients; Sakuya Iwahashi named as likely owner.
- On **cohort cadence**: university semesters are shorter than school years, so *"the cycle needs to be shorter in terms of onboarding… how do you continue to generate a flywheel for a short lifespan cohort"* — produce insights after each cohort.

**Weekly AI Grading/Marking, 17 Sep 2026** (Circleback `Mkezgcg7nclYlfkKwUau3`):
- AI marking active in the partner pipeline for **Human Campus, Seibi, Eishinkan, Ohzora, Chuo** — all targeting **April 2027** launches or upsell proposals.
- **Eishinkan OCR testing positive: 93% average accuracy, 70% of samples at 95%+**; now testing feature UX in preprod before moving to feedback-quality evaluation.
- **Ohzora's credit-granting exam is a poor fit** for AI grading — even at 80% accuracy every entry needs manual review, likely more work than their current OMR workflow.
- Team agreed AI grading for MCQ/fill-in-the-blank can't reach 100%, but Shozemi's mini-tests are low-stakes enough for teachers to glance through and override.
- **AI grading PRD (US1–US4) updated today**; Qisheng Zhang to finalise Figma, then move to the marking flow after the content side is done.
- Question column removed from the AI grading setup UI — no concrete use case across current clients.

**Content Weekly / Weekly_Content, 17 Sep 2026:**
- **AI marking UI: preprod 21 Sep, prod 5 Oct.**
- **AI 添削 (marking) test: tech-side bulk generation and evaluation 12–16 Oct; client review from 19 Oct.**
- Top Q4 content priority is fixing scoring gaps in the handwriting question types (math and language) before Sanko QA.

**Prior AI Direction Discussions (for continuity, not 17 Sep):**
- **2 Jul 2026** (`H6gDlmhD6x4FeJo9QTQ5Q`): AI Feedback and AI Grading have separate back ends but **are converging into one unified flow** — Q3 milestone is integrating AI Grading and AI Feedback into a single flow; **Q4 is plugging that into the LMS LO submission flow**. Koki Misawa: AI Feedback as a standalone student-initiated feature is hard to sell — *"students won't proactively use it"*; the more useful model is batch processing with submissions auto-returned. Koki also: feedback and grading should both operate **under the LO structure**, with HQ pre-building curriculum because juku teachers won't create assignments on the spot. AI Grading should be sold **with LMS** so the grading agent references LMS LOs instead of requiring answer-key upload.
- **18 Jun 2026** (`Mp8WpM7zD470xd6Upo4lN`): AI Feedback demos well but was **not trial-ready** — assignment-level only, no class management. Bunsuke Itamura suggested structuring the merged product **by assignment type (test vs essay)** rather than by feature, entry point always class/assignments.
- **12 May 2026, AI Tutor Product Catchup** (`51O371bkHOmZJp4u4WAvE`): the team wants AI Feedback output format **teacher-configurable** — sections, titles, granularity (passage vs line level) and length defined by the rubric, plus a standard closing "final comment" block; students choose general vs targeted (assignment-tied) feedback at upload; supported uploads PDF/JPG/PNG.

### 1.5.4 Weekly AI Direction Discussion, 24 Sep 2026 — scoring allowed in the feedback format, the study plan as the date model, dashboards, the LO refactor

> Source: **[S23]** [Notes by Gemini](https://docs.google.com/document/d/1y04oYHnmQ1vFHW5JXALpB6ycbevCn1j6TqNYbOv6Jzw/edit) (quick notes, full notes, transcript). Attendees: James Sim, Bunsuke Itamura, Koki Misawa, Trieu Le Hong; Takuya Homma invited, did not attend. James demonstrated the unified prototype [S20]. The changes these facts imply are planned in `PRDs/ai-feedback-change-plan-2026-09-24.md`; **none has been carried into Parts A–C yet** — the PM decides which and when.

**Aligned decisions recorded in the notes:**
- **Integration of tabulation and scoring in feedback** — *"allow tabulation and include scoring within the AI feedback format."* Bunsuke: *"you should add a score here for feedback… I think we should allow for tabulation in feedback, and we should add scoring"*, while *"the main thing is feedback; scoring is secondary."* Koki: *"for short time I think this is totally fine, I'm thinking about what the future will look like."* **This cuts against C2's "scoring is architecture, not a gap" and C12 P7/P9 as written.**
- **Reuse of the unified marking engine** — the same engine generates comments for feedback, grading and marking; the LOs and UIs stay distinct (Bunsuke: *"the LO will be two different LOs because the UIs are very different"*).
- **Refactoring the course and book user experience** — a separate project stream (James, with Carlo's team), Canvas as the reference: course home → dashboard, add LOs from the course, assign an LO to a class, a QR on the course. James: *"I was using the existing flow so we don't get confused what's new and what's old."*
- **Removal of sequencing from the UI** — the study plan follows the book's sequence; sequence editing leaves the UI (kept for CSV).

**On dates (the T6–T8 boards):** Koki — *"your design UI is okay… I'm talking about the data structure: we should refer to the study plan table"*; Bunsuke — *"the start/end date here becomes an auto-created study plan in the back end… I think that's better"*; both — no new date table; the study plan concept hidden for universities, UI optimised for the one-to-one course–book case; complex remote-school splits (one book, several study plans by joining month) stay in CSV; Bunsuke wants the **book-level access dates removed**. Per-student due-date extension is common in higher education (Canvas, Moodle) and belongs at the study plan's student level, not V1. On V1: James — the due date *"was just a talking point, it's not firm"*; Koki — *"in that case you can release without having due date, because that refactoring takes time"*; V2 builds it on the study plan structure.

**On dashboards:** the feedback LO sits in the existing rows; per LO type, the header and the cell contents change; *"show it for the ones that are relevant and blank for the ones that are not"* (Bunsuke); *"we just need score and status, we don't need max"* (Koki); the ▾ under a cell opens the submission history as it does for scores today; the topic dashboard is a quick link, the LO matrix is what people look at. Koki to send cleaned-up mockups; James to apply the principles.

**On LO types:** Bunsuke's restructuring of all LO types is discussed **Monday 28 Sep**. The university weekly reflection is typed into the LMS or learner app, not paper, and is separate from Lenosity; *"we just need to rename it, but it's the same LO"* (Bunsuke) — *"same"* (James).

**Action items:**
| Owner | Action |
|---|---|
| James Sim | Refactor the course and book management UX with Carlo's team, integrating the new AI-product LO concepts |
| The group | Enable tabulation and scoring in the AI feedback interface |
| Koki Misawa | Adjust the group and student dashboard designs to the agreed data-structure principles; send to James |
| The group | Discuss the LO-type restructuring on Monday |

## 1.6 Confirmed — the learning-log dashboard and the Kindai showcase

> Sources: **[S16]** [AI Feedback — Handover (John → James)](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2862710799/AI+Feedback+Handover+John+James), Confluence PRDM, created 7 Sep 2026, **explicitly a draft**; **[S17]** the handover zip `ai-feedback-dashboard-handover.zip` (prototype + fixtures + competitor research); **[S18]** Slack thread in `#C0BPM7T182C`, 17 Sep 2026, John Paoletto → James Sim, cc Hinano Matsushita.

### 1.6.1 Why the dashboard exists, and the decision already taken

- **The client did not ask for it.** [S16] is explicit: *"Learning-log visibility is not a client expectation either."* It exists because on 17 Aug Hinano made the point that AI Feedback has **no learning-log visualisation** and she needs something to show.
- **Takuya's position:** any dashboard built now is **prototype-grade**, because it will be rebuilt when AI Feedback merges into AI Grading.
- **The decision taken:** John builds a **dummy-data mock**, reviews it with Hinano, and during the trial Kindai is shown **manually created dashboards** rather than anything built into the product. [S16 §4]
- **The strategy:** use the trial to find out **which views teachers actually value**, and put only those on the roadmap. *"So the mock is a menu of what could be shown, not a spec."* [S16 §4]
- **John's three goals, restated on 17 Sep** [S18]: (1) create a manual dashboard **rather than developing one in Back Office**, (2) show it to clients through sales and trials **using data we can actually collect today**, (3) put what resonates with clients into the backlog.

### 1.6.2 The showcase itself — what Hinano confirmed on 17 Sep

- **Hinano wants to start showing the dashboard to clients ASAP, and wants to align on the final visuals and content for the manual dashboard *this month*.** [S18]
- James asked which subject to showcase. **Hinano: *"Yes weekly class submission and the subject will be Regional Environmental Statistics (地域環境統計学)."*** [S18]
- **This maps to the use case [S16] records as *not scoped*** — "Per-class mini reports (minute papers)": every-lecture **300-character reflections for 150–300 students**, where *"the professor wants rubric-based feedback immediately on submission and a way to pick out the comments worth reading. Any scoring would stay with the teacher — AI Feedback does not score."* [S16 §2]
- Current state per [S18]: dummy data matching what can be collected today, plus *"an idea-board of what we could show using that data (not even a mock/prototype, mostly like let's-clean-from-here ideas)"*. Remaining steps John listed: **look at competitors (stopped here) → distill & simplify → surface what it means clearly**.

### 1.6.3 What the prototype in [S17] actually is

- `dashboard.html` — one self-contained file, no server, no build, no dependencies. Japanese UI on the school-portal-admin design system (`manabieV5` tokens: Roboto 14px, `#2196F3`, `#F4F6F9`, 4px cards).
- Fixtures are **complete `sessions` row envelopes** that load into the real table unreshaped, following the live service contracts (`STATE_KEYS` from the migrate scripts, field shapes from `ai_feedback_svc/models.py`, `ChatMessage` from `chat_bot_svc/models.py`, chat→submission link via `state.ref_thread_id`). Tenant `-2147483622` (staging) is the only real identifier.
- `build.py` is deterministic (no RNG, no wall-clock, ids from `uuid5`). Reported state: **1578–1655 structural checks, 0 failed; 161–162 objects validated against the live Pydantic models; ruff clean.**
- **The product thesis in one line, from [S17]:** *"the essay is worthless as evidence; the trail of revision is not."* It measures **uptake** — what the student did with the feedback and in whose words — not provenance.
- **Two judgement calls encoded in code**, both flagged by John as the heart of the product and both previously wrong: `rewrite_quality()` (own / rephrased / copied verbatim, token containment ≥ 0.55 — *"works on authored data, needs tuning on real text"*) and `student_turns()` (asking vs. putting their own view forward — regex, *"should become a cheap LLM classification"*).
- **Demo dataset:** one class — みどり市立第一中学校 2年B組, **25 middle-school students**, six weeks, **two assignments (English + Science)**, 19 of 25 submitting. Everything fictional.

### 1.6.4 Design rules already encoded — stated as constraints, not preferences

[S17 §8] says each exists "because the obvious alternative actively misleads":

| Rule | Reason given |
|---|---|
| **Counts and names, never rates** | A denominator that depends on who chose to use the tool swings on adoption, not learning. Ratios only where the denominator is intrinsic to one student's own work |
| **Never show chat transcripts** — not raw, not AI-summarised. Only the student's *own* question text renders; the AI's replies never do | *"If students suspect a teacher reads their conversations, they stop thinking out loud and start performing."* Deliberately the opposite of Turnitin Clarity |
| **No leaderboards, no per-student score** | Produces evidence for a teacher's judgement, not a mark. *"Anything you rank, someone games"* |
| **「一度きり」/「未提出」, never "not trying"** | The system cannot distinguish disengagement from confusion, illness or overload |
| **Never compare raw comment counts between drafts** | Count varies with document length and model run-to-run variation |
| **Read improvement and engagement together** | High resolution with zero engagement is what pasting the AI's fix looks like |
| **Explicitly not building: AI detection** | — |
| Colour language | green = own words · light green = rephrased · grey = verbatim · blue = submissions and plain questions · orange = own opinion/proposal and still-open issues |

A student whose improvements are *all* "copied + no dialogue" gets **one quiet line suggesting a verbal check — never an accusation, never a per-comment flag**.

### 1.6.5 Four hard preconditions before the dashboard can touch real data [S17 §7]

1. **Criterion keys must be assigned at the assignment, not re-derived per run.** The live service regenerates them every submission, so keys drift (`evidence` → `use_of_evidence`) and silently split any grouping. Called *"a hard precondition"*.
2. **Persist which comment a conversation was about.** Production discards it; the timeline needs it, and the alternative is reading transcripts, which the design forbids.
3. **Confirm the class roster join** — rosters live in the backend Go service, not the ai-tutor database. `roster.json` is a stand-in.
4. **Stamp the marking config onto each record.** Model and prompt live in `temp:assistant_config` and are never persisted, so today you cannot tell student improvement from a mid-term model change.

### 1.6.6 Competitive position and the 観点別評価 finding [S17]

- **Turnitin Clarity** is the closest product (drafting process, pasted text, writing time, version playback, per-assignment AI policy) and **exposes the student–AI chat to teachers** — the opposite call. **Turnitin Draft Coach** deliberately hides student version history from teachers, which is precedent for our position. **Grammarly Authorship** classifies spans by provenance. **Packback's Writing Process Report** is closest in philosophy and warns it *"should never act as a single indictment of student behavior."* **atama+** tracks 理解度 on problem sets, not writing process.
- Research cited: *"Generative AI offers more, but students revise less"* (2026) — if it generalises, the scarce resource is **uptake**, not feedback volume.
- **The 観点別評価 opportunity:** Japan's 主体的に学習に取り組む態度 requires evidencing 粘り強い取組 and 自らの学習を調整, and prefectural guidance asks for 文章記録等のエビデンス. [S17] argues the dashboard already computes both under different names, and recommends relabelling plus a printable evidence sheet — *"evidence for a grade they are already required to assign and currently struggle to justify."*
- **Note the segment mismatch:** 観点別評価 is a Japanese **K-12** framework. It does not apply to Kindai, a university. This finding is strong for the **Juku/school secondary market**, not for the showcase in hand.

### 1.6.7 Other facts from [S16] that correct or sharpen earlier sections

- **AI Feedback does not score.** Stated three times in [S16]: *"It gives feedback only — no grading or scoring happens"*; *"feedback only, no grades or scores"*; *"Any scoring would stay with the teacher."* Agreed long-term direction (AI Q2 priorities alignment, 9 Jul): it **merges into AI Grading as the feedback-only mode** rather than staying standalone. **U15 is closed by this plus the PM's confirmation (17 Sep) that scoring belongs to AI Grading and AI Marking — see C1/C2.**
- **The rubric defect, in more detail than [S15] gave.** Today the teacher's saved rubric is *"only one of three inputs (with the student's request and what the AI thinks the document needs), gets rewritten into a handful of one-line criteria per submission, and silently falls back to a generic accuracy/completeness/clarity rubric if the rewrite fails."* Required: no rewriting, re-weighting, merging or dropping; no silent fallback where a saved rubric exists; AI-generated rubrics only when none is saved; the rubric actually used visible to the teacher or at least in logs/QA. Tracked as **PBT-3845** (which also covers **chat-prompt tuning — the AI Feedback chat prompt has most likely never been tuned**) and **PBT-3839**.
- **Tenant enablement as of 4 Sep** — directly usable for Part E: `lmsv2` pre-prod **ON** (full set: AI Feedback, Assignment, Assignment Feedback, Class Assignment, ToC, Similar Question); `aidemo2` prod **ON** (current sales demo tenant; ToC had to be enabled to make AI Feedback History work); `lmspsai` / `aidemo` prod **OFF** (turned on 3 Sep for a demo, reversed 4 Sep — *"aidemo is for trials, use aidemo2 only"*); `sankogakuen` pre-prod **testable** (AI添削 since 21 Aug, prod not configured); `demo-lms` prod **not available**. Enablement is a config change by the AI Tutor tech team (Cuong Hoang) — ask in `#ai-tutor-tech` naming tenant, environment and whether Class Assignment comes with it.
- **Submission path:** students **export to PDF** (e.g. PowerPoint → PDF). There is **no direct PowerPoint or document upload**, and [S16] flags this must be framed to the professors as the workflow before the October hands-on *"so it is framed as the workflow, not discovered as a limitation."*
- **Out of scope for the trial:** RAG over lecture materials for AI Tutor — Takuya's call, workflow fit unproven.
- **Pricing detail:** ¥900 + ¥700 = ~¥1,600 per student per month; 140 students × 3 months ≈ ¥672,000 untaxed; **pricing holds under 1,000 students**.
- **Open student-side bugs** (all Must-have, raised 15 Jul): highlight spans break on maths notation (LT-108239, Ready for QA); reference text spaces collapsed / double-delimited (LT-108240, Ready for QA); number bubbles land inside words (LT-108241, In Product Refinement); generation fails when the snap contains no detectable question (LT-108798). Plus unparented: LT-110085 (result not saved/shown in History after successful analysis, prod aidemo2), LT-109760 (Snap and AI Feedback cannot load inside a Class Assignment), LT-109763 (generation fails if the app backgrounds), LT-102617 (extracted-text errors).
- **People:** Hinano Matsushita (Kindai account owner — first call for anything client-side), Takuya Homma (exec sponsor, direction and spec), Yuna Chi (rubric pipeline + prompt tuning; AI Grading PM), Qisheng Zhang / "Hugh" (design — BO rubric and distribution clean-up, PBT-3837), Cuong Hoang (AI Tutor tech lead — tenant enablement), Bunsuke Itamura (PMO).

## 1.7 Stated but unconfirmed — each needs a named owner before it can be used

| # | Statement | Source | Why it is not confirmed | Owner to confirm |
|---|-----------|--------|-------------------------|------------------|
| U1 | Kindai Applied Sociology trial is approved and funded | [S1] | Gate was the 16 Sep 2026 extraordinary faculty meeting; outcome not recorded in any source read. The 9 Sep committee result was also **not found**. | Hinano Matsushita / Takuya Homma |
| U2 | Correspondence Division enrolment is 9,600 vs 10,273 | [S7] vs [S2] | Two different figures; [S2]'s 10,273 is a census including non-degree students. Also Takuya said "~9,000" on 17 Sep. | Hinano Matsushita |
| U3 | Prof. Fukuda's subject is civil law or constitutional law | [S6] vs [S7] | The two briefs disagree. Affects which 240 historical reports the trial uses. | James Sim, at the 18 Sep correspondence meeting |
| U4 | Per-student flat pricing ¥700–1,800/month is acceptable to the correspondence division | [S7] | Recorded as a client *preference*, not an agreed commercial term; no quotation issued for this track. | Takuya Homma |
| U5 | The librarian qualification courses are a real progression bottleneck | [S2] | [S2] states explicitly this "must be confirmed with the university". | Hinano Matsushita |
| U6 | ~140 students will actually enrol | [S1] | Registration not closed; quotation reserves 150 seats. | Hinano Matsushita |
| U7 | Evaluation thresholds (first-login ≥85%, weekly completion ≥60%, +10pp on unseen data, faculty correction <10%, authoring workload ▲25%) | [S1 §9] | [S1] states plainly: "No university-approved success criteria were found… these should be treated as working targets, not agreed contractual KPIs." | James Sim + Takuya Homma |
| U8 | Setup ≤30 min, 30s/approval, 70–85% approval rate, QWK ≥0.7, 1–2% attention-audit injection at ≥80% detection | [S3] | Internal design paper proposals. Never validated against a live cohort, never costed, never reviewed by a TL. | James Sim → Tech Lead |
| U9 | Deck model-case deltas (20→6 min, 30→8 min, 0→2 / 1→3 revisions, next-day return) | [S4][S5] | The decks themselves label these hypothetical and say they will be measured in a pilot. **They are sales assumptions, not product targets.** | Takuya Homma |
| U10 | Oral viva (post-submission spoken authorship check) is in Manabie's scope | [S7]; PM confirmation 22 Sep | **Closed — it is not a feature.** The viva is the client's own workflow, which our output complements: the instructor holds it, using the submission and the feedback as material. Manabie builds nothing for it. See C2. | — (closed) |
| U11 | File-upload defect and missing learning-log visualisation are still open | [S1 §10] | Status recorded as of **17 Aug 2026** — one month stale at time of writing. | Tech Lead |
| U12 | Kindai correspondence wants grading, not feedback | Takuya/James 17 Sep | James: *"so far what you shared is mostly gearing towards grading"* — an inference from translated meeting notes, with the clarifying meeting on 18 Sep. | James Sim |
| U13 | Artifacts [S6] and [S7] are Manabie-authored | Artifact tool | Returned marked "created outside your organization". | James Sim |
| U14 | Uploaded file `overall_ranking_en.html` content | User upload | **The file is a Slack application shell with no recoverable content** — text extraction yields only the word "Slack". Nothing from it has been used. Re-share as a Slack permalink or export. | James Sim |
| U15 | AI Feedback does not use scoring | [S15]; [S16]; PM confirmation 17 Sep | **Closed — settled architecture, in Part C.** AI Grading and AI Marking are always about scoring; AI Feedback is the feedback engine they and the learner app call when additional feedback is warranted on top of a score. Kindai's 0–5 rubric supplies criteria, not an AI score; [S3]'s scoring apparatus describes AI Grading. See C1 and C2. | — (closed) |
| U20 | Kindai trial start date | [S1] vs [S16] | [S1]: from class session 8 on **6 Nov 2026**. [S16]: *"AI Feedback from lecture 10 onward… late Nov/Dec to early Feb."* **These do not agree**, and the earlier date is the one in the quotation. | Hinano Matsushita |
| U21 | Which tenant hosts the Kindai trial | [S16 §2] | Open item in the handover: `aidemo` was described as "for trials" but is being retired; a Kindai tenant needs AI Feedback + Class Assignment + ToC enabled in time for October. | James Sim → Cuong Hoang |
| U22 | The showcase dashboard can be produced from data collectable today | [S18] claims it; [S17 §7] contradicts it | John's stated goal is "data we can actually collect today", but [S17 §7] lists **four hard preconditions** — criterion keys drift per run, the comment a conversation hung off is discarded, the roster join is unconfirmed, marking config is never persisted. **Fixtures matching the row shape is not the same as the data existing in production.** | James Sim → Cuong Hoang |
| U23 | The demo dataset suits the Kindai showcase | [S17 §9] vs [S18] | The prototype's dataset is a **middle-school class (中学2年, 25 students, English + Science)**. The showcase is a **university course, 地域環境統計学, weekly reflections, ~140 students**. Wrong level, wrong subject, wrong scale, wrong assignment shape. | James Sim |
| U24 | Minute-paper / weekly-reflection use case is scoped | [S16 §2]; PM confirmation 17 Sep | **Closed.** Both the weekly reflection and the weekly exercise are in scope for the trial — see C10.3. Dependency it creates: the reflection needs its own 2–3 criterion rubric, which Prof. Yasumoto must author and nobody has requested. | — (closed; rubric dependency open) |
| U25 | Who owns the AI Feedback dashboard | [S15] vs [S16 §4] | [S15] 11 Sep: responsibilities moved back to the **AI Grading team**. [S16]: the RISO-funded AI Dashboard is the natural home once the products merge, and PBT-3450 / PBT-3356 teacher-dashboard AI Feedback counts are marked done on the roadmap but were **still in Tech Review with metrics definitions under review on 4 Sep**. | James Sim |
| U16 | Start/end-date layer over the LO is the agreed mechanism for To-do population | [S8a] 17 Sep | Aligned in the meeting as a direction; the demo that makes it concrete is an open action on Koki, and per-student/per-class due dates are explicitly unsolved. | Koki Misawa → James Sim |
| U17 | AI Feedback dashboard sits with the AI Grading team | [S15] 11 Sep | James's decision, recorded in grooming notes. Needs confirming against the Kindai pilot's dashboard need and against the 17 Sep "consolidated group/individual dashboard" position. | James Sim |
| U18 | Rubric-overwrite fix (teacher rubrics bypass the rubric agent) is implemented | [S15] 11 Sep | Agreed in the meeting; no ticket status confirmed as done in any source read. Blocks the "rubric lifecycle" differentiator. | Cuong Hoang |
| U19 | January V1 excludes AI Feedback | [S8a] 17 Sep | Aligned that V1 is "PDF practice only" — but the AI Feedback preprod trial starts 1 Oct and Kindai goes live 6 Nov. The January PDF-practice V1 is RISO's vehicle, not Kindai's, so it is not a competing timeline for this PRD; confirm the three are separate vehicles. | James Sim |

---

# PART A — BUSINESS

> **Not authored.** The material below is a set of candidates and the questions that close them. A single client asking once — however clearly — is not a business goal.
> The field is bounded: this PRD is the LO integration for the Kindai Applied Sociology trial. The Correspondence Division's grading assistance, the engine contract and the oral viva belong to a later **AI Grading PRD**.

## A1. Business goal & outcome metric — *PM decision required*

**Questions that must be answered:**

1. **What is the business outcome?** The sources support at least three materially different ones, and they imply different builds:
   - *(a) Win and retain university accounts* — the metric would be signed university contracts / pilot-to-paid conversion.
   - *(b) Make AI Feedback the shared engine* behind AI grading feedback, AI marking feedback and the Feedback LO — the metric would be % of feedback generated through one pipeline, or engines retired.
   - *(c) Reduce instructor time per submission* — the metric would be measured minutes per approved submission.
   These are not the same goal. **Pick one primary.**
2. **What is the ONE primary metric and its target + timeframe?** No source contains an agreed metric. [S1 §9] targets are explicitly not agreed with the university (U7); [S3] targets are internal proposals (U8); [S4]/[S5] numbers are sales assumptions (U9).
3. **Supporting metrics / tracking — what must the product log?** Candidates surfaced by the sources, none yet decided:
   - instructor edit distance per approval over time — how much of the draft the teacher rewrites before returning it [S3]
   - time from submission to return; actual instructor seconds per submission [S3][S4]
   - resubmission/revision count per assignment [S1][S4][S5]
   - basic-requirements check usage and the resubmissions it avoided [S6]
   - how often a teacher highlights a submission for the class, and whether the Topic Dashboard's insight line is opened or ignored
   - Learning-log visualisation was not implemented as of 17 Aug 2026 [S1 §10, U11]. If tracking is a goal, this is a dependency, not a reporting afterthought.

## A2. Scope of applicability — *PM decision required*

- This feature is: **General / Tenant-configurable / Partner-specific** — **not decided.**
- **Candidate (strongly evidenced, still the PM's call): Tenant-configurable, built general.** The direction stated on 17 Sep is a *"standardized, versatile workflow that can serve different use cases without rebuilding from scratch each time"* (Takuya, 17 Sep) and *"built purposefully for just that use case… everything else is just a front end layer of UI/UX"* (James, 17 Sep).
- **The specific values that must NOT be hardcoded to Kindai**, each of which appears in the sources as a concrete number and each of which needs an explicit Env-level / Tenant-level decision in C3:
  - feedback length ~400–600 Japanese characters [S1]
  - three-part feedback structure (recognition / reflective question / actionable guidance) [S1]
  - six rubric dimensions on a 0–5 scale [S1] vs five criteria [S4] vs four CEFR-aligned criteria [S5] vs 13 format rules R1–R13 [S6]
  - 10–20 past submissions as anchors; first-five cold start [S3]
  - character count bounds 400–700 per answer [S6]
  - 1–2% attention-audit injection rate [S3]
  - confidence threshold for routing [S3][S7]
- **Question to answer.** Kindai Applied Sociology's rubric includes a **generative-AI literacy** dimension [S1 §3]. What has to be decided is whether one rubric model serves a university's criteria and a juku's. The correspondence division's 13 formatting rules [S6] are not part of this question — they belong to the AI Grading PRD.

## A3. Business rules owned by Biz — *PM decision required*

Rules the sources show Business, not Engineering, must decide. None are decided:

1. **Pricing model.** ¥900 AI Tutor + ¥700 AI Feedback per student per month is quoted for Applied Sociology [S1]; the correspondence division prefers ¥700–1,800 per student flat, explicitly not per-report [S7, U4]. Is per-student flat the model for universities generally?
2. **Score display policy.** [S3] and [S4] both assert students must never see a preliminary AI assessment as a grade before instructor confirmation. This is a **policy commitment with regulatory weight** (MEXT; EU AI Act high-risk from Dec 2027 [S3 ch.8]) — Biz must own it, not infer it.
3. **Accuracy claims made in sales.** Takuya, 17 Sep: *"we never say like it's 100% accurate"*, and 90–95% is acceptable. What exactly may be claimed, and against what evaluation set?
4. **Data, rights and retention.** Use of past student submissions; third-party copyrighted content in lecture slides under Copyright Act Art. 35, where AI processing is **not settled law** [S3 ch.8]. [S3] recommends syllabus language and a one-page template for the university's personal-information office. Legal review is named as a precondition to deployment — is it commissioned?
5. **Who may turn teacher review off for an LO.** Teacher review is a per-LO switch; [S4]/[S5] promised clients that administrators confirm responsibility before auto-return is enabled. Biz owns the answer.
6. **What Manabie commits to for the pharmacy-school track** — 1,103 students, full annual implementation, no trial appetite [S1 §11].

*Business sign-off is captured once at the Section D readiness gate, not here.*

---

# PART B — PROBLEM

> **Not authored.** A job-to-be-done drafted from a meeting note is how a stray remark becomes a committed behaviour. Below are the candidate jobs the sources point at, and the tests each must pass.

## B1. Problem statement (job-to-be-done) — *PM decision required*

**Candidate core jobs.** They belong to different people and pull the build in different directions — the PM picks one core and demotes the rest to secondary:

| # | Candidate job (verb + object + context) | Whose job | Source |
|---|---|---|---|
| J1 | *Return usable feedback on a written submission to every student, within a cohort too large to hand-mark* | Instructor / TA | [S4] 300 reports × 20 min = 100 hrs/week; [S2] 62,000 reports/yr across 156 faculty |
| J2 | *Apply one grading standard consistently across many part-time instructors teaching the same subject* | Programme owner / academic affairs | [S7] "previous rubric-alignment meetings proved ineffective"; [S5] HQ registers criteria once across branches |
| J3 | *Revise my own work before it is graded, knowing what specifically to change* | Student | [S1 §2.1] submit→feedback→revise→resubmit; [S6] 36% of resubmissions avoidable by pre-submission self-check |
| J4 | *Confirm the submitted work reflects the student's own understanding* | Instructor / institution | [S7] oral viva; [S2] "a better-written report can conceal weak understanding" |
| J5 | *Demonstrate to an accreditor that grading criteria were explicit and consistently applied* | Institution / IR / FD | [S3 §4.3]; [S4] Central Council for Education Feb 2025 |

**Stability test to apply to whichever is chosen:** would this job still be true if Manabie built nothing, and in ten years? J1–J5 all pass that test. Note that **"unify AI Feedback and AI Grading onto one back end" does not** — that is a feature, an engineering goal, and must not be written here.

**Which candidates the scope leaves live.** The core job is still B1's open decision, but the field is narrower. **J1 and J3 sit inside this PRD.** **J2** (one grading standard across part-time instructors) and **J4** (confirm the work is the student's own) belong to the AI Grading PRD, since the Correspondence track and the viva went there. **J5** (evidence for an accreditor) is not scoped either way and would need its own case. Choosing a core job from J2 or J4 would mean reopening the boundary, not just picking a row.

**Then frame it:** *As a [persona], I want [outcome] so that [value].* — to be written by the PM.

## B2. Desired outcomes (the user's success metrics) — *PM decision required*

Candidates, each to be restated by the PM as *direction + metric + object + context*, and each to be solution-free. Every element of Part C must move at least one of these:

- Minimise the time between a student submitting work and receiving actionable feedback on it. *(currently 2 weeks at 300-student scale [S4]; "20+ days" in juku [S11 repo SOW])*
- Minimise the instructor time required to return feedback that the instructor is willing to put their name to.
- Minimise the variance in grading standard across instructors teaching the same subject.
- Increase the number of revision cycles a student completes before final submission.
- Minimise the likelihood that a student submits work that will be rejected on grounds they could have fixed themselves.
- Minimise the likelihood that a polished submission conceals weak understanding.
- Increase the instructor's confidence that the returned feedback matches their own judgement. *([S3] proposes asking this directly on a five-point scale)*
- **Minimise the time a teacher spends working out what the class as a whole got wrong this week.** *(The Topic Dashboard's insight line is built for this outcome — C10.0.)*

**Watch for the collapse:** A1 (how the company wins) ≠ B2 (how the user judges the job done) ≠ C6 (how QA proves the build works). Do not let "QWK ≥ 0.7" appear in all three.

## B3. Current situation & pain (trace the job) — *PM to complete*

Raw material exists to trace the job, but the trace itself is the PM's work. What the sources give:

| Job step | What the sources say happens today | Where it breaks | Source |
|---|---|---|---|
| Locate / set up | Instructor has syllabus, assignment instructions, slides, past graded work — scattered; no rubric written down | "Please write a rubric" loses to doing it in ChatGPT Edu or by hand | [S3 ch.1–2] |
| Prepare | Rubric alignment attempted via meetings across part-time instructors | Recorded as ineffective | [S7] |
| Execute | 300 reports/week × 20 min, or 500–600 reports/yr per high-volume instructor at ~10 min | Exceeds available TA hours; degrades to score-only returns | [S4], [S7] |
| Confirm | Grading standards drift; instructor relaxes formatting rules inconsistently | Most AI/instructor disagreement traced to **instructor** inconsistency, not AI error | [S6] |
| Return | 2 weeks (university) / 1 week–20+ days (juku) | Student has moved on; revision count 0 | [S4], [S5] |
| Monitor | Learning-log visualisation not implemented as of 17 Aug 2026 | No trail to show the university, IR or accreditors | [S1 §10] |

**Walk the whole job before writing C3** — this trace is what surfaces the edge cases.

## B4. Who is affected (executor vs buyer) — *PM to complete*

| Persona | Role | Market | Key desired outcomes (from B2) |
|---|---|---|---|
| Course instructor / professor | Executor **and** influencer | JP university | *TBC* |
| TA / part-time instructor | Executor | JP university | *TBC* |
| Student | Executor (of revision) | JP university | *TBC* |
| Academic affairs / FD / IR | Buyer or budget influencer | JP university | *TBC* |
| Faculty budget committee | Buyer | JP university (Kindai: the 16 Sep gate) | *TBC* |
| Juku HQ / owner | Buyer | JP juku | *TBC* |
| Juku classroom instructor (often a student instructor) | Executor | JP juku | *TBC* |

**The buyer's financial outcomes must be stated separately.** University: faculty capacity without headcount, under-enrolment pressure and the Feb 2025 Central Council report's learning-outcome evidence requirement [S4]. Juku: correction labour-hours per branch, and "unlimited revisions until application" as a course selling point [S5]. Kindai Applied Sociology's buyer is a **faculty budget meeting**, not the professor — a solution Prof. Yasumoto loves but the faculty won't fund does not ship.

**Note on the executor split, from the 17 Sep direction discussion and 2 Jul:** Koki's position is that a student-initiated feature will not be used — *"students won't proactively use it"*. The current V1.1 product **is** student-initiated. This PRD resolves that: the teacher creates the assignment and the student answers it, so the executor is the instructor at set-up and the student at submission.

## B5. Evidence — *PM to promote from Section 1 with judgement*

Section 1 is what we were told. B5 is what the PM decides actually proves the problem is real and big enough to size the build. **This promotion is a decision, not a copy-paste.**

**Assessment of evidence strength as it stands:**
- **Strong, but it sizes the other PRD:** the correspondence division's volume (62,000 reports/yr, 156 faculty, 500–600 reports per high-volume instructor) [S7] and the 241-report retrospective showing 36% avoidable resubmissions [S6] — measured, from the client's own operation. The work it justifies belongs to the AI Grading PRD, so this PRD's own evidence is thinner than the document as a whole suggests.
- **Moderate, and it is what this PRD rests on:** Kindai Applied Sociology — well-specified course, rubric, materials and quotation, but **~140 students, one professor, one course, and not yet approved** (U1). Two-university interest plus a well-attended faculty seminar (Takuya, 17 Sep) is directional, not sized.
- **Weak — do not size the build on these:** all model-case deltas in [S4]/[S5] (self-labelled hypothetical, U9); all [S1 §9] evaluation thresholds (explicitly not university-approved, U7); all [S3] operating targets (internal proposals, U8).
- **Counter-evidence that should change scope, not be filtered out:** Ohzora's credit-granting exam was judged a *poor fit* even at 80% accuracy because every entry still needs manual review (Weekly AI Grading, 17 Sep). Kindai is deploying Google AI Pro for Education broadly [S1 §10]. Both point the same way — the defensible value is workflow, rubric governance and the record, not model output.

---

# PART C — SOLUTION

> Numbers floated in meetings and decks are **inputs the TL must validate**, not rules. Anything flagged *open* or *TBC* below is still an open question.

## C1. Solution summary — *scope decided; the summary itself still to be written by the PM*

> **What this PRD is, in one line.** **The LO integration**: AI Feedback as a learning-objective type in the LMS and the learner app, set up in Book Management, processed in Course › Submission Grading, and reported in the Group and Student Dashboards — serving the **Kindai Applied Sociology trial**. It is not the Q3 merge of AI Grading and AI Feedback. The engine contract behind that merge, the scoring products' own flows, and the Correspondence Division's grading assistance belong to a later **AI Grading PRD**.

**The architecture below is context, not scope.** Surface 3 is this PRD's subject; surfaces 1 and 2 are named only so the boundary is visible:

**AI Feedback is the feedback engine** — rubric/criteria in, submission in, criterion-linked instructor-voiced feedback out, **no score** — called by three surfaces. Scoring stays with AI Grading and AI Marking, which call the engine when additional feedback is warranted on top of the score:
1. **AI Grading feedback** — feedback attached to a **paper / photo** submission (AI Grading owns the score; OCR sits on this path).
2. **AI Marking feedback** — feedback attached to an **LMS Assessment LO** submission (AI Marking owns the score; the submission is already digital and already attached to an LO).
3. **A Feedback LO in the learner app** — feedback as a distinct **LO type** inside the existing LO submission flow, carrying **its own icon** on the To-do list alongside PDF, video, quiz and AI flash-card types. The LO is created in Book Management's Add Learning Objective dialog as one more LO type, in the hierarchy Book → Chapter → Topic → LO per the [Book Management PRD](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/1133903925/Book+Management) **[S21]**; its settings are resubmission (default off), accepted submission methods (file / photos / typed, 500-character limit on typed) and teacher review (default on); its content page holds the teacher's material, the generated **basic requirements** that gate submission, and the generated **rubric** that shapes the comments. **The submission window is not the LO's:** start and due dates are managed on the Course Management page, the book is linked to the course, and the course's window gates submissions — which also drives when the LO becomes clickable and when it reaches the To-do. Submissions are processed under **Course › Submission Grading**, production's existing home for work waiting on a teacher.

> **The Grading / Marking split:** **AI Grading is for paper and photo submissions. AI Marking is for LMS Assessment LO submissions.** The two are distinguished by *where the submission comes from*, not by how it is scored — both score. Surface 1 hands the engine OCR-derived text with all the confidence and layout caveats that carries, while surface 2 hands it clean digital text already bound to an LO, a rubric and a student record; one engine contract has to serve both, or there are two contracts. Surfaces 2 and 3 both sit on LOs, so the Feedback LO must be distinguishable from an Assessment LO that merely *received* feedback.

**Settled at the level of the summary itself:**
- **This PRD is the Q4 LO integration**, not the Q3 merge. 2 Jul set Q3 = merge AI Grading + AI Feedback into one flow and Q4 = plug into the LMS LO submission flow; this PRD is the second of those. The merge is a separate release with its own risk and its own PRD, so nothing here should be read as specifying it.
- **It serves the Kindai AI Feedback trial and its dashboard.** The January unified-app V1 of *PDF-based practice* is a RISO vehicle, not Kindai's, so it is not a competing timeline for this scope. The dates that bind here are the **preprod trial from 1 October with a 5 October release** [S15] and **Kindai Applied Sociology live from 6 November** [S1 §1].
- **Teacher review is a per-LO setting** (先生の確認 / Teacher review) in the Add LO dialog, **default on**. On: after the due date every draft waits in Course › Submission Grading for the teacher to review, edit and return it; only 承認して返却する makes the feedback exist for the student. Off: the feedback is returned automatically after the due date and the row carries an Auto-returned chip in Submission Grading. **Either way the student is never told AI was involved:** to the student, the teacher gives the feedback, so the student-facing name of the LO type is フィードバック / Feedback and "AI Feedback" is the internal and Back Office name. *Open: whether the student-facing copy should differ when review is off, since "the teacher gives the feedback" overstates the unreviewed case.*
- **The AI Feedback V1.1 exclusions of the teacher dashboard and of iterative feedback are superseded.** Resubmission is a **per-LO setting with its own due date, default off**; when on, the student's second submission shows the previous comments as a checklist and the returned screen opens with what changed. The teacher's overview is **not a page of its own** but AI Feedback data added to production's **Group Dashboard** (Topic and LO modes) and **Student Dashboard** in Back Office (C10.0). Kindai Applied Sociology's loop — submit → feedback → revise → resubmit [S1 §2.1] — is therefore in scope, per LO.

## C2. Scope — in and out

**In scope:**
- **The rubric** (コメントの観点) is **generated by the LLM from the teacher's uploaded material** (brief, marking criteria) and shown as **one editable block** (LaTeX output rendered as a document), which the teacher edits or regenerates in place — not as tag chips, not with per-criterion source traces. The same generate step produces the basic requirements, each of which carries its source (課題説明 p.1, 評価基準 2.(3)). Past graded submissions are not an input.
- **The review queue** is production's **Course › Submission Grading** page filtered to LO type AI Feedback — no new menu item — with its statuses, filters, bulk action and grading-detail layout. The review screen has approve-and-return, send back, highlight for class, a previous/next pager and a kebab. No confidence routing and no per-item time budget.
- **提出の基本条件 / Basic requirements** — structural conditions generated from the teacher's material, editable, gating the submission, shown as a plain list until a file is chosen or a typed answer confirmed, then checked. **Per-LO switch, on by default;** off, nothing is shown or checked. It is not a self-report: the AI-use declaration and the self-check on resubmission are both out (self-report is not evidence).
- **The formative loop.** Resubmission is a **per-LO setting with its own due date, default off**. Until the due date the student replaces the file, pages or text freely; the teacher reviews only after it. The second submission shows the previous comments as a checklist; the second return opens with what changed.
- **Feedback grounded in course materials** with page/line/slide references [S1 §4]. Each comment card carries a lecture reference; how references are produced is an engine-contract question (C7).
- **Dashboard integration, not a standalone dashboard.** AI Feedback data is added to production's Group Dashboard (Topic and LO modes) and Student Dashboard in Back Office (C10.0).
- **Submission formats**, on PC and mobile: **PDF, Word, Excel (.xlsx) and PowerPoint as they are** (no export-to-PDF step: the Excel-skill criterion is judged on the workbook), **photos of handwritten pages, several per upload kept in page order** (through the AI Grading OCR path before feedback), and a **typed answer** up to 500 characters that the student confirms before the checks run. Which methods an LO accepts is a per-LO setting. *Open: the engine has to read .xlsx/.pptx directly or convert server-side, and page-count style requirements do not apply to a workbook — per-format requirement checks are proposed, not decided.* **[S1 §10] records only PDF reliably working as of 17 Aug** — the gap between this scope and the current build is real.

**Out for this version — KIV:** an instructor-defined rubric with versioning and re-run against past submissions, with a disagreement report. The demand has to be validated first. [S7] names it the strongest competitive gap, but that is one client's brief, not measured demand; revisit when the trial or a second client shows a teacher actually needs to re-run a changed rubric over work already commented on.

**Out of scope:**
- **Graduation theses, seminar theses, specialised open-ended writing** — [S3 ch.5] excludes them: ambiguous criteria, few anchors, high stakes. [S4] slide 18 was cited as selling draft guidance for theses; the claim is not on that slide, so the citation is unverified and [S3]'s exclusion stands unopposed.
- **The oral viva** — not a feature. It is the **client's own workflow**, which our output complements: the instructor holds it, using the submission and the feedback as material. Manabie builds nothing for it.
- **AI Red-Pen Grading (the paper/photo flow)** — an AI Grading capability, outside this PRD entirely. The only thing to carry forward is the naming conflict in C5.
- **The Q3 merge of AI Grading and AI Feedback, and the engine contract that goes with it** — AI Grading PRD. See C7.
- **Rule-checked grading assistance at Correspondence Division scale** (62,000 reports/year, the 13-rule check, the historical-report validation) — AI Grading PRD. It stays in Section 1 as client context because it shapes the account, not this build.

**Two exclusions carried in earlier versions no longer hold.** **Auto-return without instructor confirmation** is not out of scope; it is the off state of a per-LO setting. Teacher review defaults on; a teacher may turn it off for an LO, and feedback then goes out automatically after the due date. [S4]/[S5]'s "administrators confirm responsibility" framing becomes a question of who may flip that switch (Biz, A3). **DOCX** is not out of scope either: [S19] shows v1 already accepts `.docx` and `.pdf`; V1.1's exclusion refers to its mobile/image additions. Word stays in for the web document flow.

**Scoring is not in scope here, and that is the architecture rather than a gap.** **AI Grading and AI Marking are always about scoring; AI Feedback is the feedback engine those two call, and the learner app calls, when additional feedback is warranted on top of a score.** The two scoring products are divided by submission origin, not by scoring method: **AI Grading takes paper and photo submissions; AI Marking takes LMS Assessment LO submissions.** Consequences to hold to throughout this PRD:
- The 11 Sep removal of rubric weights [S15] is **correct and settled** — weights belong to a scoring product, and AI Feedback is not one.
- Kindai Applied Sociology's six-dimension 0–5 rubric [S1 §3] is not a counter-example. The rubric supplies the **criteria** AI Feedback writes against; the **score** stays with Prof. Yasumoto, exactly as [S16] records (*"Any scoring would stay with the teacher"*).
- [S3]'s scoring apparatus — trial grading, QWK agreement, distribution correction, criterion-level scores on the approval card — describes **AI Grading**, not AI Feedback. Do not import it into this PRD's acceptance criteria.
- "Merging into AI Grading" means AI Feedback becomes the **feedback-only mode** of that product [S16 §5], not that it acquires scoring.

**The contract between the scoring products and the feedback engine belongs to the AI Grading PRD.** What AI Grading and AI Marking pass in, what comes back, and the rule that decides when a scored submission also gets feedback are all questions about the merge. What stays here is the LO surface: how a Feedback LO is set up, submitted to, reviewed and reported on.

**Phasing.** [S3]'s inferred rubric → trial grading → approval queue sequence is the scoring product's onboarding and goes with it to the AI Grading PRD. The LO surface ships as one piece: set up, submit, review, return, report.

**This is one feature, not two.** Kindai Applied Sociology's formative feedback that makes students revise is this PRD. Kindai Correspondence's rule-checked grading assistance is the AI Grading PRD's. They were only ever one question because they share an engine; split by PRD, each has a coherent user journey.

## C3. Business logic & behavior rules

The table below is the list of cells that must not be empty. Every row is behaviour the product must have.

| Scenario / State | Expected behavior | Notes / edge cases |
|---|---|---|
| No submission yet / first use of an assignment | The LO's overview under Submission Grading shows Submitted / Waiting for review / Returned at 0 and the LO's settings read-only; the Topic Dashboard lists the LO with its submission window, 0 counts and no insight line; the student's To-do shows the LO once the window opens | The rubric and requirements are already on the LO's Content tab before any submission. The dates shown are the course's |
| Submission in draft (formative) vs final | Until the due date the student can view and **replace** the file, pages or typed text; the basic-requirement checks run on each replacement. Nothing is reviewed or returned before the due date. A further round exists only when resubmission is on for the LO | No "learning support" label: the student sees no draft at all before return |
| Preliminary AI assessment produced, instructor has not approved | The student sees a waiting screen: **no draft, no AI mention, no teacher name, no expected date**, one generic line that they will be notified when returned. The draft is visible only in Back Office, status Not Reviewed / In Review | A3.2 still has to ratify this as policy |
| Instructor approves unchanged | 承認して返却する returns the draft as the teacher's feedback, with the teacher's own note (ひとこと) at the top of the returned screen; status Returned | Zero-diff capture: undefined |
| Instructor edits the draft | There is no score. The teacher **edits or deletes individual comments** in the report and writes the note; an edited comment carries an edited mark | What the diff feeds: undefined |
| Instructor rejects and regenerates | 差し戻す **Sent Back**: the submission goes back to the student for another submission (error tone); regenerating the draft is an action in the review screen's kebab | |
| Instructor flags for interview / viva | Not applicable — the viva is the client's own workflow, not a feature; nothing in the product flags for it | |
| Rubric is edited after submissions have already been commented against | **The teacher may edit the rubric at any time; every generation after the edit uses the edited rubric.** Comments already written are not re-generated and not retro-tagged | No versioning, no re-run, no disagreement report — those are the KIV feature (C2). Worth saying in the UI that the change applies from the next generation on |
| Feature is disabled mid-term with submissions in flight | **No new generations happen.** Work already submitted and already generated is unaffected | Residual: whether a draft already generated but not yet returned can still be returned |
| Model is replaced | **The product is model-agnostic.** There is no score to re-validate, so no re-validation ritual | [S3 ch.6]'s model-agnostic storage schema is the part that still matters technically |
| Student keeps replacing the submission until the checks pass | **No cap.** The student may keep updating until the due date; the basic-requirement checks run on each replacement | [S6]'s 36%-avoidable-resubmission figure is the argument *for* letting them retry, not against |
| **Teacher publishes a whole semester of AI Feedback items at once** | Confirm creates the LO **Unpublished**; **Publish** is a separate action on the LO page or the tree row. A published LO whose start date has not passed **shows its start date on the course tab and is not clickable until that date**. Submission windows come from the **course** (see the due-date row), not from the LO | Notification on start is undefined. A **blank** start date is not addressed: on the rule above it would leave the LO open from publication, so either make the field required or say that blank means open |
| **AI Feedback item passes its start date** | Appears on the To-do with the Feedback type icon, and the LO becomes clickable on the course tab | Notification and ordering against other LO types: undefined |
| **AI Feedback item passes its due date without submission** | To-do shows it overdue in red, and **a late submission is not accepted**. The one way in is for the teacher to **extend the due date**, which is a course-level change (see below) | |
| **Teacher review off for the LO (先生の確認 off)** | The LO's settings show it; feedback is returned automatically after the due date; the row shows a secondary **Auto-returned** chip in Submission Grading and on the Student Dashboard (**not** in the Group Dashboard matrix); the review screen is skipped. Student-facing copy is unchanged | Open: the copy overstates "the teacher gives the feedback" in this case |
| **Resubmission allowed for the LO** | Per-LO toggle, default off. The second submission screen lists the previous comments as a checklist; a returned resubmission opens with what changed; secondary chip **Resubmitted** in the tables; 再提出 1回 sits under the submission date on the Student Dashboard, never in a score column | **Where the resubmission date lives is open**, since the submission window moved to the course |
| **Teacher highlights a submission for the class** | クラスで紹介する / Highlight for class on the review screen, with a **few-word reason**. Effects: ★ before the ID in Submission Grading tables with a Highlighted-only option **inside Filters**; ★ count in the LO header of the Group Dashboard matrix and in the Topic Dashboard's AI Feedback column; the reason under the status in the matrix cell (which opens the submission) and under the LO name on the Student Dashboard; a ★ line in the teacher's note card on the student's returned screen | |
| **Basic-requirements check off for the LO** | Nothing is shown to the student and nothing is checked at submission | |
| **Student types the answer instead of uploading** | Counter to a **500-character limit** under the box; the student **confirms** the text, then the checks run on the confirmed text; Edit reopens the box and clears the checks | The limit is a per-LO value: **Env vs Tenant level not decided** |
| **Teacher tries to change the LO type after creation** | Not possible; the edit dialog shows the type as a locked field | |
| **Due date differs per student or per class** | **Dates belong to the course, not the LO.** A single student's extension is a per-student end date at the study plan's student level, set from the course's Student tab (Extend due date, drawn as a V2 proposal on T7); the course's dates do not move. The **submission start and due date are managed on the Course Management page**; the book is linked to the course; **the course's submission window gates student submissions**. Two courses using the same book therefore run the same assignment on their own dates, which is what "differs per class" needed | Drawn on production's Learning Objectives Availability page (C4, T6–T8): the LO keeps no dates of its own, and the **resubmission** deadline is proposed as a third date column there, shown only when resubmission is on — both to be confirmed. Per-*student* variation remains unsolved |

**Mandatory edge-case checklist:**
- [x] Empty / no-data / first-use state — defined for the teacher's screens; on the student side a published LO before its start date shows the date and is not clickable
- [x] Each status the entity can be in — **teacher-side:** Not Reviewed · In Review · Returned · Sent Back, plus Auto-returned and Resubmitted; **student-side:** not submitted · submitted (waiting) · returned · awaiting resubmission (再提出待ち) · overdue, with a late submission refused. **Failed generation is the one state still unnamed** — see the failure-paths item below
- [ ] Manual override / admin bypass behavior
- [ ] **Error and failure paths — the largest gap in C3.** Generation failure, model timeout, partial extraction, a corrupt or unreadable upload: none is defined, and the student-facing behaviour matters because the student is never told AI is involved
- [x] Concurrency — two staff opening the same draft belongs to the AI Grading PRD
- [ ] **Configurable vs hardcoded — every value listed in A2 needs an explicit Env-level or Tenant-level label.** None has one.

## C4. User journeys — *six exist as the prototype [S20]; one persona still owed*

The journeys below are the boards of the prototype, in the order they link. Each board has a JA and an EN version.

**Teacher — set-up, in Back Office › Book Management (boards T1–T5).** Book tree → **+ Add LO** → the Add Learning Objective dialog with **AI Feedback** as one more LO type: General Info (type, name, external ID, description the student sees) then Settings (resubmission, default off; accepted submission methods with the 500-character limit on typed; teacher review, default on) → **Confirm creates the LO Unpublished and lands on its Content tab**: upload the brief and marking criteria → **Generate requirements and criteria** → the basic requirements as an editable list (each row with its source, add/remove inline, per-LO on/off switch) and the rubric as one editable block → **Publish** (separate action) → the Settings tab shows what the dialog collected, with Edit settings reopening the dialog (type locked). A "View submissions" link jumps to the processing journey. The dialog and the Settings tab carry no dates: the 公開期間と締切 block is a pointer to Course Management, and the Settings tab lists the window per course this book is assigned to, with a link to edit it there.

**Teacher — the submission window, in Back Office › Course › Course Management (boards T6–T8).** Course list (Course Name · Teaching Method · Course Type · Subject; two courses — a Thursday and a Friday class — carry the same statistics book) → the course's detail page on its **Books** tab (the book table; production's per-book availability info alert removed, PM 23 Sep) → the book's **Learning Objectives Availability** page: Chapter · Topic · LO (with its type icon) · **Start Date** · **End Date**, chapter and topic cells merged over their rows, **Edit Date** turning every date cell into an input with Cancel / Save, Import/Export for CSV. The dates are the course's study plan items' start and end (the study plan backend; PM, 24 Sep), so Study Plan Management edits the same values. For an AI Feedback LO the Start Date is when it appears on the student's course tab and To-do, the End Date is the due date (submit and replace until it; the teacher reviews after it; a late submission is refused unless this date is extended here). One column is drawn as a proposal: **Resubmission Due**, shown only for LOs with resubmission on — the place the resubmission date could live now that dates left the LO. This is production's `CourseBookDetail` page, reused as it is; nothing here is new for AI Feedback beyond that column. **Students join the course by QR code**: the AI Tutor class page's existing **Share Access** dialog (`AIClassShare` — the QR code with Download, the class code with Copy, Close) opens from a share icon on each course row (T6) and from the course detail's ⋮ menu beside Edit and Assign Books (T7); a student who scans it or types the code is enrolled and sees the course's LOs from their start dates. The course's **Student** tab (T7, production's `StudentTab`: Student Info with its Action menu, name search and filters, the student table — Student Name · Academic Year · Location · Enrollment Date · Class · School · Study Plan) lists who is in the course; a self-joined student simply shows no class and no study plan until the teacher assigns them. A Joined via column was proposed and dropped (PM, 23 Sep): for AI Feedback nothing depends on how a student got in. **Add course** (T6, production's `DialogUpsertCourse` + `CourseForm`: a full-screen dialog — course icon, Course Name, Location, Teaching Method, Course Type, Subject, Book — Cancel / Save) is where a course is created and its book linked; nothing in it is new for AI Feedback.

**Teacher — processing, in Back Office › Course › Submission Grading (boards T9–T12).** The existing queue filtered to LO type AI Feedback (statuses Not Reviewed / In Review / Returned / Sent Back with counts; Filters incl. Highlighted only; Bulk Action) → the LO's **Overview** (Submitted / Waiting for review / Returned cards, settings read-only naming the course the window belongs to, Edit dates in Course Management, Edit in Book Management) → the LO's **Submissions** tab → the **review screen** on the grading-detail layout: previous/next pager, reviewer and submission info, the teacher's note, the recognised submission beside the draft comments (criterion, passage, comment, edit/delete), actions **Highlight for class** (with reason) · **Send back** · **Approve and return**, kebab (history, download original, regenerate draft, preview the student's screen). With teacher review off this screen is skipped.

**Teacher — dashboards, in Back Office › Dashboard (boards T13–T15).** Group Dashboard, **Topic mode** (production's table + one AI Feedback column: LO with start/due, Submitted / Waiting / Returned counts, ★ count, one tagged insight line ranked by the LLM; Filters with AI Feedback start/due-date ranges) → **LO mode** (student × LO matrix; feedback cells show the status, a highlighted cell shows the reason and opens the submission; score toggle greyed when nothing is scored) → **Student Dashboard** (LO rows with Status, Flagged criteria and a Review/View link). Specified in C10.0.

**Student — PC (boards 1–8).** Course → LO list (Feedback type chip; future weeks dimmed) → assignment: criteria chips, **basic requirements**, submit by file/photos or typed answer → **waiting** (no AI mention, no date; replace until the due date) → **returned**: teacher's note (★ line if highlighted), summary, the submission with numbered underlines beside the comment cards (click either side to centre the other) → **resubmit** with the previous comments as a checklist → waiting → second return opening with what changed → To-do carrying 再提出待ち.

**Student — mobile (boards M1–M10).** LO list → assignment with three paths: **snap** (camera with page guide → crop with auto-fit → pages review) · **file / photos** · **typed** (500 limit, confirm) → the same waiting screen → returned with a **bottom sheet** on a tapped underline. Same rules as PC; the weekly reflection is the mobile exception of C9.1.

**Not yet written:** academic affairs (rubric governance, audit log, consistency report — nothing prototyped, and rubric versioning is KIV). There is no TA journey: two-stage TA-then-instructor review belongs to the AI Grading PRD, so this PRD assumes one reviewer per LO.

**Design status.** No Figma. The prototype is the design reference: it reuses production's Back Office components and layouts (Book Management tree and Add LO dialog, Submission Grading list and grading-detail page, Group and Student Dashboards) and the Learner app Figma for the student side, so the design dependency is on **existing** screens plus the AI Feedback additions. Qisheng Zhang's AI grading US1–US4 Figma (Weekly AI Grading, 17 Sep) — **confirm whether it overlaps the Submission Grading review screen before commissioning more.**

## C5. Terminology / glossary — *PM to complete; several genuine collisions*

| Term | Definition | Replaces / aligns with |
|---|---|---|
| AI Feedback | *TBC* — today used for **both** the student-initiated V1.1 essay feature **and** the shared feedback engine behind grading/marking | Must be disambiguated; the two are conflated in [S1], [S4], [S5] and in the 2 Jul direction meeting |
| AI Grading | *TBC* — internally, the scoring product for **paper and photo** submissions | The decks' client-facing naming does not follow this split — see the row below |
| AI Marking / AI 添削 | *TBC* — internally, the scoring product for **LMS Assessment LO** submissions. But [S5] and [S4] both market **"AI Red-Pen Grading"** as the client-facing name, and 添削 (red-pen) is what a teacher does to *paper* | **Live naming conflict.** The client-facing name points at the paper flow while the internal name points at the LO flow. Align EN / JP / client-facing names before any string is cut or any deck is re-used |
| **AI Feedback LO** / Feedback LO | The LO type, created in Book Management's Add Learning Objective dialog like any other type. **Internal and Back Office name: AI Feedback. Student-facing name: フィードバック / Feedback** — no "AI" anywhere the student reads, because the teacher may endorse the reviewed draft as their own | Aligns with Koki's "everything under the LO structure" (2 Jul) |
| 提出の基本条件 / Basic requirements | Structural conditions a submission must include, generated from the teacher's material, editable, gating submission; per-LO on/off | Replaces "pre-submission self-check" and "提出前チェック"; never "checks form only" or any AI wording |
| コメントの観点 / Rubric criteria | The rubric, generated as one editable block; comments are tagged with the criterion they concern; no levels, no score | The student-facing chips on the assignment screen |
| 先生の確認 / Teacher review | The per-LO switch, default on, that routes drafts through Submission Grading | "Teacher in the loop" in meeting notes |
| Submission statuses | 未確認 Not Reviewed · 確認中 In Review · 返却済み Returned · 差し戻し Sent Back, in production's marking tones; secondary chips 自動返却 Auto-returned · 再提出 Resubmitted | Production's Submission Grading status vocabulary |
| クラスで紹介する / Highlight for class | The teacher marks a returned submission as an example for the class with a few-word reason; ★ in tables, cells and the student's note card | Not a score, not a ranking |
| インサイト / Insight (Topic Dashboard) | One tagged line per feedback LO — Missed · Going well · Worth showing · Submissions — read by an LLM pass over the submissions and their draft feedback along the rubric, the top-priority one shown | Replaces "what the class missed" as the only kind |
| Preliminary AI assessment | [S3]'s term for the pre-approval output | Deliberately **not** "grade" |
| Anchor | Past graded submission used to calibrate [S3] | |
| Approval queue / approval card | [S3] | |
| Voice model | Extracted instructor tone/length/critique patterns [S3] | |
| Attention audit | Injected known-incorrect items to measure instructor vigilance [S3] | |
| Formative mode | Draft feedback before the deadline [S3] | |
| Rubric lifecycle | Conversational elicitation → versioning → re-run with disagreement report [S7] | |
| Consistency report | Course/department-level drift and agreement report [S3] | |
| Credibility Protocol (M2) / M1 / M5 | Referenced by [S3] as moats from a prior paper **not supplied with this request** | Obtain "Differentiation and Moat Strategy for AI Feedback" (10 Sep 2026) before using these terms |

## C6. Acceptance criteria — *none written*

Cannot be written before C2 and C3. QA builds the test plan directly from this section; writing ACs against undefined business logic produces the wrong test plan.

**One observation to carry into the ACs when they are written:** [S6] found most AI/instructor disagreement was caused by *instructor* inconsistency, not AI error. Any AC of the form "*then the AI score matches the instructor's historical score*" will therefore fail for reasons that are not defects. [S7] proposes measuring **instructor agreement with the AI's presented evidence**, the number of ambiguous "Review" verdicts, and time per report instead. Decide this before QA writes anything.

## C7. Integration & technical specs — *still thin*

**The engine contract is the AI Grading PRD's.** What AI Grading and AI Marking pass into the feedback engine, what comes back, the rule that decides when a scored submission also gets feedback, and the engine's ownership and compatibility policy all describe the Q3 merge, and this PRD is the Q4 LO integration. Nothing in this PRD should be read as having specified that contract.

What remains this PRD's own, and is still undefined:

- **Systems involved:** Manabie LMS (LO submission flow, book/chapter/topic/LO, study plan); learner app (To-do, submission, result display); Back Office (Book Management LO set-up, Submission Grading, Group and Student Dashboards); the AI Grading OCR path, which multi-page photo submissions pass through before feedback; university LMS integration via **LTI 1.3** as proposed in [S3 ch.9] — **not** required by the Kindai Applied Sociology trial, which runs in the Manabie tenant. *(KULeD's API ingest and write-back requirement [S7] belongs with the Correspondence track, in the AI Grading PRD.)*
- **Learner app integration points** — the three named in the AI Marking Weekly discussion (Trieu Le Hong / Ming Yew Lee): **(1)** teacher/student registration and class association, **(2)** how the student accesses the assignment on the learner app, **(3)** how the returned result and feedback are displayed back to the student. *All three are undefined for this scope.* Trieu's position on ownership: the LMS team owns the API and everything behind it; consumers integrate at the API level only.
- **The To-do date layer.** AI Feedback is a distinct **LO type** with its own To-do icon, and the To-do needs a due-date layer built on top of existing LO functions [S8a]. **That layer lives on the course:** submission start and due dates are managed in Course Management, the book is linked to the course, and the course's window gates submissions and drives the To-do. **The dates are the study plan's (PM, 24 Sep):** the Start and End Date on the Learning Objectives Availability page are the course's study plan items' `available_from` / `available_to`, read from and written to the study plan backend, not a separate availability table; Study Plan Management edits the same rows, and the student's course tab, To-do and the dashboards read the same dates. Open: whether the LO keeps dates at all, where the resubmission date lives, how this interacts with study plan, and **per-student variation, which is still unsolved**. **Bunsuke owes a proposal on LO type refactoring; Koki owes a demo of start/due-date behaviour**, built against course-level dates.
- **Web/PC path.** University students submit from PC, not phone [S8a], which means PDF/file upload on web is a first-class path for AI Feedback, not a fallback.
- **Data flow:** *undefined*
- **Auth / token behavior:** *undefined* for the university case. Asymmetric JWT exists for the Onigroup webview; SSO is a Tier-1 assumption in [S3].
- **State fields:** submission_status, assessment_status, approval_status, rubric_version — *none defined*
- **Feature control level: Tenant-level — already built.** [S19] specifies a tenant-level feature flag: enable/disable per tenant, upload entry point hidden when disabled, existing documents stay visible but new uploads blocked. **This matches A2's candidate (tenant-configurable) and needs no new decision** — confirm the existing flag covers the new surfaces rather than inventing a second one.
- **Feature flag:** see E2 — **flag naming and registry are Carlo's; ask, do not invent.**

## C8. Non-functional requirements & feasibility — *TL validation required, none obtained*

Flag every one of these to the Tech Lead **before** commitment:
- **Latency — there IS a stated position, and it conflicts with the reflection use case.** [S19] excludes latency from v1's metrics outright: *"it can take 3-5min, it doesn't matter for this"* — reasonable for a student uploading one report on the web. **It is not reasonable for 140 reflections expecting feedback "immediately on submission"** [S16 §2] in a burst after a lecture. Either the reflection path needs its own latency budget or the professor's expectation needs resetting. Decide which before the showcase implies the former.
- **Latency, the rest.** No budget stated for the approval-queue path. For comparison, the AI Tutor pipeline runs ~62,000 input tokens per question and diagram generation was 2–3 minutes on easy problems (AI Tutor calls, 17 Sep). A 30-second approval card is worthless if generation takes minutes.
- **Volume — Kindai trial, now sizeable (confirmed 17 Sep).** Both submission types run weekly (C10.3): ~140 students × **2 submissions/week** × 7–9 remaining sessions ≈ **2,000–2,500 feedback generations** across the three-month trial, arriving in **bursts of ~140 within hours of each lecture**. The reflection half is expected *"immediately on submission"* [S16 §2], i.e. synchronous. **Nobody has sized the burst, the latency budget or the cost.** This is the volume that binds this PRD.
- **Volume — correspondence track** (62,000 reports/year, the 240-report batch re-run, corpus re-grading on a rubric version change) — AI Grading PRD. Rubric versioning is KIV here (C2), so no corpus re-run is in this scope.
- **Cost per submission.** Not calculated for the Kindai trial's ~2,000–2,500 generations plus one insight-line call per feedback LO per refresh. [S7] notes the client prefers per-student flat pricing, which puts all volume risk on Manabie. The API-vs-subscription cost gap is live in the org (~$5,000 per 70 questions on API vs $20/month subscription — Daily AI Tutor x AI Harness, 17 Sep).
- **OCR.** V1.1 sets ≥97%; Eishinkan measured 93% average with 70% of samples ≥95% (Weekly AI Grading, 17 Sep). **Reconcile the target with the measurement.** The bar belongs to the AI Grading path, but it reaches this PRD through one door: the student's multi-page photo submission runs through that path before feedback (C2).
- **Evaluation at scale.** James, 17 Sep: for a signed client launching in April, evaluation has to be ≥95% automated up front. What is the evaluation harness for feedback quality, and who owns it?
- **The 30-minute setup and 30-second approval budgets [S3] have never been validated by anyone who would have to build them.**

## C9. Localization & design

- [ ] All user-facing strings have confirmed translations — **every prototyped string exists in JA and EN** [S20]; **not yet confirmed by a translator**, and production labels (Submission Grading, Dashboard) were kept as production has them. Feedback itself is generated in Japanese (400–600 JP characters for Kindai [S1]); AI Tutor Product Catchup (12 May) required both Japanese and English base prompts.
- [x] JP / long-text overflow checked — **checked in the prototype at 1280 (student PC), 375 (student mobile) and 1440 (Back Office)** for every board, JA and EN, including the 400–600-character feedback beside the recognised submission and the bottom sheet on mobile. Real generated text may still overflow: re-check on the first real drafts.
- [x] Design exists and is linked for every flow in C4 — **the clickable prototype [S20] covers the four teacher journeys and both student journeys**, the course-level submission window included; no Figma. TA and academic-affairs flows have no design because they have no journey (C4). The Duolingo-style visual direction is a separate track owned by JPE and is not reflected.
### C9.1 Device priority for the university segment — *decided*

**The Kindai / university AI Feedback flow is PC-first, with mobile kept at genuine parity — not PC-only — and one named exception.** The reasoning and the one assumption it rests on are set out below so it can be overturned on evidence rather than re-argued.

Per surface:

| Surface | Priority | Why |
|---|---|---|
| **Faculty: rubric creation, distribution, review, dashboard** | **PC only, in practice** | Nobody works an approval queue at 30 s/item, or reads a consistency report, on a phone. Back Office is already desktop |
| **Student: coursework submission** (Excel workbooks, PowerPoint deliverables, reports) | **PC-first** | The artefact is *authored* on a PC and the submission path is an **export step** — PowerPoint → PDF [S16]. The device that made the file is the device that should submit it |
| **Student: reading feedback and deciding what to change** | **Both, genuinely** | Reading 400–600 JP characters of criterion-linked feedback is fine on a phone and often *better* — students read between classes. Acting on it is not |
| **Student: revising and resubmitting** | **PC-first** | You cannot rework a regression chart or a slide deck on a phone |
| **Student: weekly 300-character reflections** (the showcase use case) | **Mobile must work — this is the exception** | See below |
| **AI Tutor snap (sold alongside)** | **Mobile-first, unchanged** | Photographing a problem is a phone action. Kindai buys both products; each should play to its device |

**The evidence for PC-first is about the artefact, not the user.** Kindai's course is Excel exercises (AVERAGEIF, CORREL, T.TEST), analytical outputs and a final PowerPoint product proposal [S1 §2.1, §4]. [S16] confirms there is **no direct PowerPoint or document upload** — students export to PDF. James on 17 Sep: *"red pen is more for elementary, junior high… not for Kindai. Kindai is, I think most of the submissions gonna be PDF."* [S3 ch.9] lists PDF, Word and text as the accepted inputs. Every one of those is a desktop artefact. This holds for the Correspondence Division too — written reports, and a learner population [S8b] describes as *"past 22 years old… some of them can be in their 40s or 50s."*

**The exception, and why it matters more than it looks.** The showcase use case Hinano confirmed is **weekly class reflections** — ~300 characters, every lecture, 150–300 students [S16 §2, S18]. That is a phone-shaped interaction: written in or just after class, short enough to thumb-type. **If a weekly reflection requires opening a laptop, submission rate falls — and submission rate is the trial's first-order risk**, since a formative-feedback product with no submissions has nothing to demonstrate and the dashboard has nothing to show. Mobile submission for short free-text is therefore not "parity", it is a requirement of the use case that C10 depends on.

**What this actually costs.** Less than "PC-first" sounds. V1.1 already promises desktop *functional* parity; what it does not promise is desktop *design*. Koki named the real gap on 17 Sep — *"current PC version very weird because you have PC but you have like a smartphone style"* — a stretched phone layout, plus the missing web upload path (*"you can take a screenshot and then you put it here… or you can just upload your local file"*). So the work is: **(1)** file/PDF upload on web, **(2)** a desktop layout for the feedback-reading view that uses the width instead of centring a phone column, **(3)** keep the existing mobile submission path intact for short text and photos. It is not a rebuild and it does not invert the whole product — it inverts it **for this segment's document flow only**.

**The assumption this rests on, and how to falsify it.** The strongest statement in the sources — Koki's *"most of the university student they use PC, they never use smartphone to upload"* — is an assertion, not a measurement, and "never" is doing a lot of work. The artefact argument above stands independently of it, which is why the decision holds either way. But the exception does depend on the opposite being true for short reflections. **Cheapest check: ask Prof. Yasumoto how last year's cohort submitted the lecture-10 and lecture-16 exercises, and whether minute papers today are paper, LMS or phone.** One question to Hinano, and it settles both halves. If it comes back "students do everything on their phones", the reflection exception widens; it does not overturn PC-first for the PowerPoint and Excel deliverables.

**Corroborated by the v1 PRD.** [S19] states outright that *"AI Feedback v1 is a **web-only** feature designed for the common assignment workflow"*, with `.docx` and `.pdf` upload from the student's computer. So PC-first is not an inversion of the product for the document flow — it is what v1 already is. What inverts is only the mobile-first framing introduced by V1.1's additions.

**Kindai runs both submission types weekly** (C10.3), which is exactly the split this decision assumes: the reflection is the phone path, the exercise is the PC path. The mobile exception is therefore load-bearing rather than defensive.

**Consequences for the rest of the PRD:** C4 needs a desktop journey for the faculty flows and the student coursework flow, and a mobile journey for reflections and feedback-reading. The JP long-string overflow check above must be run at **both** widths. And the design brief for this segment is no longer the V1.1 mobile-first brief — say so when commissioning it.
- Terminology to align JP↔EN before strings are cut: 添削 (marking/red-pen) vs feedback vs grading; ルーブリック; 仮評価 (preliminary AI assessment). **See the naming conflict in C5 — this is now a live item, not a tidy-up.**

## C10. Learning-log dashboard — the Kindai showcase

> **This is a separate deliverable from the product build above, and it should stay separate.** It is a **manually produced artefact for sales and trials**, explicitly *not* a Back Office feature [S16 §4, S18]. Do not let it acquire engineering scope by sitting in the same PRD — its purpose is to discover which views teachers value so that *those* become backlog items.

### C10.0 The in-product dashboard — *decided*

> This subsection does not cancel C10.1–C10.7, which describe Hinano's manual showcase for Kindai on its own clock. It gives that showcase a target, because what is shown manually should be what the product will show.

**The AI Feedback overview is not a page of its own.** It is AI Feedback data added to production's **Group Dashboard** and **Student Dashboard** in Back Office, in their existing layouts (prototyped as boards T10–T12 [S20]):

- **Group Dashboard, Topic mode** (production's default, where the Dashboard menu lands): production's chapter / topic / average score / completion table, with **one added column, AI Feedback**: the topic's feedback LO (link to its overview), its **start and due dates**, **Submitted n/N · Waiting for review n (link into the LO's submissions) · Returned n**, the **★ count** of submissions highlighted for the class, and **one insight line** — a tagged sentence of one of four kinds (見落とし Missed · 良い傾向 Going well · 紹介候補 Worth showing · 提出状況 Submissions), produced by an LLM pass over that LO's **submissions and their generated draft feedback along the rubric**, ranked by the LLM with the top-priority one shown. It exists before anything is returned, refreshes itself when a submission or draft changes (no Regenerate control), is teacher-facing only, and carries **no expansion, quotes or counts behind it**: the teacher checks the submissions themself, and the line only has to alert them. **Filters** opens production's panel (Enrollment status, Duration) plus **AI Feedback start-date and due-date ranges**, shown as applied chips. Search reads "Search by Chapter Name or Topic Name". Every topic of the book is listed, as production does (the board shows only the three with a feedback LO, for the demo).
- **Group Dashboard, LO mode:** the student × LO matrix **alone**. A feedback LO's header reads Submitted / Waiting / Returned and its ★ count instead of score and completion; each cell is the submission status in the marking tones with a Resubmitted chip where relevant (no Auto-returned chip here, no comment count); a **highlighted cell shows the teacher's few-word reason under the status and opens that submission**; Highlighted-only narrows the matrix; the Latest / Highest Score toggle keeps production's labels and is greyed out when nothing in view carries a score. **Nothing above or below the matrix:** overview blocks (not submitted, waiting on you, acted on the feedback, comments by criterion, requirements that stopped a submission, count tiles, average time to return) duplicate the matrix and Submission Grading and are not required.
- **Student Dashboard:** production's chapter / topic table with the LO rows expanded; a feedback LO shows **--** in both score columns and gains three columns shared by all LO rows — **Status** (the chip, its secondary chip, the date it was reached; Completed for unscored LOs also lives here, never in a score column), **Flagged criteria** (the rubric criteria that drew an improvement comment, marked when the resubmission fixed them), and a **Review / View** link (Review while In Review, View once Returned). The LO name links to its overview, with the ★ reason under it; 再提出 1回 sits under the submission date.

**Rules carried from §1.6.4 and kept:** counts and names, never rates; no per-student score or ranking for a feedback LO (the score columns stay empty, the score toggle greys out); no chat transcripts (nothing conversational exists in this flow). **Dependency carried from §1.6.5:** the insight line and the flagged-criteria column both group by rubric criterion, so **criterion keys must be fixed per assignment** (U22).

**How this relates to C10.1–C10.7.** The reading-queue thinking in C10.3a feeds the insight line (the "worth showing" kind is the queue's purpose; "missed" is job B), but not as a ranked list of submissions: it is one line per LO, with the teacher going to the submissions themself. The revision trail (C10.3's exercise view) survives as the Student Dashboard's flagged-criteria column and the student's own "what changed" screen; no own-words / copied classification is shown to the teacher. U17 / U25 (who owns the dashboard) remain open.

### C10.1 What is actually being asked for — *confirmed*

Hinano needs a dashboard she can put in front of Kindai, aligned on **final visuals and content this month** [S18], for **weekly class submissions in 地域環境統計学** — i.e. the minute-paper / weekly-reflection use case, ~300-character reflections, 150–300 students, feedback immediately on submission, plus *"a way to pick out the comments worth reading"* [S16 §2].

### C10.2 Constraints inherited from the prototype — *PM to ratify, not re-derive*

The design rules in §1.6.4 are the one part of this work that is already decided and reasoned. **Ratify them as written or overturn them explicitly** — they should not be quietly relaxed while "simplifying". The two most load-bearing for a client showcase:
- **Never show chat transcripts.** This is a deliberate differentiator against Turnitin Clarity, not a gap, and it will be the thing a client asks about.
- **No per-student score and no leaderboard.** This dashboard produces *evidence for a teacher's judgement*. It also keeps the artefact consistent with the architecture: scoring belongs to AI Grading and AI Marking, and this dashboard reports on the feedback engine.

### C10.3 Two kinds of weekly submission, two views — *decided*

> Kindai's "weekly class submission" is **both** the short written reflection **and** the Excel/statistics exercise output, so the dashboard carries two views.

**Kindai students submit two different things each week, and they behave differently.** Trying to show both in one view is what would make the dashboard unreadable.

| | **Weekly reflection** | **Weekly exercise** |
|---|---|---|
| What the student submits | ~300 characters of written reflection [S16 §2] | Excel workbook / analytical output / slides, exported to **PDF** [S16] |
| Where from | Phone, in or just after class — the C9.1 mobile exception | PC, where the file was made |
| Revision | **Expected to be one-shot.** The professor wants feedback on submission and *"a way to pick out the comments worth reading"* [S16 §2] — no revision loop is described | **Revision is the point.** Submit → feedback → revise → resubmit is the loop Kindai signed up for [S1 §2.1] |
| Rubric | The course's six 0–5 dimensions **do not fit** — "Excel skills" and "visual clarity" are meaningless on a reflection. **Needs its own small rubric, 2–3 criteria** | The six-dimension course rubric applies as written [S1 §3] |
| What the professor needs | Triage: which criteria the class missed this week, and which of ~140 reflections are worth his time | Progress: did this student act on the feedback, and in whose words |

**So the dashboard carries two views, not one.**

**Exercise view — the revision trail.** This is what the existing prototype already does well and what it was built for: one piece of work across several drafts, showing whether the student fixed the flagged problem and whether they used their own words. Keep it, aimed at the exercises.

**Reflection view — a reading queue.** New, and the view the showcase is actually being asked for. Specified below.

#### C10.3a The reflection view — what the professor asked for

> **Provenance.** *"A way to pick out the comments worth reading"* is Prof. Yasumoto's own request [S16 §2], and **"the comments" means the students' reflections** — not the AI's feedback awaiting approval. *"Who has submitted"* and *"which rubric criteria students miss most"* are from John's menu of candidate contents [S16 §4]. **The triage signals in the table below are inferred, not sourced**, and they are the part to test with him in October.

**The problem in one line:** 140 reflections land within hours of each lecture, and the professor has minutes. He is not going to read them all, and a list of 140 rows helps him no more than the pile does.

**Three distinct jobs, deliberately not blurred into one view.** "Who submitted" and "what the class missed" do not answer "what should I read" — the first is compliance, the second is an aggregate that by construction averages away the individual reflection.

| Job | What it answers | Shape | Size on screen |
|---|---|---|---|
| **A. The reading queue** — *the actual ask* | Which reflections deserve my attention this week | A short ranked list of **submissions**, each with the reason it surfaced | The main event. **Target 5–10 items out of ~140** |
| **B. What to re-teach** | What did the class as a whole get wrong | One sentence plus the criteria the class missed most | One line. Feeds the five-minute recap at the start of the next lecture |
| **C. Who submitted** | Who do I chase | A count and a list of names | Smallest element. Counts and names, never rates (§1.6.4) |

**Candidate signals for the queue — each must state why it surfaced:**

| Signal | Why it earns the professor's time | Confidence |
|---|---|---|
| **The student asked a question** in their reflection | A direct request for his attention, already written down. Cheapest and least arguable signal there is | High — trivially computable |
| **Said something no-one else said** | The insight worth reading aloud next class. This is what professors actually mine minute papers for | Medium — needs semantic novelty across the week's cohort; untested |
| **Shows a misunderstanding, split by how many share it** | Shared → job B, re-teach it. **Unique → this student, now.** The split is what makes it actionable rather than interesting | Medium — depends on the reflection rubric existing |
| **Changed direction** — steady for weeks, suddenly confused or disengaged | The one thing reading all 140 in a sitting would *not* reveal. **Only the weekly cadence makes it computable** — the exercise view cannot do this at two submissions a term | Medium — needs ≥3–4 weeks of history before it says anything |

**Design rules this must respect (§1.6.4), and how:**
- **The queue ranks submissions, not students.** That keeps it clear of *"no leaderboards, no per-student score."* A teacher's work queue is not a ranking of people, and students never see it.
- **Reading all 140 stays one click away.** The queue is a suggestion, not a gate.
- **Showing the reflection text is fine** — it is the student's own submitted work, not a chat transcript. The rule against transcripts still binds anything from the follow-up conversation.
- **「一度きり」/「未提出」, never "not trying."** Job C names who hasn't submitted and stops there.

**The failure mode to design against.** If the professor reads the five surfaced items in week one and they are dull, he stops opening the view by week three. Two mitigations: **every item says why it surfaced**, so he can calibrate rather than guess; and he can **mark an item read or irrelevant**, which is both a courtesy and the only honest way to learn whether the triage works. That feedback is also the answer to C10.6's open question about capturing teacher reactions — for this view, it is built in rather than bolted on.

**What is still missing before this can be designed:** the reflection rubric (see above — Prof. Yasumoto's to author). Signals 2, 3 and 4 all depend on it or on having several weeks of history, so **the week-one version of this view is realistically signal 1 plus jobs B and C.** Say that out loud in the showcase rather than demonstrating a maturity the trial will not have in its first fortnight.

**Two consequences that are easy to miss:**
- **The "copied the AI's wording" signal only belongs in the exercise view.** On 300 characters there is too little text for it to mean anything, and running it there would produce noise and, worse, unfair 要確認 flags. Scope it to exercises explicitly.
- **Someone has to write the reflection rubric.** It does not exist, it is not the course rubric, and it is Prof. Yasumoto's to author. **Nobody has asked him.** That is a dependency on the October hands-on, not a design task.

**On the demo data.** The prototype ships with an invented middle-school class (25 students, English and Science essays) whose stories were written to show off multi-draft revision. That data fits the *exercise* view and not the reflection view, and it is the wrong level and scale for either. Rebuilding it as a Kindai class — ~140 students, 地域環境統計学, both submission types — is the mechanical part of the work; the reflection view's design is the real part.

**One thing worth raising with Hinano, not re-deciding here:** last year students submitted exercises at **lecture 10 and lecture 16 only** [S16]. Weekly exercises is a step up in what the professor himself has to review, even with AI doing the first pass. Worth confirming he has planned for that rather than discovering it in week two.

### C10.4 Candidate contents — *a menu, per [S16], not a spec*

**For the reflection view, C10.3a supersedes this menu** — the menu's items map onto jobs B and C there, with the reading queue as job A. The menu still stands as the candidate list for the exercise view. [S16 §4] names the natural contents to test with the professors: **who has submitted**, **feedback rounds per student**, **which rubric criteria students miss most**, and **a per-student view of each submission and the feedback it received** — framed around the improvement process from first submission through feedback to resubmission. Plus the rule carried over from the RISO AI Dashboard PRD: **report learning rather than engagement, and make every number traceable to the underlying submission.**

The prototype's own backlog of unbuilt items, in John's priority order [S17 §6]:

| # | Item | Note |
|---|---|---|
| 1 | **Simplify the visuals and surface the meaning** | *"a design problem, not a data problem"* — see C10.5 |
| 2 | Reflection prompt at submission | *"cheap, and the strongest evidence for 観点別評価"* — **but 観点別評価 is K-12; see §1.6.6. Re-justify for a university** |
| 3 | Map the summary onto 粘り強さ / 自己調整 + printable evidence sheet | Same caveat — this is a **Juku/school** play, not a Kindai one |
| 4 | Assignment-level AI policy tier | Aligns with AIAS / Missouri scales |
| 5 | Feedback issued vs. acted on | |
| 6 | Term view | |
| 7 | Time between feedback and return | |

### C10.5 The actual outstanding work — *design, and it has explicit targets*

[S17] is unusually clear that engineering is not the blocker: *"The data layer is solid and the structure is right, but the visuals still need simplifying and the meaningful insights need surfacing — a teacher should get the point without studying the screen."* Its targets, in payoff order:
- **Say the finding, don't just plot it.** The chart has four series and a legend; what a teacher needs is one sentence — *"9 of the 10 students who revised did it in their own words"* — with the chart as supporting evidence.
- **Give each student a one-line "so what".** Today the header shows three numbers and a focus line; the teacher still has to assemble "4 drafts + own words + still open" into a judgement.
- **Thin the timeline rows.** 提案どおり / 自分の言葉 / 質問4往復 / 意見・提案 is four pieces of metadata on one line; some belongs in the expanded detail.
- **Reduce the colour vocabulary** if possible without losing meaning — five is already at the limit.
- Guiding principle to keep applying: **colour and number carry the meaning; prose appears only on demand.**
- Benchmark to design against: *"A busy 塾 teacher should learn something true in about three seconds, without reading a legend or comparing bars."* **For the Kindai showcase, substitute the professor — and confirm that is the same bar.**

### C10.6 Open questions the showcase cannot ship without

1. **Who produces each manual dashboard, from what, at what cadence, and how long does one take?** "Manual" is a commitment to recurring human effort across a three-month trial with weekly submissions. Nobody has costed it. [S16] leaves it as a checklist item: *"agree how the manually created dashboards get produced during the trial."*
2. **What is genuinely collectable during the Kindai trial?** U22 — the four preconditions in §1.6.5 are unmet in production today. A showcase built on fixtures that production cannot reproduce sells something we cannot deliver.
3. **How do teacher reactions get captured?** This is the entire stated purpose of the exercise. For the reflection view C10.3a builds it in — mark-as-read / mark-as-irrelevant on each queued item is the cheapest honest signal of whether the triage works. **For every other view there is still no mechanism**, and without one the trial produces a nice PDF and no roadmap input.
4. **Are `rewrite_quality()` and `student_turns()` trustworthy on real Japanese university text?** Both are flagged as tuned on authored data only. If the showcase asserts "own words vs. copied" to a professor, that claim must survive his own reading of the submissions.
5. **Does the showcase claim anything the trial will not deliver?** Everything in the dashboard is fictional [S17 §11]. Confirm with Hinano how it is labelled to the client.
6. **Does it stay manual for the whole trial, or is there a trigger to productise?** U25 — dashboard ownership currently sits with the AI Grading team, and Takuya's position is that anything built now is rebuilt on merge.

### C10.7 Acceptance criteria — *none written*

The showcase is a document, not a build, so ACs in the QA sense may not apply. What does need writing is a **content sign-off checklist with Hinano before it goes to a client**: every number traceable to a submission, nothing claimed that production cannot collect, fictional data clearly labelled, and no view that breaks a §1.6.4 rule.

## C11. Prototype review — the PM's decisions, consolidated (18–21 Sep 2026)

> A clickable prototype of the whole flow [S20] — student PC, student mobile, Back Office — was built from 18 Sep and reviewed by the PM screen by screen through **91 comment threads** on the canvas. This section is the record of the decisions taken there, dated and grouped by screen. They are Part C decisions: they can be overturned on evidence, not re-argued. Defaults the prototype embodies that the PM has not ruled on are listed separately in C11.7 for ratification.
>
> **Reading the dates.** 18 Sep — student PC flow. 19 Sep — student naming and upload rules, mobile, Back Office set-up. 20 Sep — Back Office refinements, Submission Grading, review screen, Group Dashboard. 21 Sep — Student Dashboard columns.

### C11.1 Student — PC and mobile (18–19 Sep)

| # | Date | Decision (PM) | What it changed | PRD effect |
|---|---|---|---|---|
| S1 | 18 Sep | **No AI wording anywhere the student reads.** To the student, the teacher gives the feedback: no "the teacher reviews the AI comments", no review-step framing, no teacher's name | Waiting and returned screens, To-do, LO chip, titles | C1, C5 |
| S2 | 18 Sep | Waiting screen carries **one generic line** — you will be notified when it is returned. No teacher-set expected-return date: the student does not need it | Waiting screens, PC and mobile | C3 |
| S3 | 18 Sep | **The student can view and replace the submission until the due date.** The teacher reviews only after the due date and never returns before it, so no "this restarts the review" wording | Waiting screens; "view submission" | C3 |
| S4 | 18 Sep | **No chat or message channel.** The learner app's Message tab is not a default client feature; "message the teacher" and "ask the teacher" buttons removed. The resubmission is the channel | Waiting and returned screens | C4, C7 |
| S5 | 18 Sep | Returned screen: file page count and the "comment numbers match the underlines" hint removed — the UI should be intuitive | Returned screens | — |
| S6 | 18 Sep | Clicking an underlined passage **highlights the matching card and centres it**; and the reverse | Returned screens (PC) | C4 |
| S7 | 18 Sep | On mobile, tapping an underline **opens a bottom sheet** with that point's card | Mobile returned screen (built 19 Sep) | C4 |
| S8 | 18 Sep | **One layout for every feedback type** — file or typed reflection, long or short. Content varies, structure does not | Returned screens | C4, C9.1 |
| S9 | 18 Sep | **No AI-written "next step" card.** Prescribing what to do next is the teacher's control of the class flow; guidance stays inside each improvement comment and in the teacher's note | Returned screens | C3 |
| S10 | 18 Sep | Pre-submission checks are the **基本条件 / Basic requirements** for the submission — no AI mention, no "checks form only", no "checked automatically" hint (the checks appear on choosing a file) | Submit and resubmit screens | C2, C5 |
| S11 | 18 Sep | **No AI-use declaration; no self-check on resubmission** — self-report is not evidence. The 生成AIリテラシー criterion stays the professor's to judge. What remains on the second return is the system's own observation that flagged passages were rewritten, positive case only | Submit and resubmit screens | C2, C3 |
| S12 | 18 Sep | "Your teacher grades. The AI does not give a score." line removed from the submit screen | Submit screen | — |
| S13 | 18 Sep | **Photos of handwritten papers accepted**, several per upload, kept in page order; they go through the AI Grading OCR path before feedback | Submit screens, PC; mobile snap flow | C1, C2, C7 |
| S14 | 18 Sep | **Typed input** for weekly reflections. Shown as a **limit of 500 characters** under the box (no target line); the student **confirms the typed answer** so it can be evaluated against the basic requirements; edit reopens it. Which modes an LO accepts is a Back Office setting | Submit screens; M7 | C2, C3 |
| S15 | 18 Sep | **The AI Feedback assignment is created at the LO level** in the LMS hierarchy Book → Chapter → Topic → LO [S21]; **a new LO type for AI Feedback** | Course screen; all of Back Office | C1 |
| S16 | 19 Sep | Course-level "AI Feedback enabled" chip **not required** — the LO type chip already says it | Course screen | — |
| S17 | 19 Sep | **Excel and PowerPoint accepted directly**, not exported to PDF; **multiple images per upload** | Submit screens, mobile file/photos | C2, C7, C11.9 |
| S18 | 19 Sep | **Student-facing name has no "AI"**: the LO type reads フィードバック / Feedback, as do titles and To-do rows, because by configuration the teacher may review the generated feedback and return it as their own endorsed feedback. AI Feedback stays the internal / Back Office name | All student screens | C1, C5, C11.9 |
| S19 | 19 Sep | The "your answer is never written for you" boundary line removed from the submit screen — belongs in the teacher's brief and this PRD, not on the student's screen | Submit screens | — |
| S20 | 19 Sep | Mobile screens for **choose file / photos** and **typed answer** added, converging on the same waiting screen | M6, M7 | C4 |

### C11.2 Student — earlier defaults left standing (18 Sep)

Rules the prototype carried from the start and the review left standing: the six Kindai criteria as chips on the assignment screen; each comment card tagged with its criterion, no level or number; the teacher's note at the top of the returned screen; PDF export of the comments; the To-do carrying 再提出待ち between return and resubmission with overdue in red and future items dimmed until their start date.

### C11.3 Back Office — set-up in Book Management (19–20 Sep)

| # | Date | Decision (PM) | What it changed | PRD effect |
|---|---|---|---|---|
| B1 | 19 Sep | **Book Management is for setting up LOs only; it does not process student submissions.** Overview, Submissions and Review moved to the Course menu — first as a new Course › AI Feedback item, then (same day, PM) **reuse the existing To Review / Submission Grading entry, no new menu item** | T6–T9; nav | C1, C2, C4 |
| B2 | 19 Sep | **After Confirm, land directly on the LO's content page** (material, requirements, rubric), not back in the tree — for this type the next thing the teacher does is upload the material | T3 | C4 |
| B3 | 19 Sep | Teacher review **off** shows a **neutral info notice**, not a red warning; no hint under the on state | T2 dialog | — |
| B4 | 19 Sep | The generate button names its outputs: **Generate requirements and criteria** | T3 | C5 |
| B5 | 19 Sep | **The rubric is generated by the LLM and output as LaTeX; shown as one block, not tags.** The "Generated by AI · LaTeX" label removed. Actions: Regenerate, Edit in place | T3 | C2, C3, C11.9 |
| B6 | 19 Sep | Rubric helper copy explains what the criteria do, shortened, without "no levels, no score": *Each submission is read against these criteria, and every comment is tagged with the one it concerns* | T3 | C5 |
| B7 | 19 Sep | **The teacher can turn the basic-requirements check on or off** per LO; off, nothing is shown or checked | T3 | C3 |
| B8 | 19 Sep | **Add-a-requirement UX**: inline row, disabled Add until text, an "Added by you" source chip on the teacher's own rows, any row removable | T3 | — |
| B9 | 20 Sep | **Publish must work**: Unpublished → Published with a snackbar. Publishing stays a separate action from creation | T3, T4 | C3 |
| B10 | 20 Sep | **Add the Settings tab**: what the dialog collected, read-only, with Edit settings reopening the dialog prefilled (production's pattern). Content — material, requirements, rubric — stays on the Content tab | T4 (new board) | C4 |
| B11 | 20 Sep | **After creating an LO, the LO type cannot be edited** — the edit dialog shows it locked | T4 edit dialog | C3 |
| B12 | 20 Sep | Production's **Invalid Markers export removed** from the Submission Grading board: nothing to do with AI Feedback (production has it) | T6 | — |
| B13 | 20 Sep | LO overview page: the **requirements / criteria count rows are not useful** here; the header's Edit in Book Management and ⋮ removed (the card's button is the one way back) | T7 | — |

### C11.4 Back Office — Submission Grading and the review screen (20 Sep)

| # | Date | Decision (PM) | What it changed | PRD effect |
|---|---|---|---|---|
| R1 | 20 Sep | **A label for highlighted feedback** so the teacher can easily pick a few to show the class — *a requirement for the teacher* (PM). Became クラスで紹介する / Highlight for class on the review screen, with **a short few-word reason**, ★ before the ID in the tables | T9, T6, T8, dashboards, student note card | C3, C5, C10.0 |
| R2 | 20 Sep | **Highlighted-only is an option inside Filters**, not a chip in the bar; applied chip "Highlighted: yes" | T6, T8 | — |
| R3 | 20 Sep | "Not visible to the student" chip **not needed** — the In Review status and the Draft feedback header already say it | T9 | — |
| R4 | 20 Sep | The comments-count section (drafts / edited / criteria) is **not useful when the teacher can browse the comments** | T9 | — |
| R5 | 20 Sep | The ⋮ kebab keeps four items: this student's submission history, download the original file, regenerate the draft, preview the student's screen (to ratify, C11.7) | T9 | — |
| R6 | 20 Sep | **Previous / next navigation between student submissions** from the review screen, in the submissions list's order, Not Reviewed first | T9 | C4 |

### C11.5 Back Office — Group Dashboard (20 Sep)

The Group Dashboard was built in one pass and then taken apart block by block. The sequence is kept in order because it records what was rejected as well as what was kept.

| # | Date | Decision (PM) | Outcome | PRD effect |
|---|---|---|---|---|
| G1 | 20 Sep | **Fit the AI Feedback overview into production's Group and Student Dashboards** | T10–T12 built | C10.0 |
| G2 | 20 Sep | **Not required:** Questions Solved via AI tile; Avg. time to return tile; then the whole AI Feedback tile row | Removed | C10.0 |
| G3 | 20 Sep | **Topic select above the matrix removed** — not in production | Removed | — |
| G4 | 20 Sep | **Latest / Highest Score toggle on the left**, per production code. Latest / Best Submission was rejected as a rename — there is no criterion for the "best" feedback submission. **Grey the whole toggle out** when there are no scores to display | Production labels kept; toggle greyed | C10.0 |
| G5 | 20 Sep | Per-cell **comment count: keep it in Submission Grading only**, use case unclear | Removed from cells | — |
| G6 | 20 Sep | **Two panels below the matrix** (comments by criterion; requirements that stopped a submission) **not required** | Removed | C10.0 |
| G7 | 20 Sep | **Remove the non-AI-feedback LOs from the matrix** for a clearer demo | Matrix shows three feedback LOs | — |
| G8 | 20 Sep | **A highlight filter on the matrix** | Highlighted-only chip beside the toggle | C10.0 |
| G9 | 20 Sep | Overview blocks **not necessary / not required:** Not submitted (already in the matrix), Waiting on you (matrix header and Submission Grading carry it), Acted on the feedback | Removed | C10.0 |
| G10 | 20 Sep | Highlighted picks **link directly to the student's submission** and carry the **reason**, merged into the matrix; the lone ★ beside the status is redundant once the reason is shown | Reason line in the cell, opens the submission | C10.0 |
| G11 | 20 Sep | **Auto-returned status not needed** in the matrix cells | Removed there; stays in Submission Grading and Student Dashboard | C3 |
| G12 | 20 Sep | "What the class missed": PM asked what the criterion is (a count of drafts with an improvement comment per criterion) and **whether a generic prompt / agent over the feedback and the rubric could produce useful insight** — accepted | Insight paragraph grounded in counts and quoted passages | C10.0 |
| G13 | 20 Sep | **Base the insight on the submissions and the generated draft feedback, not on returned comments** — the teacher sees the dashboard before anything is returned | Basis changed | C10.0, C7 |
| G14 | 20 Sep | **Merge the insight into the Topic Dashboard** instead of the LO Dashboard's overview paper | LO Dashboard = matrix alone | C10.0 |
| G15 | 20 Sep | **Add the Topic Dashboard per production, but for AI Feedback data** | T10 (new board): one AI Feedback column | C10.0 |
| G16 | 20 Sep | Topic Dashboard: **remove the topics with no AI Feedback LO** (demo); search reads **Search by Chapter Name or Topic Name**; **display start and due dates** per LO | T10 | C10.0 |
| G17 | 20 Sep | **Add Filters per production, plus an AI Feedback start- and due-date range filter; show the selected ranges** as applied chips | Filters panel on all three dashboards | C10.0 |
| G18 | 20 Sep | **No Regenerate control** — no reason a teacher should ask; the insight refreshes itself | Removed | C10.0 |
| G19 | 20 Sep | **Broaden "what the class missed" to insights of several kinds**, of which missed is one, and **show the top-priority insight as judged by the LLM** | Four tagged kinds; top one shown per LO | C10.0, C5 |
| G20 | 20 Sep | **No Details section** — the teacher checks the submissions themself; the insight line only has to alert them | Expansion removed | C10.0 |
| G21 | 20 Sep | Fix cell alignment (centred) | — | — |

### C11.6 Back Office — Student Dashboard (20–21 Sep)

| # | Date | Decision (PM) | Outcome | PRD effect |
|---|---|---|---|---|
| D1 | 20 Sep | **Merge the AI Feedback table into the existing matrix** rather than a new table; then **fit the details into the existing table as columns**, creating feedback columns if required — the submission date is already a column, so remove the detail row | Three feedback columns on the LO rows | C10.0 |
| D2 | 20 Sep | **Hyperlink each row to the specific LO** | LO name → its overview | — |
| D3 | 21 Sep | **Statuses must not sit in score columns.** Rename Returned → **Status**, put every status there with its date if there is space; the score columns show -- for anything unscored, and **Completed moves into Status** too | Status column | C10.0 |
| D4 | 21 Sep | **The abbreviated-comments column is dropped**; the flagged criteria stay | Flagged criteria column | C10.0 |
| D5 | 21 Sep | Broken padding fixed; **Review** while the submission is In Review, **View** once Returned | Action column | C10.0 |

### C11.7 Defaults the PM has seen but not ruled on — to ratify

These exist in the prototype because something had to. They should be confirmed or replaced before C6 is written.
- The four **status names** and tones (Not Reviewed / In Review / Returned / Sent Back) and the two secondary chips, borrowed from production's Submission Grading.
- The **kebab items** on the review screen (R5); the **submission history** icon kept in matrix cells.
- The **★ line in the teacher's note card** on the student's returned screen, telling the student their work will be shown in class.
- The mobile **snap → crop → pages** flow adapted from the unifiedapp student mock.
- The **insight kinds and their names** (見落とし / 良い傾向 / 紹介候補 / 提出状況), and the rule that every claim must trace to a count in the data.
- The **Auto-returned** chip remaining in Submission Grading and on the Student Dashboard (the PM removed it only from the matrix).
- Bulk Action in the submissions tables as production has it: contained, disabled until rows are selected.

### C11.8 Rejected — do not re-add

Course-level "AI Feedback enabled" chip · AI-use declaration · self-check on resubmission · AI next-step card · expected-return date on the waiting screen · message / ask-the-teacher buttons · "not visible to the student" chip · comments-count section on the review panel · requirement / criteria counts on the LO overview · Invalid Markers export on the AI Feedback boards · rubric as tag chips, "Generated by AI · LaTeX" label · every Group Dashboard tile (Questions Solved via AI, avg. time to return, AI Feedback counts) · Topic select above the matrix · Latest / Best Submission rename · per-cell comment count · Auto-returned chip in matrix cells · lone ★ beside a highlighted status · Not submitted, Waiting on you, Acted on the feedback blocks · comments-by-criterion and requirements-that-stopped panels · Regenerate on the insight · Details expansion on the insight · topics without a feedback LO on the demo board · a separate AI Feedback table on the Student Dashboard · a comment-count column there · statuses or resubmission counts in score columns.

### C11.10 Boards added after the review — the course-level submission window (23 Sep)

Drawn from the PM's 22 Sep decision (C12 P11) and production's own Course Management flow (`school-portal-admin`, syllabus squad: `CourseList`, `CourseDetail` › Books, `CourseBookDetail` › `LOAvailabilityTable`), not from a comment thread; listed here so the prototype's record stays in one place.

| # | Date | What was drawn | Where | PRD effect |
|---|---|---|---|---|
| W1 | 23 Sep | **Course Management list** (Course Name · Teaching Method · Course Type · Subject) with two courses — a Thursday and a Friday class — assigned the same statistics book, so one book runs on two schedules | T6 | C4 |
| W2 | 23 Sep | **Course detail, Books tab**: the book table linking to the book's availability page (production's alert that LO availability dates are set per book was drawn, then removed on 23 Sep). The book is linked to the course here (Assign Books) | T7 | C4 |
| W3 | 23 Sep | **Learning Objectives Availability**: Chapter · Topic · LO · Start Date · End Date for every LO in the book, per course; Edit Date → inputs → Save with the success snackbar; Import/Export. The AI Feedback LO's window is a Start and an End Date like any LO's; the End Date is the due date | T8 | C3, C4, C7 |
| W4 | 23 Sep | **Resubmission Due** as a third date column, shown only for LOs whose resubmission switch is on — **a proposal**: the resubmission deadline had nowhere to go once dates left the LO | T8 | C3, D |
| W5 | 23 Sep | **Dates removed from the Add LO dialog and the LO Settings tab.** The dialog's 公開期間と締切 block is a pointer to Course Management; the Settings tab lists the window per course with a link to edit it there; the resubmission switch stays, without a date | T2, T4 | C3, C4 |
| W6 | 23 Sep | The LO's Overview under Submission Grading names the course its window belongs to and gains **Edit dates in Course Management**; the Topic Dashboard's start / due line is the course's | T10, T13 | C4, C10.0 |
| W7 | 23 Sep | Student course tab: the not-yet-open LO's sub-line carries the course's start date (11月20日 開始) beside "appears in To-do on its start date" | Screen 1 | C3 |
| W8 | 23 Sep | **Join by QR code** (prototype comment on T6: *add a way for students to join the class by QR code, which is a function on the existing AI Tutor page*). The AI Tutor class list's share icon and its **Share Access** dialog (`ClassListTable` → `AIClassShare`: QR of the class code + Download, the code + Copy, Close) reused for the course — on each course row (T6) and as the third item of the course detail's ⋮ menu, after Edit and Assign Books (T7; PM: in the 3-dot menu, not a button). Scanning or typing the code enrols the student in the course; the course's LOs then appear from their start dates | T6, T7 | C4 |
| W9 | 23 Sep | **The course's Student tab** (prototype comment on T7: *add the student list here who joined the course by code or has been added to the course manually*). Production's `StudentTab` as it is — Student Info, the Action menu, name search and Academic Year / Class / School / Location filters, the table (Student Name · Academic Year · Location · Enrollment Date · Class · School · Study Plan) — production's columns, nothing added. A **Joined via** column (QR code / code entered / added manually) was drawn, then **dropped the same day** (PM: *no separate column required*): for AI Feedback nothing downstream depends on how a student got in, and a self-joined student is visible anyway by their empty Class and Study Plan cells | T7 | C4 |
| W10 | 23 Sep | **Add course** (prototype comment on T6: *add the add course ux flow based on the production code*). Production's `DialogUpsertCourse` in add mode — a full-screen dialog with `CourseForm`: course icon, Course Name (required), Location, Teaching Method (required; Individual / Group), Course Type, Subject, Book (multiple) — Cancel / Save (production's Adaptive switch left out, PM 23 Sep); Save adds the course to the list with the created-successfully snackbar. Drawn filled in with a third class of the statistics course linking the same book. Nothing new for AI Feedback | T6 | C4 |
| W11 | 24 Sep | **The dates are the study plan's** (PM comment on T8: *start and end dates should be based on study plan backend*). The Start and End Date on Learning Objectives Availability are the course's study plan items' `available_from` / `available_to`, read from and written to the study plan backend — one source for this page, Study Plan Management, the student's course tab and To-do, and the dashboards. The proposed Resubmission Due would be one more study-plan-item field. T8's alert says so | T8 | C3, C7 |
| W12 | 24 Sep | **Three UX consequences of the auto-created study plan drawn** (PM: *do 2–4 in the prototype*). (2) The course's Student tab loses production's Study Plan column: saving dates on T8 creates the course's plan and enrols every student, QR-joined ones included, so there is nothing to assign or show. (3) An LO added to the book after the dates were set appears on T8 with empty Start and End and a warning line — shown to students from publish until dates are entered. (4) **Per-student due-date extension, a V2 proposal**: a row action on the Student tab opens 期限の延長 / Extend due date — the course's AI Feedback LOs with their window and one editable end date for this student; Save marks the row 締切延長あり; the course's dates do not move. The study plan's student level carries it | T7, T8 | C3, C7 |
| W13 | 24 Sep | **Generation is automatic on upload** (PM comment on T3: *this will be autogenerated when materials are uploaded, no need for manual trigger*). The 提出条件と観点を生成する button is gone; uploading the brief and the marking criteria generates the basic requirements and the rubric, the file row says so, and 生成し直す Regenerate on the criteria card is the only manual run | T3 | C2, C4 |

### C11.9 Questions the review raised and did not close

| # | Question | Raised where | Owner |
|---|---|---|---|
| Q1 | With Excel and PowerPoint going in as they are, the engine must **read .xlsx / .pptx directly or convert server-side**; page-count style requirements do not apply to a workbook — **per-format basic-requirement checks** in Back Office are proposed, not decided | S17 thread | James Sim → TL |
| Q2 | **Student-facing copy when teacher review is off.** "The teacher gives the feedback" reads correctly in the endorsed case and overstates in the unreviewed one | S18 thread | James Sim |
| Q3 | The review screen and the dashboards **tag comments with a criterion name**; the rubric is now a free LaTeX block, so the block must yield named criteria or the tags need another source | B5 thread | James Sim → TL |
| Q4 | **The reflection rubric** (2–3 criteria) is still Prof. Yasumoto's to author (C10.3); the prototype shows the exercise rubric everywhere | S8 thread | Hinano Matsushita |
| Q5 | **The insight line**: prompt structure (the rubric), grounding rule (every claim traces to a count), refresh trigger, cost per LO per week — and its dependency on **criterion keys fixed per assignment** (§1.6.5, U22) | G12–G20 | James Sim → TL |
| Q6 | **Who may turn teacher review off** for an LO — a Biz rule (A3), given [S4]/[S5] promised administrators confirm responsibility for auto-return | C2 | Takuya Homma |
| Q7 | **The 500-character limit** on typed answers, the 20 MB upload cap and the accepted file types: **Env-level or Tenant-level** | S14, S17 | James Sim → TL |
| Q8 | The **previous / next pager's order** across filters, and whether stepping past the last submission returns to the table | R6 | James Sim |
| Q9 | Whether the **manual Kindai showcase** (C10.1–C10.7) now simply demonstrates T10–T12 with Kindai data, and who owns the in-product dashboard (U17, U25) | C10.0 | James Sim |

## C12. Scope confirmations — the PM's answers to Part C's open questions (22 Sep 2026)

> Eleven questions Part C had been carrying as open, answered in one pass and carried into the sections they settle. Together they draw this PRD's boundary: **it is the LO integration for the Kindai Applied Sociology AI Feedback trial, and the scoring side of the house is a separate PRD.**

| # | The question | The answer | Carried into |
|---|---|---|---|
| P1 | Is this PRD the Q3 AI Grading + AI Feedback merge, the Q4 LO integration, or both? | **The LO integration.** Not the merge. | C1, C2, C7 |
| P2 | Three timelines are live — Oct trial, Jan unified-app V1, Nov Kindai. Which does this PRD serve? | **The AI Feedback trial and the dashboard for Kindai.** The January V1's PDF-based practice is **a RISO vehicle, not Kindai's**, so it is not a competing timeline here. | C1, E2 |
| P3 | Rubric versioning and re-run with a disagreement report — in or out? | **KIV.** Out of this version; the demand has to be validated first. | C2 |
| P4 | Theses and seminar papers: [S3] excludes them, [S4] slide 18 was cited as selling them. Resolve. | **The citation does not hold** — the PM does not find that claim on slide 18. **No contradiction to resolve**; [S3]'s exclusion stands. | C2, D |
| P5 | Oral viva — in scope, or an explicit exclusion? | **Neither: it is not a feature.** It is the client's own workflow that our solution complements. **U10 closed.** | C2, §1.7, D |
| P6 | AI Red-Pen Grading for university submissions — out of scope, and why? | **It is part of AI Grading**, so it is outside this PRD altogether rather than an AI Feedback scope call. | C2, C5 |
| P7 | The engine contract between the scoring products and the feedback engine — this PRD must state it precisely. | **It goes in the AI Grading PRD**, not this one. | C2, C7, C8, D |
| P8 | [S3]'s phasing trap — inferred rubric, trial grading, approval queue only work as a whole. | **AI Grading PRD, later.** That flow is the scoring product's onboarding. | C2 |
| P9 | One feature or two? Applied Sociology's formative loop vs Correspondence's grading assistance. | **One.** Grading assistance is the AI Grading PRD's; this PRD is the formative loop. | C2, C8, E1 |
| P10 | Seven C3 scenarios — cold start, past submissions without scores, an existing institutional rubric, low trial-grading agreement, a student appealing a returned grade, two-stage TA-then-instructor review, an undetected attention-audit item. | **All seven belong to the AI Grading PRD**; removed from C3. | C3, C4, C5, D |
| P11 | The remaining fourteen C3 rows: which are real, which are not, and what the undefined ones do. | **Six removed outright** (low-confidence routing, low OCR confidence, out-of-scope submission, suspected AI generation, and the two rubric-defect rows — **both bugs are fixed**); **one more to the AI Grading PRD** (two reviewers on one submission); **seven defined** — see below. | C3, C1, C4, C7, C10.0, D |

**The seven behaviours P11 defines.** A rubric may be **edited at any time, and every generation after the edit uses the edited rubric** — no versioning, no re-run. Disabling the feature mid-term means **no new generations**; work already done is untouched. The product is **model-agnostic**, with no re-validation ritual, because there is no score to re-validate. A student may **replace a submission without a cap until the due date**. A **late submission is refused** unless the teacher extends the due date. A published LO whose start date has not passed **shows that date on the course tab and is not clickable** until it arrives. And:

> **Submission dates belong to the course, not the LO.** The **submission start and due date are managed on the Course Management page**; the book is linked to the course; **the course's window gates student submissions.** This answers the per-class variation that 17 Sep left unsolved — two courses sharing a book run the same assignment on their own dates — and it supersedes the LO-level dates first drawn in the prototype; the prototype now carries the window on Course Management › Books › Learning Objectives Availability (C4, T6–T8) and the LO dialog and Settings tab hold no dates. Two things await the PM's confirmation: that **the LO keeps no dates of its own**, as drawn, and **where the resubmission deadline lives** — drawn as a Resubmission Due column in the same course table. Per-*student* variation remains unsolved.

**What the AI Grading PRD inherits.** Five things drafted in this file are now that PRD's to own: the engine contract (inputs, outputs, the trigger rule, ownership and versioning), the OCR-versus-clean-text asymmetry between the two scoring consumers, [S3]'s setup phasing, the Correspondence Division's 62,000-report volume with its corpus re-grading question, and the business-logic scenarios listed in P10, which arrive with their [S3] and [S6]/[S7] source proposals attached. The material drafted for each is in this file's v1.1 history, so that PRD can lift it rather than re-derive it.

**The test for anything new.** A scenario belongs in this PRD if it can be answered without reference to a mark. If answering it requires a score, an anchor, an agreement threshold or a marking hierarchy, it belongs to the AI Grading PRD — whatever screen it appears on.

---

## D. Readiness gate (before sprint planning)

**Verdict: not ready**, but the shape of "ready" is clear. What is left is mostly authorship: Parts A and B, the rest of C3, and acceptance criteria. Blockers, in the order they must be closed:

- [ ] **Section 1 unconfirmed list is still live.** U1 (is the Kindai trial even approved?) and U3 (which subject the 240 reports come from) gate everything downstream. **Nothing on the 1.7 list has been used in Parts A–C, and nothing may be until its named owner confirms it.**
- [ ] **Part A not authored** — no business goal, no primary metric, no applicability decision, no named Business owner.
- [ ] **Part B not authored** — five candidate jobs, no chosen core job, no desired outcomes.
- [x] **C3's scenario table is complete.** What is left is the checklist, not the table.
- [ ] **Error and failure paths — the largest gap in C3.** Generation failure, model timeout, partial extraction, an unreadable upload: none is defined, and the student-facing behaviour matters precisely because the student is never told AI is involved. **Failed generation is also the one entity state still unnamed.**
- [ ] **Manual override / admin bypass, and the Env-versus-Tenant label on every configurable value in A2.** Neither has been touched; the 500-character limit, the upload cap and the accepted file types are the concrete cases.
- [ ] **The course-level submission window is drawn but not yet decided in two places.** The prototype now carries it on production's Course Management › Books › Learning Objectives Availability page (C4, boards T6–T8), and the LO dialog and Settings tab no longer hold dates — so the first open question is answered in the drawing: **the LO keeps no dates of its own**. The second is drawn as a proposal, not decided: **the resubmission deadline sits in the same course table as a Resubmission Due column**, shown only for LOs with resubmission on. Both need the PM's yes. **Per-student due dates remain unsolved.**
- [x] **The engine contract belongs to the AI Grading PRD.** Scoring vs feedback remains settled architecture; what the scoring products pass in and the rule that fires feedback are the merge's questions. No longer a blocker here; it is a blocker there.
- [ ] **Source contradiction.** [S1]'s §12 calls the trial "operationally well defined" while §10 records an unresolved file-upload defect — against a C2 scope that accepts Excel, PowerPoint, multi-photo and typed answers. Three earlier contradictions are closed: theses/seminar papers ([S4] slide 18 citation does not hold), DOCX (v1 already supports `.docx` and `.pdf`), and mobile-first vs PC-first (C9.1).
- [ ] **Open defects that gate the October trial:** teacher rubrics destroyed by the rubric agent (U18), feedback number bubbles out of sequence on small PDFs, LangSmith validation errors with a possible one-month tail [S15].
- [ ] **Dependencies owed by others before C3 and C7 can be completed:** Bunsuke's LO-type refactoring proposal and Koki's start/due-date demo, both actioned on 17 Sep.
- [ ] **No acceptance criteria.** C3 and C11 give C6 its raw material: every row and every decision can be written as Given/When/Then.
- [ ] **C7 is thin on what remains its own.** The learner-app integration points, the start/due-date data model, data flow, auth and state fields are undefined, and the prototype review added three more (C11.9): reading .xlsx / .pptx or converting them, the insight line's one LLM call per LO, and the rubric block yielding named criteria.
- [ ] **No TL feasibility review**, no T-shirt size, no latency or cost budget.
- [x] **Designs exist** — the clickable prototype [S20] covers the six journeys in C4 (no Figma). Translations exist for every string but are **unconfirmed**.
- [ ] **No Business sign-off** on Part A — and Part A does not yet exist to sign off.
- [x] **The relationship to AI Feedback V1.1 is declared in C1: superseded.** Resubmission is a per-LO setting; the dashboard is fitted into Group and Student Dashboards.
- [ ] **Part C's decisions were taken on a prototype and are not yet reviewed by the TL or Biz.** In particular the per-LO **teacher review off** state (auto-return) needs Biz to say who may set it (A3), and the **student-facing copy when review is off** is open. C11.7 lists the prototype defaults still to ratify.
- [ ] **The AI Grading PRD does not exist**, and six things depend on it: the engine contract, [S3]'s setup phasing, AI Red-Pen Grading, the Correspondence Division's grading assistance, the seven scoring-dependent C3 scenarios, and the concurrency row. Moving them out of this PRD only helps once that PRD is started.

**The dashboard showcase (C10) runs on its own clock and is NOT gated by the above.** It is a manual sales artefact, not a build. Its own blockers, in order:
- [x] Which submission type the showcase covers — **both. Two views, per C10.3.**
- [ ] **The reflection view does not exist as a reading queue.** Specified in C10.3a; the handover prototype has nothing like it, and the product took the insight line instead (C10.0). Decide whether the showcase demonstrates C10.0's dashboards with Kindai data or still builds the queue.
- [ ] **Week-one honesty.** Three of the four queue signals need the reflection rubric or several weeks of history, so the first fortnight is realistically "student asked a question" plus the class-level and submitted views. Frame the showcase accordingly.
- [ ] **The reflection rubric does not exist** and is Prof. Yasumoto's to author — a dependency on the October hands-on, not a design task.
- [ ] **Demo data must be rebuilt** as a Kindai class (~140 students, both submission types). Mechanical, but it gates any client-facing version.
- [ ] **U22 — four production preconditions unmet** (§1.6.5), against a stated goal of "data we can actually collect today".
- [ ] **No mechanism to capture teacher reactions** — which is the entire purpose of the exercise.
- [ ] **Manual production effort uncosted** across a three-month trial with weekly submissions.
- [ ] Hinano wants visuals and content aligned **this month** — that is the binding date, not any release train.

**Shortest path to Ready:**
1. James Sim: confirm U1 (is the trial approved and funded?) with Hinano. It gates everything downstream and is the oldest open item.
2. James Sim: write **C7's learner-app half** — the start/due-date data model, the three learner-app integration points, data flow, auth and state fields.
3. James Sim + Takuya Homma: fix A1's primary metric and A2's applicability, and take A3 to the Business owner — including who may turn teacher review off.
4. James Sim: close what is left of C3 — **the failure paths first** (generation failure, model timeout, partial extraction, an unreadable upload), then manual override / admin bypass and the Env-versus-Tenant labels.
5. James Sim: confirm the **course-level submission window as drawn** (C4, boards T6–T8) — that the LO keeps no dates of its own, and whether the resubmission deadline lives in the course's LO Availability table as proposed.
6. Koki Misawa / Bunsuke Itamura: deliver the start/due-date demo, against course-level dates, and the LO-type refactoring proposal, which C3 and C7 depend on.
7. Tech Lead: size the Kindai burst (~140 submissions within hours of a lecture), the feedback-generation latency and the insight line's per-LO cost before any commitment.
8. James Sim: ratify or replace the prototype defaults in C11.7, then write C6's acceptance criteria from C3 and C11.
9. James Sim: start the **AI Grading PRD**, or name who does. Six decided-out items are homeless until it exists.

---

## E. Delivery record

### E1 — Classification
| Field | Value |
|---|---|
| **Product Area** | **AI Feedback** |
| **Product Manager** | James Sim |
| **Biz Owner** | *TBC — confirm; Takuya Homma leads university GTM* |
| **Tech Owner** | *TBC — confirm* |
| **Partner Name** | **Kindai University — Faculty of Applied Sociology.** The Correspondence Education Division is **not** this item's partner; its grading assistance is an AI Grading PRD item. A general/tenant-configurable decision is still pending in A2 |
| **Project Type** | *TBC — Core feature vs Big Bets; depends on A2* |
| **Affected Area (surface)** | **Learner App** — PC and mobile (Feedback LO in the course and To-do, submit by file / photos / snap / typed, waiting and returned screens, resubmission) · **Back Office** — Book Management (AI Feedback LO type, dialog, Content and Settings tabs, Publish), **Course Management (Course › Books › Learning Objectives Availability — the submission window; an existing page, one column added)**, Course › Submission Grading (queue, overview, submissions, review and return), Dashboard (Group Topic / LO modes, Student) · **API:** no external LMS integration in this scope (C7). Teacher Web / Widget: *TBC* |
| **T-Shirt size** | *Not obtained — chase at the readiness gate* |

### E2 — Rollout and availability
| Field | Value |
|---|---|
| **Feature flag name** | *Not created — **flag naming and the registry are Carlo's; ask, do not invent*** |
| **Preproduction tenants** | Known state at 4 Sep [S16]: `lmsv2` **ON** (full set incl. Class Assignment + ToC), `sankogakuen` testable (AI添削 since 21 Aug). The **AI Feedback trial runs in pre-release from 1 Oct 2026** [S15] — name the tenant |
| **Production tenants** | Known state at 4 Sep [S16]: `aidemo2` **ON** (current sales demo tenant; ToC required for AI Feedback History to work), `lmspsai` / `aidemo` **OFF** (`aidemo` being retired), `demo-lms` not available. **Kindai trial tenant is an open item (U21)** and needs AI Feedback + Class Assignment + ToC enabled before October; enablement is a config change by Cuong Hoang via `#ai-tutor-tech` |
| **Target release train** | *TBC, but the vehicle is named: **the Kindai AI Feedback trial**. Binding dates: **trial starts 1 Oct in pre-release, release targeted 5 Oct** [S15], **Kindai Applied Sociology live 6 Nov** [S1 §1]. The January unified-app V1 (PDF practice) is RISO's, not this — do not plan against it. AI marking and AI 添削 dates belong to the AI Grading track* |
| **Flag default at release** | *TBC — likely off pending client go-ahead, given U1.* **What the flag does mid-term is defined: disabling stops new generations; work already done is untouched** |

### E3 — Release note copy
*Cannot be written — the change itself is not yet defined. Category (新機能 / 機能追加 / 機能改善 / 不具合修正), title, EN/JP internal description, external JP description and named point of contact are all open.*

### E4 — Dogfooding brief
- **Internally dogfoodable?** *Partially.* The engine can be exercised internally with synthetic assignments, but the parts that matter — rubric inference from *real* past graded submissions, instructor voice extraction from *real* past comments, and Japanese-language academic writing at cohort scale — need real client data and a Japanese-language cohort. Business teams should not wait for a full internal dogfood of the university flow.
- **Things to actually try** (written from the prototyped journeys in C4; to be confirmed once the build exists): (1) In Book Management, add an **AI Feedback** LO under a topic, teacher review on, resubmission on; upload a brief and marking criteria, generate the requirements and the rubric, edit one requirement, publish — **then set the submission window on the course the book is linked to**. (2) As a student on a phone, open the LO from the To-do, type a 300-character answer, confirm it, watch the basic requirements check, submit, then replace it before the due date — **and confirm you can keep replacing, with no cap**. (3) After the due date, check that **a late submission is refused**, then extend the course due date and check that it is accepted. (4) In Course › Submission Grading, open the draft, edit one comment, highlight the submission for the class with a reason, approve and return; as the student, open the returned screen and check no AI wording, the teacher's note and the ★ line appear. (5) In Dashboard › Group, find the LO's counts, ★ and insight line in the Topic table, the reason in the matrix cell, and the Status / Flagged criteria columns on the Student Dashboard.
- **Which internal team:** PS and JP sales (they will run the Kindai pilot), content (rubric/material ingestion), QA.
- **What "wrong" looks like:** feedback that writes the student's answer for them (the explicit Kindai guardrail [S1 §2.2]); feedback with no quoted passage; a preliminary assessment visible to a student before instructor approval; a criterion score that cannot be traced to a rubric source; **the word "AI" on any student screen; a feedback LO showing a score, a rate or a ranking anywhere in the dashboards; a comment whose criterion tag is not in the LO's rubric block**.
- **Ready-by date on preprod / who to tell:** *TBC*

### E5 — Wiring
- [ ] PBT Epic created; key on this page and PRD URL on the Jira item — **not done**
- [ ] Confluence page properties set (status, product area, partner, PBT key, design link, biz sign-off) — **not done**
- [ ] Label applied: `prd-draft` → `prd-review` → `prd-approved` — **currently `prd-draft`**
- [ ] Design child created (E1 implies Learner App + Back Office UI), Figma URL attached — **not done; check overlap with Qisheng's AI grading US1–US4 Figma first**
- [ ] At least one LT link before Ready for Development — **not done**
- [ ] **A companion AI Grading PRD exists and has picked up what moved to it** — the engine contract, [S3]'s setup phasing, AI Red-Pen Grading, the Correspondence Division's grading assistance, and the scoring-dependent C3 scenarios. **Not created**

---

## Appendix — source index

| Ref | Source | Type | Date |
|---|---|---|---|
| S1 | [Kinki University — Manabie AI Feedback Trial: Detailed Brief and Current Status](https://docs.google.com/document/d/1yay5gBWZkiheZYevlJN_Mqg6lO9OrhiGmXZ0YhBszRQ/edit) | Client/deal brief | 10 Sep 2026 |
| S2 | [Kindai University Distance Education — Overview and AI Feedback Opportunities](https://docs.google.com/document/d/1HHj5-TVYPS6awe4LgqzciLj3ANkQrW2Ap3adOj3L1O4/edit) | Opportunity analysis | Sep 2026 |
| S3 | [AI Feedback for Higher Education: Implementation Design](https://docs.google.com/document/d/1Cz-0CMbQM35NAUh5fUB0g6iq9Q-L_9EzbrnH_u8HyxQ/edit) | Internal design paper. Most of its apparatus — anchors, trial grading, approval queue, attention audit — belongs to the AI Grading PRD | 10 Sep 2026 |
| S4 | [University proposal deck — Manabie LMS × AI](https://docs.google.com/presentation/d/1gqjE_yRlDlzJB5hjn8abfi5kprtxzn7v9OIZbewlsDA/edit) | Sales collateral | Sep 2026 |
| S5 | [Juku proposal deck — Manabie LMS × AI](https://docs.google.com/presentation/d/1tR4TP07-QMEkflpVng4dSA1CDGwbVCPuxK7N-f9_x1M/edit) | Sales collateral | Sep 2026 |
| S6 | [Kindai University AI Report Check Trial](https://claude.ai/artifact/1VdG3L8ugcshJ9G9Fq8fkT) | Artifact — ownership unconfirmed (U13) | — |
| S7 | [Kindai University AI Grading Partnership Brief](https://claude.ai/artifact/Hps1jD7gThUXSTu5ACUDZL) | Artifact — ownership unconfirmed (U13) | — |
| **S8a** | [**Weekly AI Direction Discussion — Notes by Gemini**](https://docs.google.com/document/d/1pzUZxU-vZbiNQGfSRBRvu-cqq2uwoweHm9hhTaIO9Is/edit) (Google Meet; quick notes + full notes + transcript) | Meeting — **the AI direction meeting; decides AI Feedback's place in the learner app** | 17 Sep 2026, 10:00 GMT+8 |
| S8b | Takuya / James 1:1, Circleback `zZo5BHAbqxVjjutrqFeRy`; also [Notes by Gemini](https://docs.google.com/document/d/1hHnUhG7w-MJfa33LdfZocGV4PaI00EktgqqzbLVs6gM/edit) | Meeting — university GTM | 17 Sep 2026, 15:00 GMT+8 |
| S15 | [AI Feedback trials grooming — Notes by Gemini](https://docs.google.com/document/d/1G_fvpln_a_oLdxXyD6XBRIBKTIxZViwEvuP1DRD76HQ/edit) | Meeting — current build state, October trial | 11 Sep 2026 |
| S16 | [AI Feedback — Handover (John → James)](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2862710799/AI+Feedback+Handover+John+James), Confluence PRDM | **Handover page — explicitly a draft**; Kindai trial, open bugs, dashboard mock, tenant matrix | created 7 Sep 2026 |
| S17 | `ai-feedback-dashboard-handover.zip` — `dashboard.html`, `HANDOVER.md`, `COMPETITOR-FINDINGS.md`, `dataset/` | Prototype + fixtures + competitor research. **Confidential / 社外秘; all data fictional** | Sep 2026 |
| S18 | Slack thread, `#C0BPM7T182C`, John Paoletto → James Sim cc Hinano ([link](https://manabiebiz.slack.com/archives/C0BPM7T182C/p1789620239541629?thread_ts=1789620229.644139&cid=C0BPM7T182C)) | The showcase ask; Hinano confirms 地域環境統計学 weekly submissions | 17 Sep 2026 |
| S9 | Weekly AI Grading/Marking, `Mkezgcg7nclYlfkKwUau3` | Meeting | 17 Sep 2026 |
| S10 | Content Weekly `KllJcZHljvv2nMfKhkmr0`; Weekly_Content `b4yz0CcxF6iKw6XU7cOjt` | Meetings | 17 Sep 2026 |
| S11 | Weekly AI Direction Discussion, `H6gDlmhD6x4FeJo9QTQ5Q` / `Mp8WpM7zD470xd6Upo4lN` | Meetings | 2 Jul / 18 Jun 2026 |
| S12 | AI Tutor Product Catchup, `51O371bkHOmZJp4u4WAvE` | Meeting | 12 May 2026 |
| **S19** | [**PRD: AI Feedback v1**](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2361622595/PRD+AI+Feedback+v1), Confluence PRDM — **the parent page of this PRD** | Existing PRD (John Paoletto). Web-only, student-initiated, AI-generated rubric per upload, `.docx`/`.pdf`, max 6 feedback items, 20 MB, tenant-level flag, latency excluded | May 2026 |
| **S20** | [**AI Feedback — Back Office + Student Prototype**](https://claude.ai/artifact/FYtGUxxHgPhzWnENGtgLmE), Claude Design canvas; source `prototypes/ai-feedback-student/gen.py`, static build in `prototypes/ai-feedback-student/deploy/` | **Clickable prototype, JA + EN** — student PC (8 boards), student mobile (10), Back Office (15, the course-level submission window added 23 Sep); sticky notes record the PM decisions; the 91 comment threads are the review record consolidated in C11 | 18–23 Sep 2026 |
| S21 | [Book Management PRD](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/1133903925/Book+Management), Confluence PRDM — Book → Chapter → Topic → LO | Existing PRD, cited by the PM on 18 Sep as the hierarchy the AI Feedback LO lives in | — |
| S22 | Production Back Office code and its generated prototype (`school-portal-admin`: BookDetail tree and DialogCreateLearningMaterial; ToReviewListPage and GradingScorePage; GroupDashboard and StudentDashboard), checked 19–20 Sep | The components the Back Office boards reproduce; production labels kept as production has them | — |
| S23 | [Weekly AI Direction Discussion — Notes by Gemini](https://docs.google.com/document/d/1y04oYHnmQ1vFHW5JXALpB6ycbevCn1j6TqNYbOv6Jzw/edit) (quick notes + full notes + transcript); change plan in `PRDs/ai-feedback-change-plan-2026-09-24.md` | Meeting — scoring allowed in the feedback format, study plan as the date model, dashboard columns, LO refactor on 28 Sep | 24 Sep 2026 |
| S13 | `PRDs/ai feedback.pdf` — AI Feedback V1.1 | Existing PRD | — |
| S14 | `PRDs/ai grading.pdf` — Onigroup SOW, Class & Homework Assignment v1.1 | Existing SOW | Mar 2026 |
| — | `overall_ranking_en.html` (uploaded) | **Unusable — Slack application shell, no recoverable content (U14)** | — |
| — | "Differentiation and Moat Strategy for AI Feedback" (referenced by S3) | **Not supplied — obtain before using M1/M2/M5 terminology** | 10 Sep 2026 |
