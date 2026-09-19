# Deploying the prototype on Railway

This folder is a self-contained static site: the 32 prototype screens plus a
dependency-free Node server. Nothing is built or installed at deploy time, so a
deploy is just "clone the repo and run `node server.js`".

## One-time setup on Railway

1. **New Project → Deploy from GitHub repo → `jamessim-source/aigrading`.**
2. In the service's **Settings → Source**, set
   **Root Directory** to `prototypes/ai-feedback-student/deploy`
   and **Branch** to the branch you want to publish (currently
   `claude/ai-feedback-prd-university-ewhyr6`; switch to `main` once it merges).
   This step is required — the `package.json` lives in this folder, not at the
   repository root.
3. **Settings → Networking → Generate Domain.** Railway injects `PORT`; the
   server reads it.
4. Deploy. The build is Nixpacks with no dependencies; the start command is
   `node server.js`, and `railway.json` in this folder already declares it.

Every push to that branch redeploys.

## Password protection (optional, recommended for client-visible links)

Set both variables in **Settings → Variables**:

| Variable | Example |
|---|---|
| `AUTH_USER` | `manabie` |
| `AUTH_PASS` | a long random string |

With both set the whole site asks for Basic auth; with either missing it is
open. Do not commit the password — set it in Railway only.

## What gets served

| Path | Screen |
|---|---|
| `/` | index of all 32 screens |
| `/Main.html` … `/05-Todo.html` | PC flow, Japanese |
| `/Main-en.html` … `/05-Todo-en.html` | PC flow, English |
| `/M-Main.html` … `/M-Sheet.html` | mobile flow, Japanese |
| `/M-Main-en.html` … `/M-Sheet-en.html` | mobile flow, English |

The extension is optional: `/M-Crop` serves `M-Crop.html`.

## Regenerating after a design change

Edit `../gen.py` (the single source of truth for copy, styles and screens), then:

```
cd prototypes/ai-feedback-student
python3 gen.py
```

That rewrites both `project/` (the Claude Design canvas artboards) and
`public/*.html` (this site). Commit the result; Railway redeploys on push.

`public/dc-shim.js` is hand-written, not generated. It is a ~120-line stand-in
for the canvas runtime: it resolves `{{holes}}`, evaluates `<sc-if>` branches,
binds `onClick` / `onInput` to the functions each screen's `renderVals()`
returns, and re-renders on `setState`. That is why the same artboard files work
both inside the Claude canvas and as plain pages here.

## Running it locally

```
cd prototypes/ai-feedback-student/deploy
PORT=4311 node server.js
# then open http://127.0.0.1:4311/
```
