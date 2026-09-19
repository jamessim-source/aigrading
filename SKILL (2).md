---
name: test-cases
description: >-
  Use when a Jira ticket (LT-XXXXXX), requirement doc, bug report, code diff, or
  an existing screen needs test cases written down before any automation work.
  Triggers: "viet test case", "generate test cases", "sinh case test cho ticket",
  "liet ke scenario can test", "test case cho man hinh X", "regression cases for
  this bug".
  Not for: writing Playwright specs or Jest unit tests - those are separate
  skills. This one stops at the test-case document.
---

# Test Case Generation

## Overview

The deliverable is a **markdown test-case document**, not code. An LLM asked for
test cases will produce a plausible list that reads well and is wrong: routes
that do not exist, buttons nobody built, flags that were removed two releases
ago, and twelve variations of the happy path. This skill forces every case to be
grounded in the source before it is written, and forces the negative and edge
cases to be derived systematically instead of remembered.

**Core principle: a test case that cannot be traced to a requirement AND to real
code is noise. Ground first, enumerate second, write last.**

## Output

```
playwright/tests/<squad>/cases/<TICKET-ID>-<feature-slug>.md
```

- `<squad>` - the squad that owns the feature (`syllabus`, `user`, `lesson`, ...).
  Default to the squads in `my-team.json`; create the `cases/` folder if missing.
- `<TICKET-ID>` - `LT-106024`. No ticket, use the feature slug alone.
- Markdown only. Never put `.spec.ts` in `cases/` - `playwright.config.ts` has
  `testDir: "./playwright"`, so a spec file there would be collected and run.

One document per ticket or per screen. Do not append a second unrelated feature
to an existing document.

## Pipeline

```
1 Ground   → resolve the feature against real source (routes, flags, copy, testids)
2 Extract  → requirements, entities, business rules
3 Analyze  → risks, invariants, BOUNDARIES edge cases, open questions
4 Matrix   → coverage matrix: requirement → case → category → priority → oracle
5 Cases    → Given / When / Then, exactly one When per case
6 Oracles  → how each case is proven, designed after the case, not with it
7 Verify   → grounding greps + coverage analysis + review
```

Full prompt templates per step: `references/prompt-patterns.md`.
Output document skeleton: `references/case-template.md`.

**Steps 1-4 must be done before a single `TC-` is written.** For a one-screen
change they can be five lines each. Skipped is not an option - skipping Step 1
is what produces cases for buttons that do not exist.

### Step 1: Ground in the source

This is the step generic test-generation guides do not have, and the one that
decides whether the output is usable here. Read the real code before writing
anything. Record what you found in the document's Grounding section.

| To ground | Where to look |
|---|---|
| Route / URL | `src/squads/<squad>/routing/routings.ts` + the entity enums it references (`Entities`, `EurekaEntities`, `SyllabusEntity`) |
| Whether the route is even reachable | `routing/useCanAccessRoute.ts`, `routing/useCheckFeatureAndPermissionFlag.ts` |
| Feature flag | `hooks/useFeatureToggle/` + the `Features` enum in `common/constants/feature-keys.ts` - values look like `Syllabus_Quiz_BackOffice_EssayQuestion` |
| Feature config | `@core/feature-setting/hooks/` - dotted keys, e.g. `syllabus.ai_grading.backoffice_webview_url` |
| Permission | `domains/<Domain>/hooks/use*Permission`, `internals/permission/` |
| Roles that exist | `internals/permission/` role constants - do not invent "QA Manager" |
| UI copy (English) | `src/squads/<squad>/i18n/` - cases must quote the real sentence, never the i18n key |
| Selectors | `data-testid` in the domain's `.tsx`, BEM style `Block__element` |
| Entities / field names / enums | `services/**/*.graphql`, `__generated__/proto/**` |
| Existing e2e patterns | `playwright/tests/<squad>/*.spec.ts`, `playwright/page-locator/` |
| Already covered by unit tests | `src/squads/<squad>/**/__tests__/` - do not re-specify at e2e level what a unit test already proves |

Flag-vs-config matters: `Syllabus_*` is a **feature flag** (`useFeatureToggle`),
a dotted name is a **feature config** (`useFeatureSettingConfig`). They are
toggled in different places, so a case that says "turn off X" must say which.

#### Target environment: staging

Cases run on **staging** with a **School Admin** account unless the ticket says
otherwise. That fixes what a `Given` may assume, and it is part of Step 1 -
record it as the first row of the Grounding table.

| Thing | On staging | Consequence for cases |
|---|---|---|
| Feature flag (`useFeatureToggle`, `Syllabus_*`) | always the latest value, i.e. ON | **Do not write flag-OFF variant cases.** The state is unreachable. Note the gate in Grounding, cite the unit test that covers the OFF branch, and list the drop in Coverage Analysis |
| Feature config (`useFeatureSettingConfig`, dotted key) | defaults to `true` | A config-ON case needs no setup. A config-OFF case is allowed, but it changes tenant state - **ask the user before writing it**, and put "needs a config change request" in its Notes and Sign-off row |
| Permission | run as School Admin | Only write a permission case when the feature has its own `use*Permission` branch. Do not spend a case proving a shared route gate |

