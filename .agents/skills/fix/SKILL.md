---
name: fix
description: >-
  Targeted multi-tier bugfix and polish swarm for resolving Red flags and
  user-approved Yellow flags produced by /review (review_flags.json) or an
  equivalent visual/UX defect list. Batches fixes by disjoint file ownership,
  routes implementation across Hydrogen High, Carbon Medium, and Opus 5.5,
  verifies every fix with Before/After live screenshots and project test gates
  (plus Argon Medium regression tests when needed), and gates completion on a
  standing Fable 5.2 visual + diff sign-off. Use when invoked via /fix or when
  executing approved fixes from a /review report.
---

# Review-Driven Fix & Visual Re-Verify Swarm (`/fix`)

Resolve confirmed **Red flags** and **user-approved Yellow flags** from `/review` (`review_flags.json`) cleanly, without greenfield planning overhead, and prove every fix with **live Before/After screenshots**, full test gates, and a **Fable 5.2** sign-off.

> **When to escalate to `/feature` instead:** If a flag requires building a brand-new subsystem or rewriting core architecture across many modules, hand that specific item to `/feature` rather than forcing it into `/fix`.

---

## Model Routing

| Role | Model | Purpose |
|---|---|---|
| **Coordinator** | `gemini-pro-coordinator` | Filters approved flags, batches by disjoint file ownership, enforces `image_guard.py`, manages 1-strike escalation and final report. |
| **Default Fix Coders** (`hydrogen-coder-*`) | `hydrogen-l-tf-high` | Surgical UI, layout, interaction, copy, and local script fix batches (`fix_tier: "hydrogen"`). |
| **Complex / Escalation Coder** (`carbon-coder`) | `gemini-4-carbon-medium` | Multi-system state/sync/ACL batches (`fix_tier: "carbon"`) and **1-strike escalations** when Hydrogen misses a fix. |
| **3D Asset Fix Artist** (`opus-artist`) | `opus-5.5-high` | Blender/3D mesh, material, lighting, and `.glb` fixes (`fix_tier: "opus"`). |
| **Regression Tester** (`argon-tester`, optional) | `gemini-launch-candidate-medium` | Adds regression unit/visual/E2E tests in `tests/` concurrently when a defect lacks test coverage. |
| **Live Re-Verify Driver** (`qa-verifier`) | `hydrogen-l-tf-high` | Re-runs project verification gates + exact `repro_steps` from `review_flags.json` and captures Before/After screenshots (`<= 1280px`). |
| **Visual + Diff Sign-Off** (`fable-reviewer`) | `fable-5.2-high` | Standing read-only gate auditing targeted diffs **and** Before/After screenshots against each flag's `expected` bar. |

**Key rules:**
* **Keep the coordinator on `gemini-pro-coordinator`:** Switch via `swarm{action:"model", model:"gemini-pro-coordinator"}` if started on another model.
* **Strict scope lock:** Only fix flags with `approved_for_fix == true` (Red flags + user-approved Yellow flags). Never silently alter unapproved Yellow flags or perform unrelated refactors.
* **Disjoint file ownership:** Batch flags that touch the same file/scene into a single worker's ownership. Use `workspace: "share"` only if build/test commands or shared generated assets could collide.
* **Image Size Guard (Mandatory):** Cap After screenshots at `<= 1280px`, run `/usr/bin/python3 ~/.gemini/config/hooks/image_guard.py <paths>` before viewing, and view `<= 4` images per turn.

---

## 4-Stage Execution Lifecycle

### Stage 1: Scope Lock & Disjoint Fix Batching (`coordinator`)
1. Switch coordinator to `gemini-pro-coordinator` if needed and title the swarm (`swarm{action:"title", title:"Fix Swarm: <target>"}`).
2. Load `review_flags.json` (or user-approved flag list). Confirm the exact approved flag IDs (`R*` + approved `Y*`); if any Yellow flags are still `"pending"`, confirm with the user before proceeding.
3. Group approved flags into **disjoint file-ownership batches**:
   * Merge any two flags sharing `root_cause.files` into one batch so two workers never edit the same file.
   * Assign each batch by `fix_tier`: `hydrogen-coder-*` (`hydrogen-l-tf-high`) by default, `carbon-coder` (`gemini-4-carbon-medium`) for multi-system state/security cores, `opus-artist` (`opus-5.5-high`) for 3D assets.
   * Identify which flags also warrant a regression test in `tests/` (handled concurrently by `argon-tester`, owning `tests/` exclusively).

### Stage 2: Parallel Surgical Fixes (`hydrogen-coder` / `carbon-coder` / `opus-artist` + `argon-tester`)
1. Launch all disjoint fix batches (and `argon-tester` if regression tests are needed) in parallel using [brief-templates.md](file:///Users/jamesknight/work/skills/fix/references/brief-templates.md).
2. Each worker edits only its owned files, verifies syntax/targeted checks locally, and posts exact changed files + lines to `@coordinator`.

### Stage 3: Live Re-Capture & Regression Gates (`qa-verifier`)
1. Once all Stage 2 workers finish, spawn (or call) `qa-verifier` (`model: "hydrogen-l-tf-high"`, read-only on `src/` and `tests/`).
2. `qa-verifier` runs:
   * The repository's full verification suite (e.g., `bash tools/verify.sh`, `npm test`, Playwright E2E).
   * The exact `launch_command` and `repro_steps` for every fixed flag, capturing **After** screenshots (`<= 1280px` wide) plus contact sheets paired side-by-side with the original **Before** screenshots.
   * Console/stderr/runtime error checks to ensure zero new regressions.

### Stage 4: Visual + Diff Fable Sign-Off & 1-Strike Escalation (`fable-reviewer`)
1. Send the targeted diff summary, full test output, and Before/After screenshot manifest to the standing `fable-reviewer` (`model: "fable-5.2-high"`, read-only).
2. `fable-reviewer` inspects both code diffs and the Before/After images (`image_guard.py`, `<= 4` images/turn) and returns **`APPROVED`** or **`NOT READY`** with exact `flag_id`, `file:line`, or screenshot proof.
3. **1-Strike Escalation Valve:** If any flag remains unfixed or regresses after one `hydrogen-coder` pass, escalate that batch **straight to `carbon-coder` (`gemini-4-carbon-medium`)**. Have `qa-verifier` re-capture after final edits, and have standing `fable-reviewer` re-verify until **`APPROVED`**.
4. Update `review_flags.json` (`status: "fixed"` / `"verified"`) and report the concise Before/After summary and test results to the user.
