# PRD: AI Feedback — Universities (primary) / Juku (secondary)

> **Authorship status — read this before using this document.**
> Section 1 (Background) is populated from client meetings, internal strategy documents, market decks and today's AI direction discussion. Every line carries its source.
> **Parts A, B and C are NOT authored.** They contain *candidates and questions* drawn from those sources, each clearly labelled. Product scope discussed in a meeting or asserted in a business deck is not a specification. The PM converts each candidate into a decision — or rejects it — before this PRD goes to review. Nothing in Parts A–C may be treated as committed behaviour until that happens.

| | |
|---|---|
| **Status** | Draft — Parts A–C not yet authored |
| **Product line** | LMS / **AI Tutor** / ERP |
| **Product Area (E1)** | AI Feedback |
| **Author (PM)** | James Sim |
| **Tech Lead** | *TBC — confirm (see E1)* |
| **Business owner (sign-off)** | *TBC — confirm (Takuya Homma for university GTM? see E1)* |
| **Target partner(s) / market** | **Primary:** Kindai/Kinki University — two independent tracks: (a) Faculty of Applied Sociology, (b) Correspondence Education Division. **Watching:** Sugiyama Jogakuen Univ., Kyoto Koka Women's Univ., Nagoya Univ. of Foreign Studies, Keiwa Gakuen Univ., Shitennoji Univ. **Secondary:** Juku — Waseda Academy, Eishinkan, Z-kai, CKC/Solomon, Toshin |
| **Release target** | *TBC — Kindai Applied Sociology pilot needs product in learners' hands by late Oct 2026; course starts 6 Nov 2026* |
| **TDD link** | *Not created* |
| **Design / Figma link** | *Not created for this scope* |
| **Jira epic** | *Not created* |

