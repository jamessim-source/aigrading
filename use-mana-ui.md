---
paths:
  - "**/*.tsx"
  - "**/*.ts"
---

# Prefer `@manabie-com/mana-ui` components over raw MUI

When a `mana-ui` component exists for the use case, use it instead of the raw MUI equivalent.
Import from `@manabie-com/mana-ui`.

## Component map

| Instead of (MUI)                              | Use (mana-ui)                                                   |
| --------------------------------------------- | --------------------------------------------------------------- |
| `Autocomplete`                                | `MAutocompleteBase`, `MAutocompleteCustom`, `MAutocompleteService` |
| `Autocomplete` + `react-hook-form`            | `MAutocompleteCustomHF`, `MAutocompleteServiceHF`               |
| `Accordion`                                   | `MAccordionBase`, `MAccordionSummaryBase`                       |
| `Alert`                                       | `MAlertBase`                                                    |
| `Avatar`                                      | `MAvatar`                                                       |
| `Backdrop`                                    | `MBackdropBase`, `MBackdropLoading`                             |
| `Breadcrumbs`                                 | `MBreadcrumbs`                                                  |
| `Button`                                      | `MButtonBase`, `MButtonPrimaryContained`, `MButtonPrimaryOutlined`, `MButtonPrimaryText`, `MButtonDefaultOutlined`, `MButtonCreate`, `MButtonDelete`, `MButtonDropdown` |
| `Checkbox`                                    | `MCheckboxBase`                                                 |
| `Checkbox` + `react-hook-form`                | `MCheckboxHF`                                                   |
| `Chip`                                        | `MChipBase`, `MChipStatus`, `MChipAutocomplete`                 |
| `CircularProgress`                            | `MCircularProgressBase`                                         |
| `DatePicker`                                  | `MDatePickerCustom`                                             |
| `DatePicker` + `react-hook-form`              | `MDatePickerCustomHF`                                           |
| `Dialog`                                      | `MDialogBase`, `MDialogCustom`, `MDialogCancelConfirmCustom`    |
| `Divider`                                     | `MDividerBase`, `MDividerDashed`                                |
| `Drawer`                                      | `MDrawerBase`                                                   |
| `IconButton`                                  | `MIconButtonBase`                                               |
| `Link` (external)                             | `MExternalLink`                                                 |
| `Paper`                                       | `MPaperCustom`, `MPaperSectionWrapper`                          |
| `Popover`                                     | `MPopoverBase`                                                  |
| `Radio`                                       | `MRadioBase`                                                    |
| `RadioGroup`                                  | `MRadioGroupBase`                                               |
| `Select`                                      | `MSelectCustom`                                                 |
| `Select` + `react-hook-form`                  | `MSelectHF`                                                     |
| `Skeleton`                                    | `MSkeletonBase`                                                 |
| `Snackbar`                                    | `MSnackbarBase`                                                 |
| `Switch`                                      | `MSwitchBase`                                                   |
| `Tabs` / `Tab`                                | `MTabsBase`, `MTabPanel`, `MTabLayout`                          |
| `TextField`                                   | `MTextFieldBase`                                                |
| `TextField` + `react-hook-form`               | `MTextFieldHF`                                                  |
| `TimePicker` + `react-hook-form`              | `MTimePickerAutocompleteHF`                                     |
| `ToggleButton`                                | `MToggleButtonBase`, `MToggleButtonGroupBase`                   |
| `Tooltip`                                     | `MTooltipBase`                                                  |
| `Typography`                                  | `MTypographyBase`, `MTypographyHeader`, `MTypographyPageTitle`  |
| `Typography` (truncate / ellipsis)            | `MTypographyMaxLines`, `MTypographyShortenStr`, `MTypographyWithTooltip` |
| `Typography` (label + value pair)             | `MTypographyWithValue`, `MTypographyDoubleDash`, `MDoubleDash`  |

## Layout / wrapper components

| Use case                       | mana-ui component           |
| ------------------------------ | --------------------------- |
| Page content wrapper           | `MWrapperPageContent`       |
| Dialog content wrapper         | `MWrapperDialogContent`     |
| Portal base wrapper            | `MWrapperPortalBase`        |
| "Looking for" empty state      | `MWrapperLookingFor`        |
| Form filter (advanced)         | `MFormFilterAdvanced`       |
| File upload placeholder        | `MFormUploadFilePlaceholder` |
| File upload input              | `MUploadInput`              |
| Fullscreen toggle              | `MFullscreen`               |
| Bulleted list item             | `MListBullet`               |

## Icons (use mana-ui, not raw MUI icons)

`MAssignmentIcon`, `MAudioIcon`, `MBrightcoveIcon`, `MCsvIcon`, `MDeleteIcon`,
`MDocIcon`, `MEmptyIcon`, `MExamIcon`, `MFileIcon`, `MFlashCardIcon`, `MHeicIcon`,
`MImageIcon`, `MJpgIcon`, `MLearningObjectiveIcon`, `MNoResultIcon`, `MPdfIcon`,
`MPngIcon`, `MPptIcon`, `MRetryIcon`, `MSpinnerIcon`, `MTaskIcon`, `MVideoIcon`,
`MXlsIcon`, `MZipIcon`

## When raw MUI is still fine
- `Box`, `Stack`, `Grid` for layout (no mana-ui equivalent)
- Components not listed above that have no mana-ui counterpart
- When a mana-ui component doesn't expose a prop you need and wrapping it would add unnecessary complexity — note this in a comment