The point is not that gating is untested - it is that a flag toggle is a unit
test's job and a config toggle is a request to another human. An e2e case whose
`Given` no one can produce is dead on arrival, which is exactly what Step 1
exists to prevent.

If the ticket describes something that does not exist in the source yet, that is
fine - it is a new feature. Say so explicitly in the Grounding section
(`Not yet implemented - cases written against the ticket`) rather than silently
inventing selectors.

### Step 2: Extract requirements

- **Entities** with their states and attributes.
- **Business rules**, numbered.
- **`[REQ-n]`** - stated in the ticket.
- **`[IMP-n]`** - inferred from source or from "obviously". Every one gets a
  one-line basis and goes to the Open Questions list. Inferred behaviour may be
  a bug you are about to bless as expected.

### Step 3: Risks, invariants, edge cases

- **Risks** - `Risk | Likelihood | Impact | Source`.
- **Invariants** - always true regardless of input: `score <= maxScore`, "a
  submission cannot be approved twice", "a marker only sees their own
  allocations".
- **Open questions** - what the ticket does not answer. Write the question. Do
  not pick an answer and encode it as an expected result.
- **Edge cases** - walk the BOUNDARIES checklist, adapted to this product:

| | Category | What it means here |
|---|---|---|
| B | Boundary values | 0 / max score, first and last item, `maxScore = 0` |
| O | Ordering | sort order, duplicates, already-processed submissions |
| U | Unicode & encoding | Japanese input, emoji, long CJK strings in names and rich text |
| N | Null / empty | empty list, no data state, unset optional field |
| D | Data volume | 0 / 1 / page-size / beyond-page-size, pagination and bulk actions |
| A | Access & permissions | each `use*Permission` branch, wrong role, location-scoped data |
| R | Race conditions | double-click submit, two markers on one submission, stale list after mutation |
| I | Integration failures | query error, mutation error, Learnosity / Brightcove unavailable |
| E | Environment | locale EN vs JA, timezone (Luxon), org / partner variant |
| S | State transitions | valid and invalid moves through the submission or study-plan lifecycle |

Not every letter yields a case. Every letter must be *considered*, and the ones
you drop are dropped explicitly in Coverage Analysis.

### Step 4: Coverage matrix

The single artifact that prevents both gaps and duplicates.

| ID | Req | Case | Category | Priority | Oracle type |
|---|---|---|---|---|---|
| TC-001 | REQ-1 | Approve a marked submission | Happy | P0 | UI: status chip becomes "Approved" |
| TC-002 | REQ-1 | Approve fails server-side | Error | P0 | UI: error snackbar; status unchanged |
| TC-003 | REQ-2 | Feature flag off | Flag variant | P0 | UI: Approve button absent |
| TC-004 | REQ-2 | Marker without approve permission | Permission | P1 | UI: Approve button disabled |
| TC-005 | INV-1 | Score entered above maxScore | Boundary | P0 | Data: clamped, not persisted above max |

Categories: `Happy`, `Boundary`, `Negative`, `Error/Integration`, `Flag variant`,
`Permission`, `State transition`, `Concurrency`, `i18n`, `Data volume`.
Priorities: `P0` blocks release, `P1` before release, `P2` nice to have.

Then check, in writing: every `REQ` has at least one happy **and** one negative
case; every invariant has its own case; every high risk from Step 3 maps to a
case; no two rows prove the same thing with different data.

### Step 5: Write the cases

Given / When / Then, in a `gherkin` fenced block per case:

```gherkin
Given I am logged in as a School Admin
  And the feature flag "Syllabus_..." is ON
  And a submission "[Don't touch] E2E Submission 01" is in SUBMISSION_STATUS_MARKED
  And I am on "/to_review"
When I approve that submission
Then a success message "<real English string from i18n>" is shown
  And the submission status reads "Approved"
```

- **Exactly one `When`.** Two actions that both need verifying means two cases.
  This is what keeps a case automatable one-to-one later.
- **`Given` carries the whole world** - role, flag state, config state, seeded
  data, starting URL - and every line of it must be reachable. "Given a
  submission" is not a precondition; the four lines above are.
- **`When` is one user action in business language.** "I approve the submission",
  never "I click `GradingScore__approveButton`". Selectors live in Step 6.
- **`Then` is what the user observes**, quoting the real English copy from
  `i18n/`. `But` is allowed for a negative outcome.
- **No `Given` inside a `Then`.** A case that needs setup halfway through is two
  cases, or its `Given` is incomplete.
- **Test data is named.** Not "some student" but "student with 1 submission on
  course `[Don't touch] E2E Course`". Follow the existing e2e convention of
  `[Don't touch]` prefixes for fixture records; emails on `example.com`.
