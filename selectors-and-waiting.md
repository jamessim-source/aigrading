# Selectors, waiting, and the ban list

## Locator hierarchy for this app

Generic Playwright guidance puts `getByRole` first and `getByTestId` last. That
ordering assumes an app where test ids were sprinkled on as an afterthought.
This app does the opposite: BEM `data-testid` attributes are a deliberate,
enforced convention (`Block__element`), and the test-case documents ground their
oracles on them. So:

1. **`getByTestId("Block__element")`** - first choice. It is the contract.
2. **`getByRole` / `getByLabel`** - when the element has no testid but a real
   role, e.g. MUI menu items are `role="menuitem"`.
3. **`getByText("<real English copy>")`** - for elements labelled only by copy.
   The string must be the exact sentence from `src/squads/<squad>/i18n/source/cms_en.ts`.
4. **`page.locator('[attr="value"]')`** - last resort, for `placeholder`,
   `href`, `aria-label`, `data-value`. Requires a one-line comment saying why.

Never: xpath, CSS class names, `nth-child`, structural descendant chains.

### Scope before you index

```typescript
// BAD - positional, breaks the moment a row is added or reordered
await page.getByTestId("ActionPanel__trigger").nth(1).click();

// GOOD - scoped to the thing you actually mean
await page
    .getByTestId("MasterStudyPlanImportTable__root")
    .getByRole("row")
    .filter({ hasText: "[Don't touch] E2E Course Math G9" })
    .getByTestId("MasterStudyPlanImportStatusChip__root")
    .click();
```

The existing specs use `.nth()` and `.first()`. That is legacy, not a pattern to
copy. Chain `getByTestId(root).getByTestId(child)` or `filter({ hasText })`.

### Composed test ids

Some testids are built at runtime, e.g. the export table cells are
`` `MasterStudyPlanExportTable__${key}` `` with `key` in `startDateTime`,
`status`, `download`, `note`. They never appear as literals in the source, so a
grep for them fails. Build the same string the source builds, and note in the
spec where it comes from.

### When there is no testid

The case document flags these as a "Selector gap". Address the element by its
visible English copy and leave the gap in place - **do not edit source to add a
testid** just to make a spec easier to write. That is a separate change with its
own review.

```typescript
// MButtonDropdown carries no data-testid; addressed by its label
await page.getByText("Master Study Plan").click();
await expect(page.getByRole("menuitem")).toHaveText([
    "Import Master Study Plan Structure",
    "Export Master Study Plan Structure",
]);
```

## Waiting

Every Playwright action and every `expect(locator)` assertion auto-waits. If you
reach for a wait, you have the wrong locator or the wrong assertion.

| Situation | Do this |
|---|---|
| Element will appear | `await expect(locator).toBeVisible()` |
| Element will disappear | `await expect(locator).toBeHidden()` |
| Navigation | `await expect(page).toHaveURL("/study_plan_management")` |
| Text will settle to a value | `await expect(locator).toHaveText("Completed")` |
| A list will fill | `await expect(rows).toHaveCount(n)` - only for a list the test owns |
| A polled job settles (10 s refetch) | `await expect(chip).toHaveText("Completed", { timeout: 60_000 })` |
| A download fires | `page.waitForEvent("download")` started *before* the click |

`await page.waitForLoadState("networkidle")` exists in the auth setup files. It
is acceptable in a setup file, where there is nothing to assert on yet. In a
spec, assert on a locator instead.

### Banned

```typescript
await page.waitForTimeout(2000);   // zero occurrences in this repo. Keep it that way.
await page.pause();                // local debugging only, never committed
test.only(...)                     // forbidOnly fails the CI build
locator.click({ force: true });    // hides an actionability failure
```

`force: true` has exactly one accepted use in this repo - `LoginPage.enterLoginType`
on an MUI select that intercepts pointer events. Any new use needs a comment
naming the specific widget behaviour it works around.

## Assertions

Web-first assertions retry; `expect(await locator.textContent())` does not.

```typescript
// BAD - single shot, races the render
expect(await page.getByTestId("Chip__label").textContent()).toBe("Completed");

// GOOD - retries until it holds or the timeout expires
await expect(page.getByTestId("Chip__label")).toHaveText("Completed");
```

Each case in the document lists positive **and** negative oracles. Both become
assertions:

```typescript
// positive
await expect(page.getByTestId("SnackbarBase__content"))
    .toHaveText("Template downloaded successfully.");
// negative
await expect(page.getByText("Failed to download template. Please try again."))
    .toBeHidden();
```

`SnackbarBase__content` (`src/components/Snackbars/`) is the shared snackbar
body used across squads. Snackbars auto-dismiss - assert on them before the next
action, not after.

Use `expect.soft` only when a case genuinely has several independent
observations and you want all failures in one run. Default to hard assertions.

## Shared test ids worth knowing

Verified in `src/components/` and reused by the existing specs:

| Test id | What it is |
|---|---|
| `SnackbarBase__content` | snackbar message body |
| `WrapperSnackbar__container` | multi-item snackbar container |
| `DialogCustom__root`, `MDialogCustom__footer` | dialog shell and footer button row |
| `ActionPanel__trigger`, `ActionPanel__menuList` | row action menu; items carry `aria-label` |
| `TableBase__noDataMessage` | empty-state row |
| `LocaleSwitcher` | language switch on the login screen |

Menu items inside `ActionPanel__menuList` are addressed by `aria-label`:

```typescript
await page.getByTestId("ActionPanel__trigger").click();
await page.locator(`[data-testid="ActionPanel__menuList"] [aria-label="Edit"]`).click();
```

Anything else: grep the squad's `.tsx` files. Do not guess a name from the
component name - `MasterStudyPlanImportDialog__importButton` and
`MasterStudyPlanImportTemplateSection__downloadTemplateButton` are not derivable.
