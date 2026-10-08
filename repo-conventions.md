# Repository conventions for Playwright

Everything here is read from `playwright.config.ts`, `playwright/` and
`package.json`. If one of these facts stops being true, fix this file.

## Layout

```
playwright.config.ts
playwright/
├── auth_lmsv2.setup.ts          storageState for the main (lmsv2) tenant
├── auth_jprep.setup.ts          storageState for the JPREP tenant
├── auth_sf_official.setup.ts    Salesforce full-time staff
├── auth_sf_community.setup.ts   Salesforce part-time staff
├── .auth/                       generated storageState json
├── page-locator/                shared classes: LoginPage, Snapshot
├── tests/<squad>/               specs for the lmsv2 tenant
│   ├── <feature>.spec.ts
│   ├── cases/                   markdown test-case documents (never .spec.ts)
│   ├── fixtures/                CSV / media used by the specs, colocated
│   └── __screenshots__/         generated baselines; git-ignored, so new ones stay local
└── tests-jprep/<squad>/         specs for the JPREP tenant
```

Existing spec files: `tests/auth/login-manabie.spec.ts`,
`tests/user/{user-group,student-mgmt,staff-mgmt}.spec.ts`,
`tests/architecture/{sidebar-layout,layout-common}.spec.ts`,
`tests/communication/{chat,notification}.spec.ts`.

Fixture files are colocated, following `tests-jprep/lesson/video.mov`.

## Config facts

| Setting | Value | Consequence |
|---|---|---|
| `testDir` | `./playwright` | every `.spec.ts` anywhere under `playwright/` is collected, including inside `cases/` |
| `baseURL` | `process.env.E2E_BASE_URL ?? "https://backoffice.staging.manabie.io/"` | specs run against shared, mutable staging by default |
| `timeout` | `600000` (10 min per test) | generous; do not add per-action timeouts to "be safe" |
| `expect` default | Playwright's 5 s | raise per-assertion only for a known-slow wait, e.g. `{ timeout: 60_000 }` for a polled job |
| `workers` | `1` | tests run one at a time, but each still gets a fresh context - isolation is still required |
| `fullyParallel` | `true` | irrelevant at `workers: 1`, but do not rely on ordering |
| `retries` | `2` on CI, `0` locally | a test that only passes on retry is flaky, not passing |
| `forbidOnly` | `!!process.env.CI` | a committed `test.only` fails the build |
| `reporter` | `html` | `npx playwright show-report` after a run |
| `trace` | `undefined` | no trace by default; add `--trace on` to the command when debugging |
| `snapshotPathTemplate` | `{testDir}/{testFileDir}/__screenshots__/{arg}{ext}` | screenshot names derive from the test title; `__screenshots__/` is git-ignored, so a new spec's baselines are local-only |
| `@playwright/test` | `1.55.1` | anything from 1.56+ (Test Agents, Screencast API, `locator.drop()`) does not exist here |

## Projects and auth

| Project | Runs | storageState | Notes |
|---|---|---|---|
| `auth_lmsv2` | `auth_lmsv2.setup.ts` | writes `playwright/.auth/user_lmsv2.json` | dependency of `lmsv2` |
| `lmsv2` | everything under `playwright/` **except** `tests-jprep/**` and `tests/auth/**` | reads `user_lmsv2.json` | the default project for a new squad spec |
| `auth` | `playwright/tests/auth/**` | none | login flow itself, so no saved session |
| `auth_jprep` → `jprep` | `playwright/tests-jprep/**` | `user_jprep.json` | different `baseURL` |
| `auth_sf_official` / `auth_sf_community` | Salesforce setups | - | no test project consumes them yet |

**A new spec at `playwright/tests/<squad>/<feature>.spec.ts` is picked up by
`lmsv2` with no config change.** It starts already logged in as
`diemquynh.vu+lmsv2admin@manabie.com` on the `lmsv2` organisation - a School
Admin. Never call `LoginPage` from a spec under `tests/<squad>/`.

