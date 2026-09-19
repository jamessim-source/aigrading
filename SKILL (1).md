---
name: feature-workflow
description: >
  Standard workflow for making CODE CHANGES to school-portal-admin. Use whenever
  the user asks to implement, add, build, fix, change, or remove a feature,
  component, screen, hook, translation, or feature flag in this repo - even when
  they don't mention branches or tickets. It enforces the process: a Jira ticket
  before any code, work starts from the latest develop on a fresh
  feature/<ticket-id>-<description> branch, and the ticket moves to In
  Development. Do NOT use for read-only investigation, questions, code reading,
  or work outside this repo.
---

# Feature workflow

Every code change starts from a ticket and a clean branch cut from `develop`, so
history stays traceable and PR diffs stay minimal. Follow the steps in order -
don't skip ahead to editing code.

## Step 1 - Require a Jira ticket (blocking)

- Look for a Jira key (`LT-12345`) in the request.
- **No ticket ID → STOP and ask for it.** Don't create a branch, don't write
  code, don't guess an ID.
- Fetch the title with `getJiraIssue` (Atlassian MCP) to craft the branch
  description and sanity-check the ticket matches the request. Lookup failure is
  not blocking - continue with just the ID.

## Step 2 - Check the current branch first

If the current branch already belongs to this ticket, or is a shared branch the
user is deliberately stacking several tickets on, **stay on it** - ask rather
than cutting a new branch. Otherwise:

```bash
git status            # confirm a clean tree first
git checkout develop
git pull origin develop
```

Uncommitted changes → surface them and ask (stash / commit elsewhere / abort).
Never discard silently.

## Step 3 - Create the feature branch

Format: **`feature/<ticket-id>-<short-description>`**, description derived from
the ticket title, words joined by `-`.

```bash
git checkout -b feature/LT-12345-short-description
```

Examples from this repo:
`feature/LT-109154-remove-syllabus-draft-js`,
`feature/LT-110227-allow-multiple-submission-id-search-in-to-review-screen`.

Creating the branch is where work starts, so move the ticket to **In
Development**: `getTransitionsForJiraIssue`, pick the transition whose name
matches "In Development" (or a close variant like `In Progress`, `In Dev`,
case-insensitive), apply with `transitionJiraIssue`. Never move a ticket
backwards; if it's already there or further along, leave it. Best-effort only -
this must never block coding.

## Step 4 - Do the work

Plan first and wait for approval before writing code. Follow the repo
conventions in `CLAUDE.md` and reuse the existing squad skills where they fit
(`test-cases`, `e2e`, `write-requirement`). Keep the diff scoped to the ticket.

Only touch squads listed in `my-team.json` unless asked otherwise. Verify with
`yarn test:selective src/squads/<squad>` and `yarn lint` before reporting done.

## Step 5 - Stop at the local commit

**Do not push, do not open a PR, do not merge.** A branch here can hold several
tickets, and the author pushes and opens the PR when the whole branch is ready.
Report what was implemented and ask what's next.

Commit messages: no `[LT-XXXXX]` prefix (CI adds the ticket automatically), no
co-author trailer, keep the subject short and imperative.

## Guardrails

- **No ticket → no code.** The one hard gate.
- **Plan → approve → implement**, even for a few-line fix.
- **One ticket = one branch**, unless the user is deliberately stacking tickets
  on a shared branch - then keep using theirs.
- **Never push/PR/merge on your own.**
