# AI Feedback — student prototype (PC + mobile)

Clickable prototype of the student side of AI Feedback for universities (Kindai
地域環境統計学 exercise, teacher-in-the-loop, revise loop). It accompanies
`PRDs/ai-feedback-university-prd.md`.

Live canvas (Claude Design artifact, comments live there):
https://claude.ai/artifact/FYtGUxxHgPhzWnENGtgLmE

## Layout

| Row | Boards | Size |
|---|---|---|
| PC · 日本語 | `Main` → `02-Assignment` → `03-Pending` → `04-Feedback` → `06-Resubmit` → `07-Pending2` → `08-Feedback2` → `05-Todo` | 1280 × 800 |
| PC · English | same, `-en` suffix | 1280 × 800 |
| Mobile · 日本語 | `M-Main` → `M-Assignment` → `M-Camera` → `M-Crop` → `M-Pages` → `M-Pending` → `M-Feedback` → `M-Sheet` | 375 × 812 |
| Mobile · English | same, `-en` suffix | 375 × 812 |

Every board has a 日本語 / English toggle (header) and a PC / Mobile switch
(bottom-left pill) that jump to the twin screen. The DEMO pill on the waiting
screens simulates the teacher approving and returning the feedback.

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

## Publishing

The canvas is a Claude Design artifact. To republish after editing `gen.py`,
regenerate, then publish `project/canvas.json` and the changed `project/*.dc.html`
to the artifact URL above (the index must be merged onto the live copy first,
because viewers can move notes and boards on the page).
