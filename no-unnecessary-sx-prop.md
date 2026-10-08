---
paths:
  - "**/*.tsx"
  - "**/*.ts"
---

# No unnecessary `sx` prop on MUI system-prop components

`Box`, `Stack`, and `Grid` (from `@mui/material` / `@mui/system`) accept MUI system
properties **as direct JSX props**. Do not wrap them in `sx` when a direct prop works.

## Bad
```tsx
<Box sx={{ display: "flex", alignItems: "center", gap: 2 }} />
<Stack sx={{ width: "100%", mt: 2 }} />
<Grid sx={{ justifyContent: "space-between" }} />
```

## Good
```tsx
<Box display="flex" alignItems="center" gap={2} />
<Stack width="100%" mt={2} />
<Grid justifyContent="space-between" />
```

## When `sx` IS required
- Pseudo-selectors or child selectors: `sx={{ "&:hover": { opacity: 0.8 } }}`
- Theme function: `sx={(theme) => ({ color: theme.palette.primary.main })}`
- Any key that is NOT a system prop (e.g. custom CSS not in the system)

## System props that can be used directly
`display`, `flexDirection`, `flexWrap`, `justifyContent`, `alignItems`, `alignContent`,
`flex`, `flexGrow`, `flexShrink`, `flexBasis`, `alignSelf`, `justifyItems`, `justifySelf`,
`gap`, `columnGap`, `rowGap`,
`m`, `mt`, `mr`, `mb`, `ml`, `mx`, `my`, `p`, `pt`, `pr`, `pb`, `pl`, `px`, `py`,
`margin`, `marginTop`, `marginRight`, `marginBottom`, `marginLeft`,
`padding`, `paddingTop`, `paddingRight`, `paddingBottom`, `paddingLeft`,
`width`, `maxWidth`, `minWidth`, `height`, `maxHeight`, `minHeight`,
`color`, `bgcolor`, `opacity`,
`border`, `borderRadius`, `borderColor`, `boxShadow`,
`position`, `top`, `right`, `bottom`, `left`, `zIndex`,
`fontSize`, `fontWeight`, `fontFamily`, `lineHeight`, `textAlign`,
`overflow`, `overflowX`, `overflowY`, `visibility`

## Lint check
```bash
yarn lint:no-unnecessary-sx-prop
# or for a specific folder:
node scripts/detect-unnecessary-sx-prop.js src/squads/lesson
```
