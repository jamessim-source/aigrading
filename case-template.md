# Test-case document template

Copy this skeleton into `playwright/tests/<squad>/cases/<TICKET>-<feature>.md`.
Every section is required. A section with nothing in it says "None" plus one
line of why - an empty heading is indistinguishable from a forgotten one.

Every value below is an illustrative placeholder. Replace all of them with what
Step 1 actually found in the source - the selectors and copy shown here do not
exist.

---

```markdown
# <TICKET-ID> - <Feature name>

| | |
|---|---|
| Ticket | [LT-XXXXXX](https://manabie.atlassian.net/browse/LT-XXXXXX) |
| Squad | syllabus |
| Feature area | domains/ToReview/modules/grading-score |
| Source of truth | ticket description / PRD link / bug report / commit range |
| Status | Draft \| Reviewed \| Approved |
| Last updated | YYYY-MM-DD |

## 1. Grounding

What was verified against the source, with paths. If the feature is not built
yet, say so here.

| Item | Value | Source |
|---|---|---|
| Environment | Staging, School Admin account. Feature flags run at their latest value (ON); feature configs default to `true`. Cases needing a config flipped say so and require a request first | team convention |
| Route | `/to_review` | `src/squads/syllabus/routing/routings.ts` |
| Route gating | permission `to_review.read` + flag `Syllabus_ToReview` | `routing/useCheckFeatureAndPermissionFlag.ts` |
| Feature flag | `Features.SYLLABUS_...` (useFeatureToggle) | `common/constants/feature-keys.ts` |
| Feature config | `syllabus.<area>.<key>` (useFeatureSettingConfig) | `@core/feature-setting/hooks/useShowRawScoreSetting.ts` |
| Permissions used | `canApprove`, `canMark` | `domains/ToReview/hooks/useToReviewPermission.ts` |
| Roles in scope | School Admin, Teacher | `internals/permission/` |
| Key selectors | `GradingScore__approveButton`, `GradingStatusChip__label` | `domains/ToReview/**/*.tsx` |
| Key copy (EN) | "You have returned submission successfully!" | `i18n/` |
| Existing unit coverage | `domains/ToReview/modules/grading-score/__tests__/` | - |
| Existing e2e | none for this squad yet | `playwright/tests/syllabus/` |

## 2. Requirements

### Entities
- **Submission** - states: `SUBMISSION_STATUS_TO_MARK`, `SUBMISSION_STATUS_MARKED`,
  `SUBMISSION_STATUS_COMPLETED` (take the real enum from `__generated__/proto/`)
- **Marker** - a staff user allocated to a submission

### Business rules
1. ...

### Explicit requirements
- **[REQ-1]** ...
- **[REQ-2]** ...

### Implicit requirements (inferred - confirm before treating as spec)
- **[IMP-1]** ... - Basis: ...

## 3. Risks, invariants, open questions

### Risks
| Risk | Likelihood | Impact | Source |
|---|---|---|---|
| Double-click fires the approve mutation twice | Medium | High | REQ-1 |

### Invariants
- **[INV-1]** A submission's score never exceeds its `maxScore`.
- **[INV-2]** An approved submission cannot be approved again.

### Open questions
1. Is the Approve button hidden or disabled when the user lacks permission?
2. ...

### Edge cases (BOUNDARIES)
| | Case | Input | Expected | Risk |
|---|---|---|---|---|
| B | Score equals maxScore | score = maxScore | accepted | high |
| N | Submission list empty | 0 submissions | empty state renders | medium |
| A | Teacher not allocated as marker | other marker's submission | not visible in list | high |
| ... | Considered, no case: U (no free-text input in this flow) | | | |

## 4. Coverage matrix

| ID | Req | Case | Category | Priority | Oracle type |
|---|---|---|---|---|---|
| TC-001 | REQ-1 | Approve a marked submission | Happy | P0 | UI: status chip = "Approved" |
| TC-002 | REQ-1 | Approve fails server-side | Error | P0 | UI: error snackbar, status unchanged |

## 5. Test cases

### TC-001 - Approve a marked submission

- **Requirement:** REQ-1
- **Category:** Happy path
- **Priority:** P0

```gherkin
Given I am logged in as a School Admin
  And the feature config "syllabus.<area>.<key>" is enabled
  And a submission "[Don't touch] E2E Submission 01" is in SUBMISSION_STATUS_MARKED
  And that submission is allocated to me
  And I am on "/to_review"
When I approve the submission "[Don't touch] E2E Submission 01"
Then a success message "<real English string from i18n>" is shown
  And the submission status reads "Approved"
  And the submission no longer appears in the To Review list after reload
```

- **Test data:** submission `[Don't touch] E2E Submission 01`, course
  `[Don't touch] E2E Course`
- **Oracles:**
  - Positive: `GradingStatusChip__label` text = "Approved"; success snackbar text
  - Negative: no error snackbar; `GradingScore__approveButton` is no longer rendered
- **Notes:** related to TC-002 (failure path)

### TC-002 - ...

## 6. Coverage analysis

- Requirements with no negative case: none
- Invariants with no direct case: none
- Risks with no case: `<risk>` - deferred, needs backend seeding support
- Potential duplicates: none
- BOUNDARIES letters deliberately skipped: U, E - no text input, single locale
  in scope for this ticket
- Deliberately left to unit tests: score clamping (covered by
  `useControlGradingScore.test.ts`)

## 7. Sign-off

| Case | Verdict | Reviewer | Note |
|---|---|---|---|
| TC-001 | KEEP | | |
| TC-002 | DEFER | | blocked on open question 1 |
```

---

## Field rules

- **Case IDs** are `TC-001`, three digits, never reused inside one document.
- **Requirement IDs** are `REQ-n` (stated) and `IMP-n` (inferred). Invariants are
  `INV-n`.
- **Verdicts**: `KEEP` (ready to automate) · `MODIFY` (fix the listed issue) ·
  `REJECT` (wrong, or already covered) · `DEFER` (blocked on an open question).
- **Copy** in a `Then` line is the real English sentence from `i18n/`, in quotes.
  Never the i18n key, never a paraphrase.
- **Fixture data** follows the existing e2e convention: `[Don't touch]` prefix on
  shared records, emails on `example.com`, no `test@test.com`, no `John Doe`.

### Gherkin rules

- **Exactly one `When` per case.** Two actions that both need verifying means two
  cases. This is the rule that keeps cases automatable one-to-one.
- **`Given` carries the whole world**: role, flag state, config state, seeded
  data, and the starting URL. Continuation lines use `And`, indented two spaces.
  No `Given` may describe an unreachable state.
- **`When` is one user action in business language** - "I approve the
  submission", not "I click `GradingScore__approveButton`". Selectors belong in
  the Oracles block, not in the `When`.
- **`Then` is what the user observes**, and it is the outcome, not the mechanism.
  Use `But` for a negative outcome if it reads better than `And ... not ...`.
- **No `Given` in a `Then`.** If a case needs a second setup halfway through, it
  is two cases, or the first case's `Given` is incomplete.
- Write in first person present (`I am on ...`, `I approve ...`) and keep it
  consistent across the whole document.