`auth_lmsv2.setup.ts` also seeds `manabie_SORTED_LOCATIONS_TYPES` into
localStorage (org / Brand A / Center A1 / Center A2). Location pickers in a spec
see those values.

## Running

```bash
# one file
yarn test:e2e --project=lmsv2 playwright/tests/syllabus/master-study-plan.spec.ts

# one test by title
yarn test:e2e --project=lmsv2 -g "TC-008"

# headed, stepping through
yarn test:e2e --project=lmsv2 --headed --debug playwright/tests/syllabus/master-study-plan.spec.ts

# discovery only, no browser
yarn test:e2e --list --project=lmsv2 playwright/tests/syllabus/

# against a local dev server instead of staging
E2E_BASE_URL=http://localhost:4012 yarn test:e2e --project=lmsv2 ...

# refresh local screenshot baselines after a deliberate UI change
# (they are git-ignored, so this only affects your working tree)
yarn test:e2e --project=lmsv2 --update-snapshots playwright/tests/syllabus/

# open the report from the last run
npx playwright show-report
```

`--debug` and `--headed` are local only. `page.pause()` is never committed.

## Test titles

Existing titles: `[User]UserGroup mgmt page`, `[Comm] Notification`,
`[Comm] Notification Detail`, `[Arch] LocationSettings`,
`[JPREP-Syllabus] Upload lesson media`.

For a new spec derived from a case document, carry the case ID:

```typescript
test("[Syllabus] TC-008 Import a valid CSV", async ({ page }) => { ... });
```

The title feeds `snapshotPathTemplate`, so `[Syllabus] TC-008 Import a valid CSV`
produces `__screenshots__/-Syllabus-TC-008-Import-a-valid-CSV-1.png` locally.
Those files are git-ignored, so a rename costs nothing beyond a stale PNG in your
own working tree.

## Page-locator classes

`playwright/page-locator/` holds only what more than one spec uses. Current
contents: `LoginPage` (login, organisation, language switch, SF and JPREP
variants) and `Snapshot`.

Style, copied from `LoginPage`:

- constructor takes `private page: Page` from `"playwright"` (not
  `"@playwright/test"`), reassigns `this.page`, and binds every method it
  exposes;
- methods return the locator promise directly when they are a single action;
- **no `expect`** anywhere in the class.

## Snapshot, and why it is not an assertion

```typescript
async takeScreenshot() {
    ...
    try {
        await expect(await this.page).toHaveScreenshot({ fullPage: true, timeout: 100000 });
    } catch (e) {
        console.error(e);   // <- the failure dies here
    }
}
```

A screenshot mismatch logs to the console and the test still passes. **So
`toHaveScreenshot` asserts nothing in this repo**, baseline or no baseline.

`playwright/**/__screenshots__/` is also git-ignored. The 41 baselines committed
before that rule remain tracked; anything a new spec generates stays on your
machine, so the first run elsewhere writes a fresh baseline and compares it
against itself.

`Snapshot` gives you a visual record while debugging locally, plus a "the page
rendered without throwing" smoke check. It is not an oracle. Every case still
needs a real `expect`.

If a case genuinely needs visual regression, that is a change to `Snapshot`
(drop the `try/catch`) plus a decision about committing baselines. Raise it; do
not work around it in a spec.

`goToAndTakeScreenshot({ url, cb })` navigates, waits for the URL, runs `cb` and
screenshots. It also hides `import-map-overrides-full` before shooting, which is
why full-page screenshots are stable in this app.

## Staging is shared

Other engineers and other suites use the same tenant at the same time.

- Never assert an absolute count on a shared list.
- Scope every assertion to a record the test itself created, or to a
  `[Don't touch]`-prefixed fixture nobody edits.
- A test that creates data (an import job, an export request) leaves it behind.
  That is accepted here - there is no teardown - so the assertion must survive
  the residue of every previous run.
- Fixture naming follows the existing convention: `[Don't touch]` prefix on
  shared records, emails on `manabie.com` or `example.com`.
