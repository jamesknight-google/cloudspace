# Review-Driven Fix Swarm — Brief Templates

Workers start fresh with zero prior conversation context. Fill in `{...}` so every brief stands on its own.

---

## 1. Stage 2 Fix Batch Brief (`hydrogen-coder` / `carbon-coder` / `opus-artist`)

Pin `model: "hydrogen-l-tf-high"` (default), `"gemini-4-carbon-medium"` (complex state/escalation), or `"opus-5.5-high"` (3D/Blender).

```markdown
@{worker_name} You own Fix Batch `{batch_name}` on {model_label}.

## Disjoint File Ownership
- Owned paths (read/write): {exact files/dirs for this batch}
- Off-limits (owned by other workers or tests): {all other files}

## Approved Flags to Fix (STRICT SCOPE — do NOT touch unrelated code or unapproved Yellow flags)
{For each flag in batch:
- Flag ID: {R1 / Y2}
- Title: {title}
- Screenshot / repro: {screenshot_path + repro_steps}
- Observed vs Expected: {observed} -> {expected}
- Root cause hint: {root_cause.files + summary}}

## Definition of Done
1. Fix every assigned flag cleanly with minimal, maintainable edits inside owned files.
2. Run targeted local syntax/lint/check commands (`{commands}`).
3. Post modified files, line summaries per flag ID, and local check output to `@coordinator`.
```

---

## 2. Stage 2 Parallel Regression Tester Brief (`argon-tester`, `model: "gemini-launch-candidate-medium"`)

```markdown
@argon-tester You own regression test updates in `tests/` on Gemini 4 Argon (Medium).
Do NOT edit any `src/` files.

## Disjoint File Ownership
- Owned paths (read/write): {exact tests/ files}
- Read-only / off-limits: {all src/ files}

## Flags Requiring Regression Coverage
{For each flag: ID, expected invariant/behavior, and repro steps from review_flags.json}

## Definition of Done
1. Add concise regression assertions locking in the `expected` behavior for each listed flag (no relaxed assertions).
2. Wait for `@coordinator`'s green light on `src/`, or verify test syntax immediately.
3. Post added/updated test paths and what each assertion proves to `@coordinator`.
```

---

## 3. Stage 3 Live Re-Verify & Before/After Capture Brief (`qa-verifier`, `model: "hydrogen-l-tf-high"`)

```markdown
@qa-verifier You are `qa-verifier` on Gemini 4 Hydrogen (High). Read-only — do NOT edit `src/` or `tests/`.

## Verification Scope
- Project full suite / gates: `{full_test_commands}`
- Launch command: `{launch_command}`
- Flags to re-verify live: {list of flag IDs, repro_steps, and original Before screenshot paths}

## Instructions
1. Run `{full_test_commands}` after all edits and record exact pass/fail counts.
2. Re-run `{launch_command}` and execute each flag's `repro_steps`.
3. Capture **After** screenshots (`<= 1280 px` wide) into `{scratch_dir}/after/` and build side-by-side or contact-sheet comparisons with the original **Before** shots (`<= 1280 px` wide).
4. Record any console/stderr errors or newly introduced layout/interaction regressions.

## Deliverable (post to `@coordinator`)
- Full suite command output & counts
- Per-flag checklist (`flag_id` -> Before path, After path, observed behavior, runtime errors: none/details)
```

---

## 4. Stage 4 Fable Visual + Diff Sign-Off Brief (`fable-reviewer`, `model: "fable-5.2-high"`)

```markdown
@fable-reviewer Adversarial Fix & Visual Sign-Off Gate (read-only — do NOT edit any files).
You are the standing `fable-reviewer` on Claude Fable 5.2 for this fix cycle and any follow-up pass.

## Image Rules (MANDATORY)
- Before viewing ANY image, run `/usr/bin/python3 ~/.gemini/config/hooks/image_guard.py <paths>` and view the returned paths.
- View **at most 4 images per turn**.

## What to Audit
- Approved flags & expected outcomes: {flag list with expected bars}
- Targeted diff / modified files: `{git_diff_scope}`
- Post-fix verification baseline: {exact test counts from @qa-verifier}
- Before vs After screenshots: {before_and_after_paths}

## Output Format (post to `@coordinator`)
- Verdict: **APPROVED** vs **NOT READY**
- Per-flag status (`R1`: FIXED / STILL BROKEN, etc.)
- Any remaining or newly introduced **Critical / High / Medium** issues with `file:line` or `shot_id` and exact required fix.
```
