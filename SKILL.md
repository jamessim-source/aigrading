---
name: e2e
description: >-
  Turn a test-case document or a Jira ticket into Playwright specs that match
  this repository - `playwright/tests/<squad>/*.spec.ts`, the `page-locator`
  classes, staging auth via `storageState`, and BEM `data-testid` locators.
  Use when: "write e2e", "automate these cases", "Playwright spec", "add e2e for
  LT-XXXXXX".
  Not for: writing the cases themselves - use `test-cases` first. Not for: unit
  or integration tests - those are Jest under `src/**/__tests__/`.
---

# E2E Automation

## Overview

The input is a reviewed test-case document. The output is a spec file that runs
against staging. The failure this prevents: a spec written from memory of how
Playwright suites usually look - `e2e/pages/`, `getByRole` everywhere, fixture
factories, `waitForTimeout` to paper over a race. None of that is this repo.
This repo has a fixed layout, an existing auth project, `data-testid` as the
locator contract, and a `Snapshot` helper that silently swallows its own
failures.

**Core principle: the case document decides *what* to assert, the existing
`playwright/` tree decides *how* to write it. Neither is negotiable, and
neither is invented.**

Do not write a spec for a case that does not exist in a document. If the user
hands you a ticket and no cases, run the `test-cases` skill first - a spec
written straight off a ticket has no oracle, only an action.

## Output

```
playwright/tests/<squad>/<feature-slug>.spec.ts        the spec
playwright/tests/<squad>/fixtures/<name>.csv           fixture files, colocated
playwright/page-locator/<Thing>.ts                     only when reused across specs
```

- `<feature-slug>` is kebab-case and names the **feature**, not the ticket:
  `master-study-plan.spec.ts`, not `LT-106024.spec.ts`. The ticket lives in the
  case document; the spec outlives the ticket.
- One spec file per feature. Adding cases for the same screen later appends to
  the existing file.
- `playwright/tests/<squad>/cases/` holds markdown only. Never put a `.spec.ts`
  there - it would be collected and run.

## Pipeline

```
1 Source   → locate the case document; no document, no spec
2 Ground   → re-verify every selector, route and copy string still exists
3 Select   → decide which cases automate now, and say which do not
4 Locators → reuse page-locator; add to it only for cross-spec reuse
5 Write    → one test() per TC, one When per test, oracles become expects
6 Run      → actually execute against staging
7 Verify   → ban greps, typecheck, traceability
```

Steps 1-3 are cheap and are not optional. Step 6 is what separates a spec from
a plausible-looking file.

### Step 1: Source

Find `playwright/tests/<squad>/cases/<TICKET>-*.md`. Read the Grounding table,
the Coverage matrix and the Sign-off table.

- Cases with verdict `KEEP` are in scope.
- `DEFER` / `REJECT` / `MODIFY` are not automated. Say so in the reply.
- No document and the user gave a ticket → run `test-cases` first, then return.

### Step 2: Ground again

The document was written at a point in time; `develop` has moved. Before
writing, confirm against source:

| Check | How |
|---|---|
| Every `Block__element` in the doc still exists | `grep -rn "MasterStudyPlanImportDialog__importButton" src/squads/<squad>` |
| The route is still the route | `src/squads/<squad>/routing/routings.ts` |
| Quoted English copy is still the copy | `grep -rn "Template downloaded successfully." src/squads/<squad>/i18n/source/cms_en.ts` |
| Testids the doc flags as composed at runtime | build the same string the source builds; do not expect a literal |

Anything that moved: fix the case document in the same change, do not silently
write the spec against the new value. The document is the reviewed artifact.

### Step 3: Select

Not every `KEEP` case is worth automating today. Skip, and state why:

- **Backend-shaped outcomes** - a case whose oracle is "the server rejects it"
  needs a seeded failure. Skip unless staging can produce it on demand.
- **Long-running jobs** - a case that waits on a 10 s poll loop to settle is
  automatable but slow; keep it, mark it, do not put five of them in one file.
- **Locale variants** - the app switches language through the UI
  (`LoginPage.changeLanguage`), which invalidates the saved `storageState`
  session flow. Treat JA cases as a separate spec, or skip.
- **Anything a unit test already proves.** The document's Coverage Analysis
  already lists these. Do not re-litigate.

### Step 4: Locators

`playwright/page-locator/` holds shared classes only (`LoginPage`, `Snapshot`).
The bar for adding a file there is **used by two or more spec files**. A
locator used once lives in the spec.

Class style, matching `LoginPage`:

```typescript
import type { Page } from "playwright";

export class StudyPlanManagementPage {
    constructor(private page: Page) {
        this.page = page;
        this.openMasterStudyPlanMenu = this.openMasterStudyPlanMenu.bind(this);
    }

    openMasterStudyPlanMenu() {
        return this.page.getByText("Master Study Plan").click();
    }
}
```

**No `expect` inside a page-locator class.** A failure must point at the test,
not at the helper. `Snapshot` is the existing exception and it is a bad one -
see the Snapshot warning below.

### Step 5: Write

One `test()` per case, in case-ID order. Title carries the squad and the case
ID so a failure names the row it came from:

```typescript
test("[Syllabus] TC-008 Import a valid CSV", async ({ page }) => { ... });
```

Map the Gherkin literally. `Given` becomes navigation and setup, the single
`When` becomes one action, each `Then` line becomes one `expect`. If a spec
grows a second logical action that needs verifying, the case document is wrong
- fix it there first, do not fold two cases into one test.

Full mapping table and a worked example: `references/case-to-spec.md`.
Locator hierarchy, waiting rules and the ban list: `references/selectors-and-waiting.md`.
Config, projects, auth and run commands: `references/repo-conventions.md`.