- First person present, consistent across the whole document.

### Step 6: Oracles

An **oracle** is the observable thing you look at to decide the case passed.
"The submission is approved" is an expected result; "the status chip reads
Approved" is an oracle. Written deliberately after Step 5, so cases are not
biased toward whatever happens to be easy to check.

Per case, at least one positive and one negative oracle:

| Oracle | Example |
|---|---|
| UI state | status chip reads "Approved" |
| Absence / negative | no error snackbar; the Approve button is gone from the row |
| Data | reloading the page still shows Approved |
| Side effect | the submission leaves the "To Review" list |

Be specific. "The page updates correctly" is not an oracle.

### Step 7: Verify

Grounding greps - run these before handing the document over. Replace `<doc>`
and `<squad>`.

```bash
# Every data-testid quoted in the doc exists in source
grep -ohE '\b[A-Z][A-Za-z0-9]*__[A-Za-z0-9]+' <doc> | sort -u \
  | while read -r id; do
      grep -rq "$id" src/squads/<squad> --include="*.tsx" || echo "MISSING testid: $id"
    done

# Every route the cases navigate to is a real route.
# Only picks up double-quoted paths ("I am on "/to_review""), so the file paths
# in the Grounding table do not produce false positives.
grep -ohE '"/[a-z0-9_/:-]+"' <doc> | tr -d '"' | sort -u \
  | while read -r p; do
      seg=$(printf '%s' "$p" | cut -d/ -f2)
      grep -rq "\"$seg\"\|'$seg'\|\`$seg\`" \
        src/squads/<squad>/routing src/squads/<squad>/common \
        || echo "CHECK route: $p"
    done

# Every English string quoted as expected copy exists in i18n
# (run per quoted sentence; grep the EN locale files)
grep -rn "<expected sentence>" src/squads/<squad>/i18n
```

Then the review checklist:

- [ ] Every case traces to a matrix row, and every matrix row to a `REQ`/`INV`.
- [ ] Every `[IMP-n]` is listed as an open question, not silently promoted to a
      requirement.
- [ ] No case depends on another case having run first.
- [ ] `Then` lines quote real copy, not i18n keys, not paraphrases.
- [ ] Every case has exactly one `When`, and no `Given` after a `Then`.
- [ ] All ten BOUNDARIES letters were considered; drops are justified.
- [ ] Nothing in the doc is already covered by an existing unit test.
- [ ] Greps report zero `MISSING`, and every `CHECK` line was manually resolved.
- [ ] Open questions are surfaced to the user, not buried at the bottom.

## Guardrails

- **No `TC-` before the coverage matrix exists.** Cases written first get a
  matrix reverse-engineered to fit them, and the gaps stay invisible.
- **Never invent a selector, route, role, flag, or copy string.** If it is not
  in the source, either the feature is unbuilt (say so) or you are hallucinating.
- **Never write an expected result you had to guess.** It becomes an open
  question instead.
- **Do not write code.** No `.spec.ts`, no Jest, no snippets in the document
  beyond a quoted selector or URL. A separate skill turns cases into automation.
- **Do not edit source** to make a case writable - if a screen has no testid, the
  case uses visible text and notes the gap.

## Red Flags

| Thought | Reality |
|---|---|
| "The ticket is short, I'll just list the cases" | The matrix for a small ticket is six rows. Write it. |
| "I know roughly what the button is called" | Roughly means wrong. Grep the source. |
| "I'll assume the flag is on by default" | On staging it is - flags run at their latest value. What you may not assume is a flag-OFF `Given`, or a flipped feature config: that one needs the user's say-so. |
| "I'll add a case for the flag being off" | Unreachable on staging. Cite the unit test instead and record the drop in Coverage Analysis. |
| "All cases are happy path, the feature is simple" | The matrix is incomplete. Every REQ needs a negative row. |
| "I'll write the Playwright spec while I'm here" | Out of scope. Different skill. |
| "Twelve cases looks thorough" | Count is not coverage. Duplicates dilute review. |

## Anti-Patterns

1. **Skipping Step 1.** The dominant failure. Produces confident, unusable cases.
2. **Cases that restate the UI.** "Click Save, the form saves" proves nothing.
   The oracle has to be observable and specific.
3. **Over-generating.** Twenty cases for a filter. Each one costs review and
   later automation time. The matrix bounds the count.
4. **Burying ambiguity.** An open question written in the doc but not raised
   with the user gets answered by whoever automates it, badly.
5. **Duplicating unit coverage.** If a hook test already proves the clamp, the
   e2e case for it is waste.

## Done When

- `playwright/tests/<squad>/cases/<TICKET>-<feature>.md` exists and follows
  `references/case-template.md`.
- Grounding, requirements, risks, matrix, cases, oracles, and coverage analysis
  are all present.
- The matrix predates the cases.
- Grounding greps report zero `MISSING`.
- Open questions were raised with the user in the reply, not only in the file.