### Change log
| Date | Version | Author | Change | Status | Approved by |
|------|---------|--------|--------|--------|-------------|
| 2026-09-17 | v0.1 | James Sim (drafted with Claude) | Section 1 populated from source documents; Parts A–C raised as candidates/questions; Parts D–E scaffolded | Draft | — |
| 2026-09-17 | v0.2 | James Sim (drafted with Claude) | Added the **Weekly AI Direction Discussion of 17 Sep** (Gemini notes — the session that decides AI Feedback's place in the learner app: error/LO type with its own To-do icon, start/end-date layer over the LO, January V1 excludes AI Feedback) and the **11 Sep AI Feedback trials grooming** (Oct preprod trial, rubric-overwrite defect, rubric weights removed). Added the blocking scoring contradiction (U15), six new C3 behaviour rows, U15–U19, and the PC-first vs mobile-first design conflict | Draft | — |

---

## 0. TL;DR

*Not written — depends on A1 and B1, which are PM decisions.*

What is true and can be said today: Manabie has AI Feedback shipping as a student-initiated, rubric-aligned essay feedback feature (V1.1), a separate AI Grading/Marking pipeline for paper-based submissions, and a stated direction that the two converge onto one engine and one submission flow. University demand for feedback is arriving faster than the product is standardised, and at least one committed pilot (Kindai Applied Sociology, ~140 students) expects to run from 6 Nov 2026.

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

- **Scale.** 10,273 learners in the 2026 census vs 9,244 in 2025 (~11.1% growth); includes degree, non-degree and special preparatory students, so it is not a count of degree students alone. [S2] — [S7] states 9,600 enrolled across 4 programs. **These two figures conflict; see 1.6.**
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

## 1.5 Confirmed — today's AI direction discussion and adjacent product meetings (17 Sep 2026)

> **Where the notes live.** The **Weekly AI Direction Discussion of 17 Sep 2026, 10:00 GMT+8** ran in Google Meet and was minuted by **Gemini, not Circleback** — [Notes by Gemini](https://docs.google.com/document/d/1pzUZxU-vZbiNQGfSRBRvu-cqq2uwoweHm9hhTaIO9Is/edit) (quick notes + full notes + full transcript). Attendees: **James Sim, Bunsuke Itamura, Koki Misawa, Trieu Le Hong. Takuya Homma was invited but did not attend** (struck through on the invite). A separate **Takuya / James 1:1** ran the same day at 15:00 GMT+8 and *was* captured by Circleback (`zZo5BHAbqxVjjutrqFeRy`); it covers university GTM rather than app architecture. Both are recorded below and cited separately.

### 1.5.1 Weekly AI Direction Discussion, 17 Sep 2026 — **this is the session that decides how AI Feedback sits in the learner app**

> Source: **[S8a]** Notes by Gemini, as above. Quotes are from the verbatim transcript.

**The unifying decision.** The meeting was an app-redesign review of Koki Misawa's demo, whose stated purpose was merging LMS, AI Tutor, AI Feedback and the J-Prep/study-plan app into **one application navigation**: an **assignment tab**, a **to-do tab** (based on Takuya's B2C app 1.0), and a **course tab**. Koki: *"how we can merge the all the experience into one app… as well as how we can beat the Monoxa."*

**AI Feedback is an error/LO type in the learner app, and it needs its own icon.** Koki: *"we need to divide the error type further like PDF errors, video errors, quiz errors, you know, AI feedback, you know, AI flash card… so that we can visually see on the to-do list what student needs to be done."* This is the concrete form of the "everything under the LO/error structure" position from 2 Jul.

**The load-bearing problem raised, and the decision taken — how AI Feedback reaches the student's To-do.**
- Koki stated the problem: *"AI feedback like whenever teacher create should move into [to-do] but… all of things are preset, right? In this case it can be weird — you have all the AI feedback as a to-do, it seems weird."* And more precisely: *"if you do that you have whole semester AI feedback here when teacher publish before the semester, then you have like let's say 20 set of the AI feedback it comes here, it gets too messy. To-do list is something that you want to define what you do right now."*
- Koki also noted the gap: *"we don't have like due functionality on errors."*
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
- **Rubric weights are being removed because AI Feedback does not use scoring.** *(See the contradiction flagged in C2 — Kindai's rubric is a scored 0–5 across six dimensions.)*
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

**Prior AI Direction Discussions (for continuity, not today):**
- **2 Jul 2026** (`H6gDlmhD6x4FeJo9QTQ5Q`): AI Feedback and AI Grading have separate back ends but **are converging into one unified flow** — Q3 milestone is integrating AI Grading and AI Feedback into a single flow; **Q4 is plugging that into the LMS LO submission flow**. Koki Misawa: AI Feedback as a standalone student-initiated feature is hard to sell — *"students won't proactively use it"*; the more useful model is batch processing with submissions auto-returned. Koki also: feedback and grading should both operate **under the LO / "error" (LO row) structure**, with HQ pre-building curriculum because juku teachers won't create assignments on the spot. AI Grading should be sold **with LMS** so the grading agent references LMS LOs instead of requiring answer-key upload.
- **18 Jun 2026** (`Mp8WpM7zD470xd6Upo4lN`): AI Feedback demos well but was **not trial-ready** — assignment-level only, no class management. Bunsuke Itamura suggested structuring the merged product **by assignment type (test vs essay)** rather than by feature, entry point always class/assignments.
- **12 May 2026, AI Tutor Product Catchup** (`51O371bkHOmZJp4u4WAvE`): the team wants AI Feedback output format **teacher-configurable** — sections, titles, granularity (passage vs line level) and length defined by the rubric, plus a standard closing "final comment" block; students choose general vs targeted (assignment-tied) feedback at upload; supported uploads PDF/JPG/PNG.

## 1.6 Stated but UNCONFIRMED — each needs a named owner before it can be used

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
| U10 | Oral viva (post-submission spoken authorship check) is in Manabie's scope | [S7] | Named as a client requirement and as the feature the client is evaluating other vendors for. No Manabie capability, PRD or estimate exists. | James Sim |
| U11 | File-upload defect and missing learning-log visualisation are still open | [S1 §10] | Status recorded as of **17 Aug 2026** — one month stale at time of writing. | Tech Lead |
| U12 | Kindai correspondence wants grading, not feedback | Takuya/James 17 Sep | James: *"so far what you shared is mostly gearing towards grading"* — an inference from translated meeting notes, with the clarifying meeting on 18 Sep. | James Sim |
| U13 | Artifacts [S6] and [S7] are Manabie-authored | Artifact tool | Returned marked "created outside your organization". | James Sim |
| U14 | Uploaded file `overall_ranking_en.html` content | User upload | **The file is a Slack application shell with no recoverable content** — text extraction yields only the word "Slack". Nothing from it has been used. Re-share as a Slack permalink or export. | James Sim |
| U15 | AI Feedback does not use scoring | [S15] 11 Sep | Rubric weights were removed on this basis, but Kindai's rubric is a scored 0–5 across six dimensions [S1 §3] and both [S3] and the AI Grading convergence assume scoring. **See C2 — this is a blocking contradiction, not a detail.** | James Sim + John Paoletto |
| U16 | Start/end-date layer over the LO is the agreed mechanism for To-do population | [S8a] 17 Sep | Aligned in the meeting as a direction; the demo that makes it concrete is an open action on Koki, and per-student/per-class due dates are explicitly unsolved. | Koki Misawa → James Sim |
| U17 | AI Feedback dashboard sits with the AI Grading team | [S15] 11 Sep | James's decision, recorded in grooming notes. Needs confirming against the Kindai pilot's dashboard need and against the 17 Sep "consolidated group/individual dashboard" position. | James Sim |
| U18 | Rubric-overwrite fix (teacher rubrics bypass the rubric agent) is implemented | [S15] 11 Sep | Agreed in the meeting; no ticket status confirmed as done in any source read. Blocks the "rubric lifecycle" differentiator. | Cuong Hoang |
| U19 | January V1 excludes AI Feedback | [S8a] 17 Sep | Aligned that V1 is "PDF practice only" — but the AI Feedback preprod trial starts 1 Oct and Kindai goes live 6 Nov. Confirm these are three separate vehicles, not a conflict. | James Sim |

---

# PART A — BUSINESS

> **NOT AUTHORED.** The material below is a set of candidates and the questions that close them. A single client asking once — however clearly — is not a business goal.

## A1. Business goal & outcome metric — *PM decision required*

**Questions that must be answered:**

1. **What is the business outcome?** The sources support at least three materially different ones, and they imply different builds:
   - *(a) Win and retain university accounts* — the metric would be signed university contracts / pilot-to-paid conversion.
   - *(b) Make AI Feedback the shared engine* behind AI grading feedback, AI marking feedback and the Feedback LO — the metric would be % of feedback generated through one pipeline, or engines retired.
   - *(c) Reduce instructor time per submission* — the metric would be measured minutes per approved submission.
   These are not the same goal. **Pick one primary.**
2. **What is the ONE primary metric and its target + timeframe?** No source contains an agreed metric. [S1 §9] targets are explicitly not agreed with the university (U7); [S3] targets are internal proposals (U8); [S4]/[S5] numbers are sales assumptions (U9).
3. **Supporting metrics / tracking — what must the product log?** Candidates surfaced by the sources, none yet decided:
   - approval rate, and instructor edit distance per approval over time [S3]
   - agreement between preliminary AI assessment and instructor-finalised score (QWK), per assignment and over time [S3]
   - time from submission to return; actual instructor seconds per approval [S3][S4]
   - resubmission/revision count per assignment [S1][S4][S5]
   - pre-submission self-check usage and the resubmissions it avoided [S6]
   - low-confidence routing rate and the share of flagged items the instructor overturned [S3]
   - **Note:** learning-log visualisation was not implemented as of 17 Aug 2026 [S1 §10, U11]. If tracking is a goal, this is a dependency, not a reporting afterthought.

## A2. Scope of applicability — *PM decision required*

- This feature is: **General / Tenant-configurable / Partner-specific** — **not decided.**
- **Candidate (strongly evidenced, still the PM's call): Tenant-configurable, built general.** The direction stated today is a *"standardized, versatile workflow that can serve different use cases without rebuilding from scratch each time"* (Takuya, 17 Sep) and *"built purposefully for just that use case… everything else is just a front end layer of UI/UX"* (James, 17 Sep).
- **The specific values that must NOT be hardcoded to Kindai**, each of which appears in the sources as a concrete number and each of which needs an explicit Env-level / Tenant-level decision in C3:
  - feedback length ~400–600 Japanese characters [S1]
  - three-part feedback structure (recognition / reflective question / actionable guidance) [S1]
  - six rubric dimensions on a 0–5 scale [S1] vs five criteria [S4] vs four CEFR-aligned criteria [S5] vs 13 format rules R1–R13 [S6]
  - 10–20 past submissions as anchors; first-five cold start [S3]
  - character count bounds 400–700 per answer [S6]
  - 1–2% attention-audit injection rate [S3]
  - confidence threshold for routing [S3][S7]
- **Question to answer:** Kindai Applied Sociology's rubric includes a **generative-AI literacy** dimension [S1 §3] and the correspondence division's check is **13 formatting rules** [S6]. Is the rubric model general enough to express both, or are these two different products? If two, say so here and split.

## A3. Business rules owned by Biz — *PM decision required*

Rules the sources show Business, not Engineering, must decide. None are decided:

1. **Pricing model.** ¥900 AI Tutor + ¥700 AI Feedback per student per month is quoted for Applied Sociology [S1]; the correspondence division prefers ¥700–1,800 per student flat, explicitly not per-report [S7, U4]. Is per-student flat the model for universities generally?
2. **Score display policy.** [S3] and [S4] both assert students must never see a preliminary AI assessment as a grade before instructor confirmation. This is a **policy commitment with regulatory weight** (MEXT; EU AI Act high-risk from Dec 2027 [S3 ch.8]) — Biz must own it, not infer it.
3. **Accuracy claims made in sales.** Takuya, 17 Sep: *"we never say like it's 100% accurate"*, and 90–95% is acceptable. What exactly may be claimed, and against what evaluation set?
4. **Data, rights and retention.** Use of past student submissions; third-party copyrighted content in lecture slides under Copyright Act Art. 35, where AI processing is **not settled law** [S3 ch.8]. [S3] recommends syllabus language and a one-page template for the university's personal-information office. Legal review is named as a precondition to deployment — is it commissioned?
5. **Oral viva.** In or out (U10). The client is evaluating competitors on it [S7].
6. **What Manabie commits to for the pharmacy-school track** — 1,103 students, full annual implementation, no trial appetite [S1 §11].

*Business sign-off is captured once at the Section D readiness gate, not here.*

---

# PART B — PROBLEM

> **NOT AUTHORED.** A job-to-be-done drafted from a meeting note is how a stray remark becomes a committed behaviour. Below are the candidate jobs the sources point at, and the tests each must pass.

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

**Then frame it:** *As a [persona], I want [outcome] so that [value].* — to be written by the PM.

## B2. Desired outcomes (the user's success metrics) — *PM decision required*

Candidates, each to be restated by the PM as *direction + metric + object + context*, and each to be solution-free. Every element of Part C must move at least one of these:

- Minimise the time between a student submitting work and receiving actionable feedback on it. *(currently 2 weeks at 300-student scale [S4]; "20+ days" in juku [S11 repo SOW])*
- Minimise the instructor time required to return feedback that the instructor is willing to put their name to.
- Minimise the variance in grading standard across instructors teaching the same subject.
- Increase the number of revision cycles a student completes before final submission.
- Minimise the likelihood that a student submits work that will be rejected on grounds they could have fixed themselves.
- Minimise the likelihood that a polished submission conceals weak understanding.
- Increase the instructor's confidence that the returned assessment matches their own grading. *([S3] proposes asking this directly on a five-point scale)*

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

**Note on the executor split, from today's direction discussion and 2 Jul:** Koki's position is that a student-initiated feature will not be used — *"students won't proactively use it"*. The current V1.1 product **is** student-initiated. If B4 lands on "the instructor is the executor", that contradicts the shipped product's flow and C2 must say so explicitly.

## B5. Evidence — *PM to promote from Section 1 with judgement*

Section 1 is what we were told. B5 is what the PM decides actually proves the problem is real and big enough to size the build. **This promotion is a decision, not a copy-paste.**

**Assessment of evidence strength as it stands:**
- **Strong:** the correspondence division's volume (62,000 reports/yr, 156 faculty, 500–600 reports per high-volume instructor) [S7] and the 241-report retrospective showing 36% avoidable resubmissions [S6] — this is measured, from the client's own operation.
- **Moderate:** Kindai Applied Sociology — well-specified course, rubric, materials and quotation, but **~140 students, one professor, one course, and not yet approved** (U1). Two-university interest plus a well-attended faculty seminar (Takuya, 17 Sep) is directional, not sized.
- **Weak — do not size the build on these:** all model-case deltas in [S4]/[S5] (self-labelled hypothetical, U9); all [S1 §9] evaluation thresholds (explicitly not university-approved, U7); all [S3] operating targets (internal proposals, U8).
- **Counter-evidence that should change scope, not be filtered out:** Ohzora's credit-granting exam was judged a *poor fit* even at 80% accuracy because every entry still needs manual review (Weekly AI Grading, 17 Sep). Kindai is deploying Google AI Pro for Education broadly [S1 §10]. Both point the same way — the defensible value is workflow, rubric governance and the record, not model output.

---

# PART C — SOLUTION

> **NOT AUTHORED.** This is where precision matters most and where PRDs most often fail. Numbers floated in meetings and decks are **inputs the TL must validate**, not rules. Everything below is a candidate or an open question.

## C1. Solution summary — *PM decision required*

**The shape the sources point at**, to be accepted, rejected or rewritten by the PM:

One AI Feedback engine — rubric in, submission in, criterion-level assessment plus instructor-voiced draft feedback out — consumed by three surfaces:
1. **AI Grading feedback** — feedback attached to an AI-graded submission.
2. **AI Marking feedback** — feedback attached to a photo/paper-based marked submission.
3. **A Feedback LO in the learner app** — feedback as a distinct **error/LO type** inside the existing LO submission flow, carrying **its own icon** on the To-do list alongside PDF, video, quiz and AI flash-card types, and populating the To-do via **start and end dates layered over the LO** (the aligned decision of 17 Sep).

**Open at the level of the summary itself:**
- The 17 Sep AI Direction Discussion says *"grading and feedback should be part of"* the unified app experience, and 2 Jul set Q3 = merge AI Grading + AI Feedback into one flow, Q4 = plug into the LMS LO submission flow. **Is this PRD the Q3 merge, the Q4 LO integration, or both?** They are different releases with different risk.
- **The January V1 does not include AI Feedback.** The 17 Sep session aligned that V1 in January is *PDF-based practice functionality only*. Meanwhile the AI Feedback trial runs in preprod from **1 October** with a **5 October** release [S15], and Kindai Applied Sociology expects live use from **6 November**. **Three different timelines are in play and this PRD must say which one it serves.**
- Today James also noted the current prototype returns feedback straight to the student with no teacher in the loop and *"I don't think it's meant to be this way"*. **Is teacher-in-the-loop mandatory, optional per assignment, or per tenant?** This single answer changes C3, C4, C6 and A3 simultaneously.
- The existing **AI Feedback V1.1** PRD (`PRDs/ai feedback.pdf`) lists **teacher dashboard** and **iterative feedback / re-upload** as *out of scope*. Kindai Applied Sociology needs a teacher dashboard by late October (Takuya/James, 17 Sep) and its whole loop is submit → feedback → revise → resubmit [S1 §2.1]. **This PRD either supersedes those exclusions or it does not — say which, explicitly.**

## C2. Scope — in and out — *PM decision required*

**Candidate in-scope** (each needs a yes/no, not a nod):
- Instructor-defined rubric with versioning and re-run against past submissions, with a disagreement report *(named the strongest competitive gap in [S7])*
- Rubric inference from assignment instructions + syllabus + past graded submissions, presented for approval with per-criterion source traces [S3 ch.3]
- Approval queue with confidence routing and 30-second-per-item card [S3 §3.2]
- Student-facing pre-submission self-check [S6]
- Formative mode: draft → feedback → revise → resubmit, with version history [S1][S2][S3]
- Feedback grounded in course materials with page/line/slide references [S1 §4; Takuya 17 Sep]
- Teacher/group/individual dashboard integration (not a standalone dashboard) [Takuya/James 17 Sep]
- PDF + image submission; Word/text [S3 ch.9] — **note [S1 §10] records only PDF reliably working as of 17 Aug**

**Candidate out-of-scope, with the reason each is a candidate:**
- **Graduation theses, seminar theses, specialised open-ended writing** — [S3 ch.5] excludes them: ambiguous criteria, few anchors, high stakes. **But [S4] slide 18 sells exactly this** ("draft guidance for graduation theses, seminar papers, research proposals", 4th-years, 200 students). **This is a live contradiction between the design paper and the sales deck and the PM must resolve it here.**
- **Oral viva** — U10; no capability exists, and the client is shopping it to competitors [S7].
- **AI Red-Pen Grading for university submissions** — James, 17 Sep: *"not for Kindai… most of the submissions gonna be PDF"*.
- **Auto-return without instructor confirmation** — [S4]/[S5] both state pilots assume instructor confirmation of every item, with auto-return a separate workflow configured after administrators confirm responsibility.
- **DOCX** — out in V1.1; [S3 ch.9] assumes Word is accepted. **Contradiction — resolve.**

**A third contradiction, and it is the most consequential: does AI Feedback score or not?**
- On 11 Sep the team **removed rubric weights on the grounds that "AI feedback does not use scoring"** [S15].
- Kindai Applied Sociology's rubric is **explicitly scored — six dimensions on a 0–5 scale** [S1 §3], and its whole institutional case rests on rubric-based assessment records.
- [S3]'s entire design — trial grading, QWK agreement, distribution correction, criterion-level scores on the approval card — **presupposes scoring**.
- The convergence with AI Grading presupposes scoring.
**If AI Feedback genuinely does not score, then it cannot serve Kindai Applied Sociology as specified, cannot be the engine behind AI grading feedback, and most of [S3] does not apply. If it does score, the 11 Sep weight removal needs revisiting. This must be settled before anything else in Part C.**

**Phasing & end-state — the specific trap to avoid.** [S3]'s flow only works as a whole: inferred rubric without trial grading gives the instructor no reason to trust it; trial grading without correction-diff learning means it never improves; an approval queue without confidence routing is just a list. **A phase that ships two of these three is the "2 of 3 settings = nothing" case.** If phasing is chosen, describe the end state and state which phase is independently useful.

**Is this one feature or two?** Kindai Applied Sociology wants *formative feedback that makes students revise*. Kindai Correspondence wants *rule-checked grading assistance at 62,000-report scale with a viva*. They share an engine and almost nothing else in the user journey. **Split them here if they are two.**

## C3. Business logic & behavior rules — *NOT DEFINED — this is the largest blocker*

The table below is **the list of cells that must not be empty**, not a specification. Every "*UNDEFINED*" is a clarification request the team will otherwise raise mid-sprint.

| Scenario / State | Expected behavior | Notes / edge cases |
|---|---|---|
| No submission yet / first use of an assignment | *UNDEFINED* | What does the instructor see before any student submits? |
| Cold start — no past graded submissions | *UNDEFINED* | [S3 ch.7] proposes "instructor grades first five, AI takes over at the sixth". Is 5 the number, and is it Env- or Tenant-level? |
| Past submissions exist but have no scores | *UNDEFINED* | [S3] proposes 10 pairwise comparisons |
| Rubric already exists at the institution | *UNDEFINED* | [S3] proposes skip inference but still run trial grading, since existing rubrics diverge from actual grading |
| Trial-grading agreement comes back low | *UNDEFINED* | [S3] proposes: do not enter operational mode; fall back to first-five. What threshold? Who is told? |
| Submission in draft (formative) vs final | *UNDEFINED* | [S3 §4.1] proposes draft feedback is labelled "learning support", never a grade |
| Preliminary AI assessment produced, instructor has not approved | *UNDEFINED* | Does the student see anything at all? **This is the policy question in A3.2** |
| Instructor approves unchanged | *UNDEFINED* | Is the diff recorded as a zero-diff signal? |
| Instructor edits score only / text only / both | *UNDEFINED* | Correction diffs feed the next run [S3 ch.6] — define what is captured |
| Instructor rejects and regrades from scratch | *UNDEFINED* | |
| Instructor flags for interview / viva | *UNDEFINED* | Depends on U10 |
| Low-confidence item | *UNDEFINED* | Routing order, and whether the student's return is delayed |
| OCR / transcription confidence low on a photo submission | *UNDEFINED* | [S3 ch.9] proposes showing the original image beside the transcription. V1.1 sets OCR target ≥97% |
| Submission is out of the course's scope (concept not in the material index) | *UNDEFINED* | [S3 ch.6] proposes flagging as a confirmation item, **not** as an error |
| Suspected wholesale AI generation / anomalous draft history | *UNDEFINED* | [S3 §4.2] proposes presenting as "candidate for confirmation in an interview", never as a detection accusation. **This is a business rule (A3), not an engineering choice** |
| Student appeals a returned grade | *UNDEFINED* | [S3 ch.8] requires an appeal path with instructor reconfirmation, recorded |
| Rubric is edited after submissions have already been graded against v1 | *UNDEFINED* | Versioning + re-run is the headline differentiator in [S7] — the semantics must be exact |
| Two markers / TA-then-instructor two-stage review | *UNDEFINED* | [S3 ch.7] proposes TA first, instructor final. What happens if both edit? |
| Same submission open by two reviewers at once | *UNDEFINED* | **Concurrency is unaddressed in every source read** |
| Feature is disabled mid-term with submissions in flight | *UNDEFINED* | |
| Attention-audit item injected and **not** detected | *UNDEFINED* | [S3 ch.6] proposes 1–2% injection, ≥80% detection, auto-exclusion of detected cases. Does an undetected injected item ever reach a student? **Answer this one before anything else in this table** |
| Model is replaced | *UNDEFINED* | [S3 ch.6] proposes model-agnostic schema + re-validation via the same trial-grading procedure |
| Pre-submission self-check: student keeps submitting until clean | *UNDEFINED* | Is there a cap? [S6] shows 36% of resubmissions were avoidable — what stops gaming? |
| **Teacher publishes a whole semester of AI Feedback items at once** | *UNDEFINED — mechanism agreed 17 Sep, semantics not* | Aligned: start + end dates layered over the LO, used **only** by the To-do page. Undefined: what a blank start date does; whether the item is visible in the course tab before its start date; whether end date means hidden, overdue, or locked |
| **AI Feedback item passes its start date** | *UNDEFINED* | Appears on To-do. Does it notify? Does it order against other error types? |
| **AI Feedback item passes its due date without submission** | *UNDEFINED* | Koki: overdue shows in red. Still submittable? Still gradeable? |
| **Due date differs per student or per class** | *UNDEFINED — and this has failed before* | Koki: *"study plan is meant to be built for that, and we fail."* Provisional lean is teacher sets on the spot for targeted students. **Do not let this be inferred by engineering** |
| **Teacher-created rubric is saved** | **Currently broken** — routed through the rubric agent, which restructures it and erases the teacher's work [S15] | Agreed fix: teacher rubrics bypass the rubric agent and go straight to the feedback agent. Needs an AC |
| **Student-generated rubric exists alongside a teacher rubric** | *UNDEFINED* | This collision is what produced the overwrite defect |

**Mandatory edge-case checklist — none of these can be ticked yet:**
- [ ] Empty / no-data / first-use state
- [ ] Each status the entity can be in (draft, submitted, AI-assessed, in-queue, approved, returned, appealed)
- [ ] Manual override / admin bypass behavior
- [ ] Error and failure paths (OCR failure, model timeout, partial extraction)
- [ ] Concurrency (multiple markers, TA + instructor)
- [ ] **Configurable vs hardcoded — every value listed in A2 needs an explicit Env-level or Tenant-level label.** None has one.

## C4. User journeys — *PM to write; no designs exist*

Journeys needed, one per persona chosen in B4. Candidate set:
- Instructor: course setup → rubric approval → trial grading review → approval queue → semester-end report
- Student (learner app): assignment appears in To-do → submit → (draft feedback) → revise → resubmit → receive instructor-finalised result
- TA: first-pass review handoff
- Academic affairs: rubric governance, audit log, consistency report

**Design status: no Figma exists for this scope.** The Kindai teacher dashboard is wanted by late October and today's direction discussion resolved it should be *integrated into the existing group/individual dashboards*, not built ad hoc — which means the design dependency is on the existing dashboard, not a new screen. Qisheng Zhang is finalising Figma for AI grading US1–US4 (Weekly AI Grading, 17 Sep); **confirm whether that work covers this flow before commissioning more.**

## C5. Terminology / glossary — *PM to complete; several genuine collisions*

| Term | Definition | Replaces / aligns with |
|---|---|---|
| AI Feedback | *TBC* — today used for **both** the student-initiated V1.1 essay feature **and** the shared feedback engine behind grading/marking | Must be disambiguated; the two are conflated in [S1], [S4], [S5] and in the 2 Jul direction meeting |
| AI Grading | *TBC* | |
| AI Marking / AI 添削 | *TBC* — [S5] and [S4] both market "AI Red-Pen Grading" as the client-facing name | Align EN / JP / client-facing names |
| Feedback LO | *TBC* — a Feedback learning-object type in the LO submission flow | Aligns with Koki's "everything under the LO / error structure" (2 Jul) |
| Preliminary AI assessment | [S3]'s term for the pre-approval output | Deliberately **not** "grade" |
| Anchor | Past graded submission used to calibrate [S3] | |
| Approval queue / approval card | [S3] | |
| Voice model | Extracted instructor tone/length/critique patterns [S3] | |
| Attention audit | Injected known-incorrect items to measure instructor vigilance [S3] | |
| Formative mode | Draft feedback before the deadline [S3] | |
| Rubric lifecycle | Conversational elicitation → versioning → re-run with disagreement report [S7] | |
| Consistency report | Course/department-level drift and agreement report [S3] | |
| Credibility Protocol (M2) / M1 / M5 | Referenced by [S3] as moats from a prior paper **not supplied with this request** | Obtain "Differentiation and Moat Strategy for AI Feedback" (10 Sep 2026) before using these terms |

## C6. Acceptance criteria — *NONE WRITTEN*

Cannot be written before C2 and C3. QA builds the test plan directly from this section; writing ACs against undefined business logic produces the wrong test plan.

**One observation to carry into the ACs when they are written:** [S6] found most AI/instructor disagreement was caused by *instructor* inconsistency, not AI error. Any AC of the form "*then the AI score matches the instructor's historical score*" will therefore fail for reasons that are not defects. [S7] proposes measuring **instructor agreement with the AI's presented evidence**, the number of ambiguous "Review" verdicts, and time per report instead. Decide this before QA writes anything.

## C7. Integration & technical specs — *BLANK, and there are at least five integrations*

This section cannot remain blank. Known integration surfaces:

- **Systems involved:** Manabie LMS (LO submission flow, book/topic/LO, study plan); learner app (To-do, submission, result display); Back Office (rubric creation, approval queue); AI Grading pipeline; AI Marking pipeline + OCR; university LMS — **Kindai Correspondence runs a fully in-house LMS (KULeD) requiring API ingest and write-back with no manual file movement** [S7]; Canvas / Moodle / Manaba / Google Classroom via **LTI 1.3** as proposed in [S3 ch.9]; Onigroup webview + asymmetric JWT per the existing SOW (`PRDs/ai grading.pdf`).
- **Learner app integration points** — the three named in the AI Marking Weekly discussion (Trieu Le Hong / Ming Yew Lee): **(1)** teacher/student registration and class association, **(2)** how the student accesses the assignment on the learner app, **(3)** how the returned result and feedback are displayed back to the student. *All three are undefined for this scope.* Trieu's position on ownership: the LMS team owns the API and everything behind it; consumers integrate at the API level only.
- **Learner app — what the 17 Sep AI Direction Discussion actually settled and what it left open.** Settled: AI Feedback is a distinct **error/LO type** with its own To-do icon, and the To-do page gets a **custom due-date layer built on top of existing LO functions** (start + end dates, used only by the To-do page) rather than reusing LO due-date behaviour. Open and needing a spec: the data model for that layer, whether it lives with the LO or beside it, how it interacts with study plan, and how per-student/per-class variation is expressed. **Bunsuke owes a proposal on LO type refactoring (dedicated PDF and video LO types); Koki owes a demo of start/due-date behaviour.** Both are inputs this PRD depends on.
- **Web/PC path.** University students submit from PC, not phone [S8a], which means PDF/file upload on web is a first-class path for AI Feedback, not a fallback.
- **Data flow:** *UNDEFINED*
- **Auth / token behavior:** *UNDEFINED* for the university case. Asymmetric JWT exists for the Onigroup webview; SSO is a Tier-1 assumption in [S3].
- **State fields:** submission_status, assessment_status, approval_status, rubric_version — *none defined*
- **Feature control level:** Env-level / Tenant-level — ***not decided***. Given A2's candidate (tenant-configurable, built general), this almost certainly needs to be Tenant-level, but a candidate is not a decision.
- **Feature flag:** see E2 — **flag naming and registry are Carlo's; ask, do not invent.**

## C8. Non-functional requirements & feasibility — *TL validation required, none obtained*

Flag every one of these to the Tech Lead **before** commitment:
- **Latency.** No budget stated anywhere for feedback generation. For comparison, the AI Tutor pipeline runs ~62,000 input tokens per question and diagram generation was 2–3 minutes on easy problems (AI Tutor calls, 17 Sep). A 30-second approval card is worthless if generation takes minutes.
- **Volume.** 62,000 reports/year [S7] and a proposed batch re-run of 240 historical reports [S6][S7]. Batch re-grading on rubric version change is a **re-run of an entire corpus** — this is the load-bearing cost question and nobody has sized it.
- **Cost per submission.** Not calculated. [S7] notes the client prefers per-student flat pricing, which puts all volume risk on Manabie. The API-vs-subscription cost gap is live in the org (~$5,000 per 70 questions on API vs $20/month subscription — Daily AI Tutor x AI Harness, 17 Sep).
- **OCR.** V1.1 sets ≥97%; Eishinkan measured 93% average with 70% of samples ≥95% (Weekly AI Grading, 17 Sep). **Reconcile the target with the measurement.**
- **Evaluation at scale.** James, 17 Sep: for a signed client launching in April, evaluation has to be ≥95% automated up front. What is the evaluation harness for feedback quality, and who owns it?
- **The 30-minute setup and 30-second approval budgets [S3] have never been validated by anyone who would have to build them.**

## C9. Localization & design

- [ ] All user-facing strings have confirmed translations — **not started**. Feedback itself is generated in Japanese (400–600 JP characters for Kindai [S1]); AI Tutor Product Catchup (12 May) required both Japanese and English base prompts.
- [ ] JP / long-text overflow checked — **not checked**. 400–600 Japanese characters of feedback plus quoted passages plus criterion scores on a mobile-first card is a real overflow risk; V1.1 is explicitly mobile-first.
- [ ] Design exists and is linked for every flow in C4 — **no designs exist for this scope.** Koki's redesign demo and back-office mock (17 Sep) are the nearest thing; they are a demo, not a spec, and the Duolingo-style visual direction is a separate track owned by JPE.
- **Mobile-first vs PC.** V1.1 is built mobile-first on desktop parity. The 17 Sep session states the opposite for this segment: *"most of the university student they use PC, they never use smartphone to upload… most of the AI feedback should come from PDF document."* **Resolve: is the university AI Feedback flow PC-first?** This changes the design brief, not just a breakpoint.
- Terminology to align JP↔EN before strings are cut: 添削 (marking/red-pen) vs feedback vs grading; ルーブリック; 仮評価 (preliminary AI assessment).

---

## D. Readiness gate (before sprint planning)

**Verdict: NOT READY.** Not close. Blockers, in the order they must be closed:

- [ ] **Section 1 unconfirmed list is still live.** U1 (is the Kindai trial even approved?) and U3 (which subject the 240 reports come from) gate everything downstream. **Nothing on the 1.6 list has been used in Parts A–C, and nothing may be until its named owner confirms it.**
- [ ] **Part A not authored** — no business goal, no primary metric, no applicability decision, no named Business owner.
- [ ] **Part B not authored** — five candidate jobs, no chosen core job, no desired outcomes.
- [ ] **Part C3 has no defined cells.** Every row is undefined and the edge-case checklist is empty. This alone blocks sprint planning.
- [ ] **Does AI Feedback score? (U15)** Rubric weights were removed on 11 Sep because "AI feedback does not use scoring", while Kindai's rubric is a scored 0–5 across six dimensions and both the design paper and the AI Grading convergence assume scoring. **This is the first question to answer — it determines whether the rest of Part C is even the right shape.**
- [ ] **Four live contradictions in the source material must be resolved by the PM, not absorbed:**
      (a) scoring — as above;
      (b) theses/seminar papers are excluded by [S3] and sold by [S4];
      (c) DOCX is out of scope in V1.1 and assumed in [S3 ch.9];
      (d) mobile-first (V1.1) vs PC-first for university submissions ([S8a]).
      A fifth, softer one: [S1]'s own §12 says the trial is "operationally well defined" while §10 records an unresolved file-upload defect and a prototype-stage dashboard.
- [ ] **Open defects that gate the October trial:** teacher rubrics destroyed by the rubric agent (U18), feedback number bubbles out of sequence on small PDFs, LangSmith validation errors with a possible one-month tail [S15].
- [ ] **Dependencies owed by others before C3 and C7 can be completed:** Bunsuke's LO-type refactoring proposal and Koki's start/due-date demo, both actioned on 17 Sep.
- [ ] **No acceptance criteria.**
- [ ] **C7 blank while at least five integrations exist**, including a hard API-only requirement against a client-built LMS.
- [ ] **No TL feasibility review**, no T-shirt size, no latency or cost budget.
- [ ] **No designs**, no translations.
- [ ] **No Business sign-off** on Part A — and Part A does not yet exist to sign off.
- [ ] **Relationship to AI Feedback V1.1 undeclared** — does this supersede its out-of-scope list (teacher dashboard, iterative feedback/re-upload)?

**Shortest path to Ready:**
1. James Sim + John Paoletto: settle U15 — **does AI Feedback score?** Everything else in Part C is downstream of this.
2. James Sim: confirm U1, U3, U12 at the 18 Sep correspondence meeting and from Hinano on the Applied Sociology budget outcome.
3. James Sim: answer the single question in C1 — is teacher-in-the-loop mandatory? Then decide C2's "one feature or two", and which of the three timelines (Oct trial / Jan V1 / Nov Kindai) this PRD serves.
4. James Sim + Takuya Homma: fix A1's primary metric and A2's applicability, and take A3 to the Business owner.
5. James Sim: fill C3 completely. Start with the scoring row, the attention-audit row, the "student sees nothing before approval" row and the four new To-do/due-date rows — all are policy or cross-cutting, and all cascade.
6. Koki Misawa / Bunsuke Itamura: deliver the start/due-date demo and the LO-type refactoring proposal, which C3 and C7 depend on.
7. Tech Lead: size the rubric-version batch re-run and the feedback-generation latency before any commitment.

---

## E. Delivery record

### E1 — Classification
| Field | Value |
|---|---|
| **Product Area** | **AI Feedback** |
| **Product Manager** | James Sim |
| **Biz Owner** | *TBC — confirm; Takuya Homma leads university GTM* |
| **Tech Owner** | *TBC — confirm* |
| **Partner Name** | Kindai University (Faculty of Applied Sociology; Correspondence Education Division) — **plus a general/tenant-configurable decision pending in A2** |
| **Project Type** | *TBC — Core feature vs Big Bets; depends on A2* |
| **Affected Area (surface)** | **Learner App** (Feedback LO, submission, result display), **Back Office** (rubric creation, approval queue, dashboards), **API** (university LMS ingest/write-back). Teacher Web / Widget: *TBC* |
| **T-Shirt size** | *Not obtained — chase at the readiness gate* |

### E2 — Rollout and availability
| Field | Value |
|---|---|
| **Feature flag name** | *Not created — **flag naming and the registry are Carlo's; ask, do not invent*** |
| **Preproduction tenants** | *TBC — but note the **AI Feedback trial runs in pre-release (preprod) from 1 Oct 2026** [S15]; name the tenant* |
| **Production tenants** | *TBC — note Kindai Applied Sociology needs production access before 6 Nov 2026* |
| **Target release train** | *TBC. Known dates: **AI Feedback trial starts 1 Oct, release targeted 5 Oct** [S15]; AI marking UI preprod 21 Sep, prod 5 Oct; AI 添削 evaluation 12–16 Oct, client review from 19 Oct; **unified-app V1 (PDF practice only) January** [S8a]* |
| **Flag default at release** | *TBC — likely off pending client go-ahead, given U1* |

### E3 — Release note copy
*Cannot be written — the change itself is not yet defined. Category (新機能 / 機能追加 / 機能改善 / 不具合修正), title, EN/JP internal description, external JP description and named point of contact are all open. **This is a blank, which is recoverable; do not guess.***

### E4 — Dogfooding brief
- **Internally dogfoodable?** *Partially, and worth saying why.* The engine can be exercised internally with synthetic assignments, but the parts that matter — rubric inference from *real* past graded submissions, instructor voice extraction from *real* past comments, and Japanese-language academic writing at cohort scale — need real client data and a Japanese-language cohort. Business teams should not wait for a full internal dogfood of the university flow.
- **Things to actually try:** *TBC once C2 is settled.* Candidate shape: "upload last year's assignment instructions plus ten graded reports, approve the inferred rubric, then check whether the trial grading agrees with the scores you already gave" — that is the whole value proposition in one action.
- **Which internal team:** PS and JP sales (they will run the Kindai pilot), content (rubric/material ingestion), QA.
- **What "wrong" looks like:** feedback that writes the student's answer for them (the explicit Kindai guardrail [S1 §2.2]); feedback with no quoted passage; a preliminary assessment visible to a student before instructor approval; a criterion score that cannot be traced to a rubric source.
- **Ready-by date on preprod / who to tell:** *TBC*

### E5 — Wiring
- [ ] PBT Epic created; key on this page and PRD URL on the Jira item — **not done**
- [ ] Confluence page properties set (status, product area, partner, PBT key, design link, biz sign-off) — **not done**
- [ ] Label applied: `prd-draft` → `prd-review` → `prd-approved` — **currently `prd-draft`**
- [ ] Design child created (E1 implies Learner App + Back Office UI), Figma URL attached — **not done; check overlap with Qisheng's AI grading US1–US4 Figma first**
- [ ] At least one LT link before Ready for Development — **not done**

---

## Appendix — source index

| Ref | Source | Type | Date |
|---|---|---|---|
| S1 | [Kinki University — Manabie AI Feedback Trial: Detailed Brief and Current Status](https://docs.google.com/document/d/1yay5gBWZkiheZYevlJN_Mqg6lO9OrhiGmXZ0YhBszRQ/edit) | Client/deal brief | 10 Sep 2026 |
| S2 | [Kindai University Distance Education — Overview and AI Feedback Opportunities](https://docs.google.com/document/d/1HHj5-TVYPS6awe4LgqzciLj3ANkQrW2Ap3adOj3L1O4/edit) | Opportunity analysis | Sep 2026 |
| S3 | [AI Feedback for Higher Education: Implementation Design](https://docs.google.com/document/d/1Cz-0CMbQM35NAUh5fUB0g6iq9Q-L_9EzbrnH_u8HyxQ/edit) | Internal design paper | 10 Sep 2026 |
| S4 | [University proposal deck — Manabie LMS × AI](https://docs.google.com/presentation/d/1gqjE_yRlDlzJB5hjn8abfi5kprtxzn7v9OIZbewlsDA/edit) | Sales collateral | Sep 2026 |
| S5 | [Juku proposal deck — Manabie LMS × AI](https://docs.google.com/presentation/d/1tR4TP07-QMEkflpVng4dSA1CDGwbVCPuxK7N-f9_x1M/edit) | Sales collateral | Sep 2026 |
| S6 | [Kindai University AI Report Check Trial](https://claude.ai/artifact/1VdG3L8ugcshJ9G9Fq8fkT) | Artifact — ownership unconfirmed (U13) | — |
| S7 | [Kindai University AI Grading Partnership Brief](https://claude.ai/artifact/Hps1jD7gThUXSTu5ACUDZL) | Artifact — ownership unconfirmed (U13) | — |
| **S8a** | [**Weekly AI Direction Discussion — Notes by Gemini**](https://docs.google.com/document/d/1pzUZxU-vZbiNQGfSRBRvu-cqq2uwoweHm9hhTaIO9Is/edit) (Google Meet; quick notes + full notes + transcript) | Meeting — **the AI direction meeting; decides AI Feedback's place in the learner app** | 17 Sep 2026, 10:00 GMT+8 |
| S8b | Takuya / James 1:1, Circleback `zZo5BHAbqxVjjutrqFeRy`; also [Notes by Gemini](https://docs.google.com/document/d/1hHnUhG7w-MJfa33LdfZocGV4PaI00EktgqqzbLVs6gM/edit) | Meeting — university GTM | 17 Sep 2026, 15:00 GMT+8 |
| S15 | [AI Feedback trials grooming — Notes by Gemini](https://docs.google.com/document/d/1G_fvpln_a_oLdxXyD6XBRIBKTIxZViwEvuP1DRD76HQ/edit) | Meeting — current build state, October trial | 11 Sep 2026 |
| S9 | Weekly AI Grading/Marking, `Mkezgcg7nclYlfkKwUau3` | Meeting | 17 Sep 2026 |
| S10 | Content Weekly `KllJcZHljvv2nMfKhkmr0`; Weekly_Content `b4yz0CcxF6iKw6XU7cOjt` | Meetings | 17 Sep 2026 |
| S11 | Weekly AI Direction Discussion, `H6gDlmhD6x4FeJo9QTQ5Q` / `Mp8WpM7zD470xd6Upo4lN` | Meetings | 2 Jul / 18 Jun 2026 |
| S12 | AI Tutor Product Catchup, `51O371bkHOmZJp4u4WAvE` | Meeting | 12 May 2026 |
| S13 | `PRDs/ai feedback.pdf` — AI Feedback V1.1 | Existing PRD | — |
| S14 | `PRDs/ai grading.pdf` — Onigroup SOW, Class & Homework Assignment v1.1 | Existing SOW | Mar 2026 |
| — | `overall_ranking_en.html` (uploaded) | **Unusable — Slack application shell, no recoverable content (U14)** | — |
| — | "Differentiation and Moat Strategy for AI Feedback" (referenced by S3) | **Not supplied — obtain before using M1/M2/M5 terminology** | 10 Sep 2026 |
