---
paths:
  - "src/squads/**/*.tsx"
  - "src/squads/**/*.ts"
---

# Prefer importing from the current squad

When working within a squad (e.g., `src/squads/syllabus`), **prefer importing from the squad's own directories** before importing from shared/common directories.

## Hierarchy (in order of preference)

1. **Squad-local paths** → `src/squads/{squad}/hooks/`, `src/squads/{squad}/common/`, etc.
2. **Shared paths** → `src/hooks/`, `src/common/`, `src/components/`, etc.
3. **External packages** → `@manabie-com/mana-ui`, etc.

## Examples

### ✅ Good (working in `src/squads/syllabus`)

```tsx
// Prefer syllabus's local hook
import useTranslate from "src/squads/syllabus/hooks/useTranslate";
import useShowSnackbar from "src/squads/syllabus/hooks/useShowSnackbar";

// If the squad doesn't have it, then use shared
import { formatDate } from "src/common/utils/date";
```

### ❌ Bad (working in `src/squads/syllabus`)

```tsx
// Don't import from shared if squad has its own
import useTranslate from "src/hooks/useTranslate";
import useShowSnackbar from "src/hooks/useShowSnackbar";
```

## Rationale

- **Encapsulation**: Each squad can have customized versions of hooks/utilities tailored to their domain
- **Independence**: Reduces dependencies on shared code, making squads more self-contained
- **Override capability**: Squads can provide specialized implementations while still using shared code as fallback

## When to use shared code anyway

- No squad-local equivalent exists
- The shared code is intentionally generic/platform-wide (e.g., `ra.common.` translation keys)
- Cross-squad imports (when importing from a different squad, use absolute paths: `src/squads/{other-squad}/...`)

# Import MUI slot class names, never hardcode them

To target a MUI component's inner slot from `sx` or `styled`, import the component's
`*Classes` object and build the selector from it. Never write the class name as a string.

## Why

Each squad prefixes every MUI slot class so its bundle stays isolated
(`src/squads/{squad}/styles/mui-classname-setup.ts` runs
`ClassNameGenerator.configure((name) => \`Mana{Squad}-${name}\`)`).

The monolith dev server does the opposite: `vite.config.ts` strips every
`configure()` call, because all squads share one JS context and only the last call
would win.

So the same source produces two different DOMs:

| Build | Class in the DOM |
|-------|------------------|
| `yarn dev` (monolith) | `MuiChip-label` |
| MFE build (deployed) | `ManaSyllabus-MuiChip-label` |

A hardcoded `"& .MuiChip-label"` matches locally and matches **nothing** once deployed.
The style silently disappears on the server while looking correct on your machine.

## ❌ Bad

```tsx
sx={{
    "& .MuiChip-deleteIcon": { color: "rgba(0, 0, 0, 0.54)" },
    "& .MuiChip-label": { opacity: 0.38 },
    "& .MuiDialog-container": { overflow: "visible" },
}}
```

## ✅ Good

```tsx
import { chipClasses } from "@mui/material/Chip";
import { dialogClasses } from "@mui/material/Dialog";

sx={(theme) => ({
    [`& .${chipClasses.deleteIcon}`]: { color: theme.palette.action.active },
    [`& .${chipClasses.label}`]: { opacity: 0.38 },
    [`& .${dialogClasses.container}`]: { overflow: "visible" },
})}
```

`chipClasses.label` resolves to `MuiChip-label` locally and
`ManaSyllabus-MuiChip-label` on the MFE, so one expression is correct in both builds.

## Import the `*Classes` object from the component path

Use `@mui/material/Chip`, not the `@mui/material` barrel. A babel transform rewrites
barrel imports to deep paths, and paths like `@mui/material/dialogClasses` do not
exist — the Jest resolver fails with `Cannot find module`.

```tsx
// ✅ resolves
import { dialogClasses } from "@mui/material/Dialog";

// ❌ babel rewrites this to @mui/material/dialogClasses, which does not exist
import { dialogClasses } from "@mui/material";
```

## Global state classes are exempt

`Mui-selected`, `Mui-disabled`, `Mui-focusVisible`, `Mui-error`, `Mui-checked` and the
other `Mui-*` state classes are **never** prefixed, so writing them as strings is fine:

```tsx
sx={{ "&.Mui-selected": { bgcolor: "action.selected" } }}
```

The rule applies only to slot classes — the ones shaped `Mui<ComponentName>-<slot>`.

## Renaming a MUI icon changes its test id

MUI derives `data-testid` from the icon's display name, so swapping
`<ClearOutlined />` for `<Cancel />` turns `ClearOutlinedIcon` into `CancelIcon`.
Update every spec that queries it.
