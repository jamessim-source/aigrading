---
paths:
  - "**/*.test.tsx"
  - "**/*.test.ts"
---

# Testing guidelines

## Use `userEvent`, not `fireEvent`

When writing or editing React Testing Library tests, prefer `userEvent`
(from `@testing-library/user-event`) over `fireEvent`
(from `@testing-library/react`) for any interaction a real user would perform:
click, type, hover, focus, tab, select, etc.

`fireEvent` dispatches a single raw DOM event. `userEvent` dispatches the full
sequence of events the browser fires for a real interaction (a click also fires
focus, mousedown, mouseup; typing fires keydown/keypress/input/keyup per char).
This catches event-handling bugs that `fireEvent` hides and keeps tests close to
real behaviour.

```tsx
// Good
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/react";

it("saves on click", async () => {
    render(<MyComponent />);
    await userEvent.click(screen.getByRole("button", { name: "Save" }));
});

// Bad
import { fireEvent, render, screen } from "@testing-library/react";

it("saves on click", () => {
    render(<MyComponent />);
    fireEvent.click(screen.getByRole("button", { name: "Save" }));
});
```

- `userEvent` interactions are async — always `await` them and mark the test `async`.
- Import as the default export: `import userEvent from "@testing-library/user-event"`.
- Drop `fireEvent` from the `@testing-library/react` import once it is no longer used.
- Reserve `fireEvent` only for events that have no `userEvent` equivalent (rare).

## Do not mock `useTranslate` in unit tests

Do NOT add `jest.mock("src/squads/syllabus/hooks/useTranslate/useTranslate")` to
new unit tests. The real `syllabusPolyglot` already returns English under Jest,
so `useTranslate()` works out of the box — and returns actual translated
strings, not the key verbatim.

`src/squads/syllabus/i18n/polyglot.ts` defaults to English in the test
environment (`import.meta.env.NODE_ENV === "test" ? LanguageEnums.EN`).
`setupTests.ts` resets the polyglot between tests via
`syllabusPolyglot.destroy()` in `afterEach`. There is no global mock of
`useTranslate` — the English strings come from the real polyglot singleton.

- **Hook tests:** `renderHook(() => useMyHook())` with no wrapper is enough —
  the polyglot is a module singleton, not React context.
- **Component tests:** wrap with `TestLanguageWrapper` (from
  `src/squads/syllabus/test-utils/TestLanguageWrapper`) when mounting a full
  component tree that needs `LANG` pinned.
- Assert on the **real English string**. Example:
  `t("commonMessage.unableToLoadData")` → `"Unable to load data, please try again!"`.

Some older suites still auto-mock `useTranslate` (it returns the key verbatim).
Do not copy that pattern into new tests — use the real polyglot so the test
exercises the actual copy.
