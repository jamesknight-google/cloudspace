---
name: resume
description: >-
  Fast, token-disciplined cold-start session orientation from a fresh context.
  Reads docs/HANDOFF.md and AGENTS.md, cross-checks live git/tag/build state in
  one read-only shell command, flags any uncommitted drift, and presents a
  concise "Where We Stand & What's Next" briefing. Use when invoked via /resume
  or when the user starts a fresh session asking "what's next?", "pick up where
  we left off", "catch up on HANDOFF", or "status / orient to this repo".
---

# Cold-Start Session Resume (`/resume`)

Orient to any project from a fresh context window in **under 30 seconds** without bloating context or re-running passing test suites unnecessarily.

---

## Step 1: Read Canonical Entry-Point Docs Only (Token-Disciplined)

1. Locate and read the handoff & repo guardrail docs in priority order:
   * `docs/HANDOFF.md` (or root `HANDOFF.md`)
   * `AGENTS.md` / `GEMINI.md` (if not already injected in `<user_rules>`)
   * Active defect/plan handoffs **only** if `HANDOFF.md` flags unfinished work (e.g., `docs/review/review_flags.json` or an active `docs/*_PLAN.md`).
2. **Hard Context Guards:**
   * Do **not** recursively read `src/`, `tests/`, or 1,000-line design docs end-to-end during orientation. If you need roadmap details from a large spec (e.g., `docs/GAME_DESIGN_DOCUMENT.md`), grep headings first (`grep -n -E "^#{1,3} "`) and read only the target line range.
   * Do **not** load screenshot PNGs into model context during cold orientation unless diagnosing an active visual bug (and always pass images through `image_guard.py` first if viewed).

---

## Step 2: Cross-Check Live Git & Build State (Single Shell Call)

Run **one** fast, read-only command to verify reality against `HANDOFF.md`:

```bash
git status -sb && git log -n 5 --oneline --decorate && ls -la build/ dist/ 2>/dev/null || true
```

Check specifically for **handoff drift**:
* Commits landed *after* `HANDOFF.md` was last updated (`git log -n 1 -- docs/HANDOFF.md` if unclear).
* Uncommitted changes, untracked files, or stashed WIP (`git stash list`).
* Built artifact timestamps (`build/`, `dist/`) newer or older than `HEAD`.

---

## Step 3: Conditional Health Verification

* **Clean match (`HEAD` matches `HANDOFF.md` + working tree clean):** Trust the recorded gate counts in `HANDOFF.md`—do **not** burn minutes re-running heavy test/visual suites before the user picks a task.
* **Drift detected (dirty tree, unrecorded commits, or WIP blocker noted in `HANDOFF.md`):** Note the drift clearly and either run the fast check gate or offer to verify before starting new edits.

---

## Step 4: Present "Where We Stand & What's Next"

Reply concisely (`< 30` lines) in GitHub-Flavored Markdown (using clickable `file://` links in chat):

1. **Current Baseline:** Branch, tag/`HEAD` commit, recorded gate & build status from `HANDOFF.md`, plus any live git/artifact drift found in Step 2.
2. **Active Guardrails (2–3 bullets max):** Only the highest-leverage project invariants that shape the next decision.
3. **Ranked Next Options (2–4 tracks):**
   * Playtest / live feedback iteration (if recent builds exist)
   * Next roadmap slice / feature milestone (paired with `/feature`, `/proto`, or `/grill-me`)
   * Deferred polish / audit backlog items from `HANDOFF.md` (paired with `/fix` or `/review`)
4. End with one clear question asking which track to launch.
