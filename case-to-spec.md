# From a test case to a spec

## The mapping

| Case document | Spec |
|---|---|
| `### TC-008 - Import a valid CSV` | `test("[Syllabus] TC-008 Import a valid CSV", ...)` |
| `Given the standard world` | nothing - `storageState` already logged you in as School Admin |
| `Given I am on "/study_plan_management"` | `await page.goto("/study_plan_management")` |
| `Given I have opened "Import..."` | setup actions before the `When`, wrapped in `test.step("setup")` when there is more than one |
| the single `When` | exactly one action, the last action before the assertions |
| each `Then` / `And` / `But` line | one `expect` |
| **Oracles → Positive** | the assertions that prove it happened |
| **Oracles → Negative** | the assertions that prove the failure path did not |
| **Test data** | `[Don't touch]` fixture names as constants at the top of the file |
| **Notes** | a code comment only when it explains a non-obvious locator or wait |

Rules that carry over unchanged from the case document: one `When` per test, no
setup after an assertion, real English copy in every expected string.

## Worked example

Source case, from `playwright/tests/syllabus/cases/LT-106024-bulk-import-master-study-plan.md`:

```gherkin
Given the standard world
  And I have opened "Import Master Study Plan Structure"
  And I have replaced the "All Courses" chip with "[Don't touch] E2E Course Math G9" and "[Don't touch] E2E Course English G9"
When I click "Download Template File"
Then a CSV file whose name starts with "import_master_study_plan_" is downloaded
  And a success message "Template downloaded successfully." is shown
```

Oracles: filename matches `import_master_study_plan_\d{8}_\d{6}\.csv`, success
snackbar text; negative - no error snackbar.

The spec:

```typescript
import { expect, test } from "@playwright/test";

const COURSE_MATH = "[Don't touch] E2E Course Math G9";
const COURSE_ENGLISH = "[Don't touch] E2E Course English G9";

test("[Syllabus] TC-003 Download the template for two named courses", async ({ page }) => {
    await test.step("open the import dialog with two named courses", async () => {
        await page.goto("/study_plan_management");
        // MButtonDropdown has no data-testid; addressed by its label
        await page.getByText("Master Study Plan").click();
        await page.getByRole("menuitem", { name: "Import Master Study Plan Structure" }).click();
        await expect(page.getByTestId("MasterStudyPlanImportDialog__root")).toBeVisible();

        const courseField = page.getByTestId("CourseLocationOrderByAutocompleteHF__root");
        await courseField.getByRole("button", { name: "All Courses" }).getByTestId("CancelIcon").click();
        for (const course of [COURSE_MATH, COURSE_ENGLISH]) {
            await courseField.getByRole("combobox").fill(course);
            await page.getByRole("option", { name: course }).click();
        }
    });

    const downloadPromise = page.waitForEvent("download");
    await page
        .getByTestId("MasterStudyPlanImportTemplateSection__downloadTemplateButton")
        .click();
    const download = await downloadPromise;

    expect(download.suggestedFilename()).toMatch(/^import_master_study_plan_\d{8}_\d{6}\.csv$/);
    await expect(page.getByTestId("SnackbarBase__content"))
        .toHaveText("Template downloaded successfully.");
    await expect(page.getByText("Failed to download template. Please try again."))
        .toBeHidden();
});
```

What that example is demonstrating:

- setup collapses into one `test.step`, so the trace reads as setup / action /
  assertions and the single `When` is unmistakable;
- the download listener is registered **before** the click - registering it after
  loses the event;
- both oracles became assertions, including the negative one;
- the one non-testid locator carries a comment;
- fixture names are constants, so a renamed fixture is a one-line change.

## Recurring patterns

### Download

