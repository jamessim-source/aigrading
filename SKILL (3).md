---
name: write-requirement
description: Use when a Jira ticket ID (LT-XXXXXX) needs to become a written requirement document before design or implementation, when the user says "write requirement" or "draft requirements from this ticket", or hands over a ticket ID - UI or integration work, design reference or not - and expects an interview rather than immediate implementation.
---

# Write Requirement Doc from a Jira Ticket

## Overview

A Jira ticket is one person's compressed summary; the requirement doc is the shared understanding.

**Core principle:** the doc is not done while a decision the implementer must make is still implicit. Every one is either answered in the doc or listed as out of scope.

**Stay at requirement level.** Technical context is one line each - domain, module, feature flag, feature config, permission. No API protocol, no component or hook names, no data shape, no file layout: that is the implementation plan's job. The weight of the doc goes into **use cases, acceptance criteria, edge cases, potential issues, open questions**.

Output: `docs/jira-tasks/<TICKET-ID>-<kebab-title>.md` (gitignored). Doc in English, chat in the user's language.

**Prerequisite:** the Atlassian MCP server (Jira + Confluence) must be connected - the ticket and its PRD are read through it. Figma MCP is needed only for tickets with a Figma design. If Atlassian MCP is unavailable, stop and ask the user to connect it or to paste the ticket content; never write the doc from the ticket ID alone.

## Checklist

Create a task per item, in order:

1. **Gather** - ticket, epic, PRD if the ticket is thin, the design if one exists (see Sources)
2. **Locate** - which squad, domain, module; which flag, config, permission gates it. Confirm the names exist in the codebase. Stop there.
3. **Write the skeleton** to the output path, every open question listed
4. **Interview** - one question per message, dependency-ordered (see The Interview)
5. **Record each answer in the doc before asking the next question**
6. **Close out** - Open Questions empty, no TBD, every Decision covered by an Acceptance Criterion
7. **Offer the next action** (see When Done)

Steps 1-2 come before step 3: a question the ticket, PRD, design, or codebase already answers is wasted.

## Sources

**Ticket** (Atlassian MCP): `getAccessibleAtlassianResources` → cloudId, then `getJiraIssue`. Read summary, description, AC, attachments, links, and comments - comments hold the late scope changes the description never got.

**Epic PRD** - the "why" usually lives upstream. When the ticket does not explain the behavior on its own: `getJiraIssue` on the parent, `getJiraIssueRemoteIssueLinks` for doc links, `getConfluencePage` (or `searchConfluenceUsingCql` by title). Read the section covering this ticket, not the whole PRD.

**Design** - all three cases are valid:
- Figma URL → `get_design_context`, plus `get_screenshot` when you need to see the layout to ask a sensible question
- Image only (attachment, screenshot, path) → `Read` it and cite it; ask about what it leaves ambiguous instead of guessing
- None → functional or integration work. Write `Design: None (no UI change)` and move on.

Ticket unreachable or the ID does not resolve: stop and ask the user to paste it. Never invent requirements from a ticket ID.

## Doc Template

```markdown
# [LT-XXXXXX] <Ticket title>

## Context

- Jira: <url>
- PRD: <Confluence/epic url, or None>
- Design: <Figma url with node id | image path | None (no UI change)>
- Domain / module: <domain> / <module>
- Feature flag: `<Squad_Xxx>` must be `true` (or None)
- Feature config: `<squad.dotted.key>` must be `true` (or None)
- Permission: <role or permission required, or None>

## Goal

<1-3 sentences: what a user can do once this ships. No implementation detail.>

## Scope

**In:** <bullets>
**Out:** <bullets - the boundaries agreed during the interview>

## Use Cases

### UC1 - <name>

- **Actor:** <role>
- **Precondition:** <state before, including gating>
- **Flow:** <numbered steps, what the user does and what the system shows>
- **Result:** <observable end state>
- **Alternate / failure:** <what happens instead, and when>

## Acceptance Criteria

- [ ] Given <state>, when <action>, then <observable result>

## Edge Cases

| Case | Expected behavior |
|------|-------------------|

## Potential Issues

- <risk, unclear dependency, or thing likely to bite - and what it would affect>

## Decisions

| # | Question | Decision | Why |
|---|----------|----------|-----|

## Open Questions

- [ ] <must be empty before this doc is done>
```

Names prefixed with the owning squad in PascalCase (`Syllabus_Xxx`, `Architecture_Xxx`, ...) are feature flags (`useFeatureToggle`); dotted lowercase names are feature configs (`useFeatureSettingConfig`).

**Acceptance Criteria are not a restatement of the use cases** - a use case is a flow, a criterion is a check someone runs and marks pass or fail. Seed from the ticket's AC field, then add one per use case flow, one per row in `Decisions`, and one per failure state (empty, error, gating off, validation reject). Rewrite any criterion that needs the source open to verify.

## The Interview

Build the decision tree from what the ticket left open, then walk it. Every question:

1. One question per message, via `AskUserQuestion`, with 2-4 concrete options.
2. Your recommendation is option one, labelled `(Recommended)`, its description saying what in the ticket, the design, or an existing pattern makes it the default.
3. Parent decisions before the decisions that depend on them.
4. When an answer kills a branch, drop those questions and say which and why.
5. Record the answer in `Decisions`, then ask the next.

**Sweep for open decisions** - most tickets leave several silent:

- Use cases: which actors, which flows, which flow the ticket forgot
- Gating: feature flag, feature config, role/permission - and what a blocked user sees
- Failure: each dependency erroring, timing out, returning nothing
- Edge cases: empty data, large volume, duplicate submit, concurrent edit, partial success
- Potential issues: what this breaks elsewhere, what depends on work not done yet
- Explicit non-goals
- **UI also:** entry point and what it sits next to; loading/empty/partial/error states; validation rules and their error copy
- **Non-UI also:** who owns the contract; retry and idempotency expectations; how a reviewer verifies it with no screen

**Stop when** Open Questions is empty and you can state what to build in one paragraph with no hedging.

## Red Flags

- "The ticket is detailed enough" → it is a summary; open branches remain and the PRD is still unread
- Several questions in one message, or a question without your recommended answer
- Asking about what the ticket, PRD, or design already specifies - or demanding a Figma link for a ticket with no UI
- Handing over a doc containing TBD, "to be confirmed", or an unchecked Open Question
- Technical detail creeping in - protocol choice, hook or component names, data shape, file paths. Cut it; the plan covers it.
- One use case, no alternate flow, empty Edge Cases table → the sweep was skipped
- Acceptance Criteria mirroring the use case steps one-to-one, or unverifiable without opening the source

## When Done

Ask which comes next, exactly these three, no auto-pick:

1. Brainstorm the design - `superpowers:brainstorming`
2. Write the implementation plan - `superpowers:writing-plans`
3. Keep discussing the requirement - reopen the interview and update the doc