### Step 6: Run

```bash
yarn test:e2e --project=lmsv2 playwright/tests/<squad>/<feature>.spec.ts
```

A spec that has never run is a draft. Run it, read the failure, fix the spec -
not the assertion. Changing an expected value to match what the app printed is
how a suite stops testing anything.

If staging is unreachable or the account is locked, say so plainly and hand
over the spec as unrun. Do not report it as passing.

### Step 7: Verify

```bash
# banned synchronisation and debug leftovers - all three must print nothing
grep -rn "waitForTimeout\|page.pause()\|test.only" playwright/

# every test parses and is discovered (esbuild transpile - catches syntax and bad imports)
yarn test:e2e --list --project=lmsv2 playwright/tests/<squad>/

# format and lint - biome covers playwright/, and lint-staged runs it on commit
yarn biome:lint:fix && yarn biome:formatter:fix
```

`playwright/` is **not** in any `tsconfig.json` include list, so
`yarn typecheck:unit` does not see the specs and Playwright does not type-check
at run time. `--list` is the only cheap structural check you get. To actually
type-check a new spec:

```bash
npx tsc --noEmit --skipLibCheck --esModuleInterop --target es2020 \
  --module esnext --moduleResolution node --jsx preserve \
  playwright/tests/<squad>/<feature>.spec.ts
```

Then the checklist:

- [ ] Every `test()` title carries a `TC-` id that exists in the case document.
- [ ] Every case-document oracle became an `expect`, positive **and** negative.
- [ ] Exactly one user action per test.
- [ ] No test depends on another having run first, or on a row a previous test
      created.
- [ ] No raw CSS/xpath locator without a one-line comment saying why.
- [ ] Expected strings are the real English copy from `i18n/`, not paraphrases.
- [ ] Fixture records use the `[Don't touch]` prefix.
- [ ] The spec ran, and the reply says which cases were skipped and why.

## Repo facts you must not re-derive

Details in `references/repo-conventions.md`; the load-bearing ones:

- `testDir` is `./playwright`, so **any** `.spec.ts` under it is collected.
- `baseURL` defaults to `https://backoffice.staging.manabie.io/`, overridable
  with `E2E_BASE_URL`. Tests are written against **shared, mutable staging**.
- Auth is the `auth_lmsv2` setup project writing
  `playwright/.auth/user_lmsv2.json`; the `lmsv2` project replays it. A new spec
  under `playwright/tests/<squad>/` is picked up with no config change. Never
  log in inside a test.
- `workers: 1`, `retries: 2` on CI. Serial execution is not isolation - each
  test still gets a fresh context and must stand alone.
- Playwright is pinned at **1.55.1**. APIs added after that do not exist here.
- `eslint-plugin-playwright` is not installed. The bans are enforced by the
  greps in Step 7, by you.

### The Snapshot warning

`playwright/page-locator/Snapshot.ts` wraps `toHaveScreenshot` in a
`try/catch` that logs and swallows. **A screenshot mismatch does not fail the
test.** Every existing spec in this repo is therefore a smoke test that proves
the page rendered without throwing, not that it rendered correctly.

On top of that, `playwright/**/__screenshots__/` is git-ignored, so a **new**
spec's baselines never leave your machine and the first run anywhere else
writes a fresh one and compares it against itself. (The 41 baselines committed
before that rule stay tracked; the rule only stops new ones.)

Use `Snapshot` as a local visual record alongside real assertions. Never as a
case's only oracle - a case whose only `Then` is a screenshot is a case that
always passes.

## Anti-Patterns

1. **Writing the spec from the ticket.** The ticket has actions, not oracles.
   The case document exists precisely to close that gap.
2. **Importing the reference layout.** `e2e/pages/`, `base.fixture.ts`,
   `global-setup.ts` - none of that is here, and adding it strands the new spec
   away from the four that already work.
3. **`getByRole` reflex.** This is an MUI app with BEM testids as the deliberate
   test contract. `getByTestId` is first choice here, not last resort.
4. **Asserting on shared staging counts.** "The import list has 3 rows" is true
   until somebody else runs the same test. Scope every assertion to the record
   the test itself created.
5. **A snackbar assertion with no negative half.** Success text visible proves
   the happy path fired; it does not prove the error path did not.
6. **Copying `.nth(1)` from the existing specs.** It is positional and breaks on
   any reorder. `filter({ hasText })` instead.

## Red Flags

| Thought | Reality |
|---|---|
| "I'll just add a short wait here" | `waitForTimeout` is zero in this repo today. Keep it there. Find the right locator. |
| "There's no case for this but it's obviously needed" | Then the case document is incomplete. Fix it there, then automate. |
| "I'll set up fixtures properly while I'm here" | Out of scope. Four working specs use none. |
| "The screenshot will catch it" | `Snapshot` swallows its own failures. It catches nothing. |
| "I'll log in at the start of the test" | `storageState` already did. A UI login per test is the slowest possible bug. |
| "Staging returned something different, I'll update the expectation" | That is a finding, not a fix. Report it. |
| "This case needs a flag turned off" | Staging runs flags at their latest value. That case is unautomatable here - say so. |

## Done When

- The spec exists at `playwright/tests/<squad>/<feature>.spec.ts`, one `test()`
  per automated case, each titled with its `TC-` id.
- Step 7's three greps print nothing and `tsc --noEmit` passes.
- The spec has actually been run and the result reported honestly.
- Cases that were not automated are listed in the reply with a reason each.
- Any drift found in Step 2 was written back into the case document.