```typescript
const downloadPromise = page.waitForEvent("download");
await page.getByTestId("Something__downloadButton").click();
const download = await downloadPromise;

expect(download.suggestedFilename()).toMatch(/\.csv$/);

// only when the case's oracle is about file contents
const stream = await download.createReadStream();
const body = (await stream.toArray()).join("");
expect(body.replace(/^﻿/, "").split("\n")[0]).toContain("ex_course_id");
```

### Upload

Every upload in this app goes through `@share/components/Upload`, which wraps
mana-ui's `MUploadInput`. The hidden field carries `MUploadInput__inputFile` and
the attached file renders as `Upload__chip-{index}` - use those, not a raw
`input[type="file"]` selector and not a click on the label.

Fixture files live next to the spec, e.g.
`playwright/tests/syllabus/fixtures/valid-msp.csv`:

```typescript
await page
    .getByTestId("StudyPlanUpload__root")
    .getByTestId("MUploadInput__inputFile")
    .setInputFiles("playwright/tests/syllabus/fixtures/valid-msp.csv");

await expect(page.getByTestId("Upload__chip-0")).toBeVisible();
await expect(page.getByTestId("MasterStudyPlanImportDialog__importButton")).toBeEnabled();
```

When the file only exists to be rejected, build it inline instead of committing
a fixture nobody reads - the dropzone checks the name and MIME type, never the
bytes:

```typescript
await page.getByTestId("MUploadInput__inputFile").setInputFiles({
    name: "master-study-plan.xlsx",
    mimeType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    buffer: Buffer.from("ex_course_id,ex_msp_id\n"),
});
```

`MUploadInput` wires react-dropzone's `onDropAccepted` only, so a rejected file
never reaches the app: there is no error message to assert, and the oracle is
that no chip appeared and the drag-and-drop prompt is still on screen.

### Dialog open / close

```typescript
await expect(page.getByTestId("MasterStudyPlanExportDialog__root")).toBeVisible();
// ... action ...
await page.getByTestId("MDialogCustom__footer").getByText("Cancel").click();
await expect(page.getByTestId("MasterStudyPlanExportDialog__root")).toBeHidden();
```

### A row in a table the test just created

Never index. Filter by something the test owns:

```typescript
const row = page
    .getByTestId("MasterStudyPlanImportTable__root")
    .getByRole("row")
    .filter({ hasText: COURSE_MATH });

await expect(row.getByTestId("MasterStudyPlanImportStatusChip__root")).toHaveText("Processing");
```

### A polled job settling

The list refetches every 10 s while any row is pending, then stops. Do not sleep
through it - assert the end state with a raised timeout.

```typescript
await expect(row.getByTestId("MasterStudyPlanImportStatusChip__root"))
    .toHaveText("Completed", { timeout: 120_000 });
```

Keep at most one of these per spec file. Two turn a run into four minutes of
waiting.

### A snackbar

Snackbars auto-dismiss. Assert immediately after the action that raises them,
before any further interaction.

```typescript
await expect(page.getByTestId("SnackbarBase__content")).toHaveText("<exact copy>");
```

### A screenshot alongside real assertions

```typescript
import { Snapshot } from "../../page-locator/Snapshot";

const snapshot = new Snapshot(page);
await snapshot.takeScreenshot();   // local visual record only - asserts nothing
```

Never the only oracle in a test. Baselines are git-ignored and `Snapshot`
swallows its own failures. See the Snapshot warning in `repo-conventions.md`.

## Cases that do not become specs

Say which, and why, in the reply. Recurring reasons in this repo:

| Case shape | Why not |
|---|---|
| "with the flag off" | staging runs flags at their latest value; the OFF branch is unreachable |
| "with config `x.y.z` disabled" | flipping a feature config changes tenant state for everyone on the environment |
| "the server rejects the request" | needs a seeded backend failure; possible with `page.route` interception, but that stops testing the real integration - flag the trade-off rather than deciding it silently |
| "in Japanese" | the locale switch invalidates the saved session flow; separate spec or skip |
| already proven by a unit test | the case document's Coverage Analysis already says so |
