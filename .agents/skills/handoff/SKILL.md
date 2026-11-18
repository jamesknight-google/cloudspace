---
name: handoff
description: >-
  End-of-session and milestone progress capture into docs/HANDOFF.md. Verifies
  live test/build gates and git cleanliness, closes active swarms cleanly, and
  updates docs/HANDOFF.md in-place using compact, portable Markdown for external
  MD readers and seamless /resume cold starts. Use when invoked via /handoff or
  when the user asks to save progress to HANDOFF, wrap up a session, checkpoint
  a milestone, or prepare a handoff for a fresh context.
---

# Session & Milestone Handoff (`/handoff`)

Capture verified repository state into a single, compact, self-contained `docs/HANDOFF.md` so the next fresh session can `/resume` immediately with zero lost context.

---

## Step 1: Audit Live State, Gates & Running Tasks

1. **Check active tasks & swarms:**
   * If a swarm is active (`swarm{action:"status"}`), ensure any `share`/`branch` worker changes are merged/landed first, post `[done] <summary>` (if `monitor` is active), and `kill` finished workers.
   * Check background tasks (`manage_task{Action:"list"}`) so no orphan dev servers or watchers are left behind unless intentional.
2. **Audit git & scratch hygiene:**
   * Run `git status -sb`, `git diff --stat`, and `git log -n 10 --oneline --decorate`.
   * Remove any temporary scratch files accidentally created inside the workspace (keep scratch scripts strictly in `<artifact_dir>/scratch/`).
   * In Godot repos, verify `docs/.gdignore` exists whenever images live under `docs/`.
3. **Verify truth of test/build claims:**
   * Only record **"Green / Passing"** gate counts if the verification suite (e.g., `bash tools/verify.sh`, `npm test`) actually ran and passed against the **current** code state.
   * If wrapping up mid-feature or with failing checks, record the exact pass/fail state honestly under **In-Progress / Known Blockers** rather than running unrequested fixes or claiming stale green numbers.

---

## Step 2: Write / Update `docs/HANDOFF.md` In-Place

Write to `<workspace>/docs/HANDOFF.md` (unless the repository already standardizes on root `HANDOFF.md`).

### Formatting Rules (External MD Reader Compatibility)
* **Portable standard GFM only:** Must render cleanly in Obsidian, Typora, Marked 2, VS Code, and macOS Quick Look.
* **Relative paths only** inside `docs/HANDOFF.md`:
  * Source/doc links: `[config.gd](../src/core/config.gd)`, `[GAME_DESIGN_DOCUMENT.md](./GAME_DESIGN_DOCUMENT.md)` — **never** `file://` URLs.
  * Embedded screenshots: copy key proof images (`<= 1280px` wide) into `docs/review/` and embed via `![Caption](./review/shot.png)` — **never** `~/.gemini/jetski/brain/...` paths or Jetski-only ````carousel` blocks.
* **Compact rolling budget (`<= 180` lines):** Update `HANDOFF.md` **in-place**—do not append unbounded session logs. Condense older shipped milestones into 1-line bullets under *Committed Milestones* and keep detailed changelogs focused on the latest milestone/delta.

### Required 6-Section Structure

1. **Current Repository State (`branch` @ `tag / commit`):**
   * Stack/engine version, package/bundle ID, exact verification gate results & counts, and 1-line summary of committed milestones.
2. **Locked Creative, Product & Architecture Decisions:**
   * Concise bullet list of non-negotiable invariants a fresh session must preserve (linking `AGENTS.md` and detailed specs rather than duplicating them).
3. **Built Artifacts & Documentation Map:**
   * Compact table mapping *Area -> Key Files / Directories* + exported binary paths.
4. **Latest Session / Post-Baseline Changelog:**
   * Concrete summary of what changed in the current milestone (key files, architectural choices, new tests, and up to 2–4 key visual proof embeds if UI changed).
5. **Verification, Run & Build Commands:**
   * Copy-pasteable shell block for tests, local launch, and platform builds.
6. **Next Steps & Open Backlog:**
   * Prioritized next tracks (playtest validation, next slice/feature, deferred non-blocking polish items with exact identifiers/`file:line`, and any open questions or WIP blockers).

---

## Step 3: Final Git Check & User Summary

* Run `git status -sb` to confirm whether `docs/HANDOFF.md` (and any `docs/review/*.png` assets) are the only modified/untracked files or part of a release commit.
* Only `git commit` or `git tag` if the user asked for a commit/release; otherwise ask in one line if they want `docs/HANDOFF.md` committed now.
* Reply concisely in chat with a clickable `file://` link to the updated `HANDOFF.md` and confirm the session is ready for a clean `/resume`.
