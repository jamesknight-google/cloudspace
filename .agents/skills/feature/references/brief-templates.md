# Multi-Tier Build & Fable Review Swarm — Brief & Gate Templates

Swarm workers start fresh with zero prior conversation context. Fill in the `{...}` slots so every brief stands on its own.

---

## 1. Stage 1 Contract-Locked Planner Brief (`carbon-planner`, `model: "gemini-4-carbon-high"`)

```markdown
@carbon-planner You are `carbon-planner`, running on Gemini 4 Carbon (High).
Do NOT edit or create repository files.

## Request & Goal
{User request, acceptance criteria, and any locked constraints.}

## Verified Workspace Context
- Repo path: {path}
- Relevant files / conventions: {key files, stack, infra patterns}

## Deliverable
Post a structured, **contract-locked** architecture plan to `@coordinator` covering:
1. System boundaries, stack, and directory layout.
2. **Locked contracts** (exact function signatures, types/JSON schemas, routes, node hierarchies, and state invariants) so `hydrogen-coder` and `argon-tester` can build in parallel without guessing.
3. Disjoint file ownership per worker (separating `src/` tracks from `tests/`), plus explicit flag on any high-risk slice that must go to `carbon-coder` (`gemini-4-carbon-medium`) instead of `hydrogen-coder`.
4. Key trade-offs, risks, and crisp open decisions needed from the user (if any).
```

---

## 2. Stage 2 Default Coder Brief (`hydrogen-coder`, `model: "hydrogen-l-tf-high"`)

```markdown
@hydrogen-coder You own the `{track_name}` implementation track on Gemini 4 Hydrogen (High).

## Disjoint File Ownership
- Owned paths (read/write): {exact src/ files/dirs}
- Read-only / off-limits (owned by other coders or `argon-tester`): {other workers' paths, tests/}

## Locked Contract & Invariants
- Approved plan & locked signatures/schemas: {summary or ref #seq}
- Do NOT deviate from the locked contract; if a contract gap blocks you, post to `@coordinator` immediately instead of inventing a new interface.

## Definition of Done
1. Implement all owned components cleanly against the locked contract.
2. Run syntax/build/targeted verification (`{commands}`) and fix any errors in owned files.
3. Post modified files, contract notes, and verification output to `@coordinator`.
```

---

## 3. Stage 2 Parallel Spec-Driven Tester Brief (`argon-tester`, `model: "gemini-launch-candidate-medium"`)

```markdown
@argon-tester You own the test & verification track on Gemini 4 Argon (Medium).
Start writing tests **immediately** from the Stage 1 locked contract—do NOT wait for `hydrogen-coder` to finish `src/`.

## Disjoint File Ownership
- Owned paths (read/write): {exact tests/ files/dirs}
- Read-only / off-limits: {all src/ files — never edit application code}

## Locked Contract & Invariants
- Approved plan, exact signatures, schemas, and invariants: {summary or ref #seq}
- Write black-box unit, contract, visual, and E2E tests against the **spec**, not against Hydrogen's in-progress implementation.

## Definition of Done
1. Author the test suite covering happy paths, edge cases, and non-negotiable invariants.
2. Once `@coordinator` signals `src/` workers are ready, run the full verification suite (`{commands}`).
3. Report exact pass/fail counts, failing `file:line` traces, and any contract drift to `@coordinator`.
```

---

## 4. Stage 2 Complex / Escalation Coder Brief (`carbon-coder`, `model: "gemini-4-carbon-medium"`)

Use for slices flagged as high-risk/complex core in Stage 1, or for 1-strike Stage 4 escalations.

```markdown
@carbon-coder You own the `{track_name}` implementation track on Gemini 4 Carbon (Medium).

## Disjoint File Ownership
- Owned paths (read/write): {exact files/dirs}
- Read-only / off-limits (owned by other workers): {other workers' paths}

## Architecture & Contracts
- Approved plan & invariants: {summary or ref #seq}
- Shared API / schema contracts: {exact types, routes, state invariants}

## Definition of Done
1. Implement all owned components cleanly against the shared contract (or resolve the escalated Stage 3/4 finding).
2. Run build/typecheck/targeted verification (`{commands}`) and fix any errors in owned files.
3. Post modified files, contract notes, and verification output to `@coordinator`.
```

---

## 5. Stage 3 Single-Track Fable Review Gate (`fable-reviewer`, `model: "fable-5.2-high"`)

```markdown
@fable-reviewer Adversarial Final Review Gate (read-only — do NOT edit any files).
You are the standing `fable-reviewer` on Claude Fable 5.2 for this build and any follow-up re-verification passes.

## Scope & Context
- Repo / changed files: {paths or git diff scope}
- Plan / invariants / requirements: {key invariants or ref #seq}
- Post-edit verification already run: {exact test/build commands and counts}

## What to Audit
1. Correctness, edge cases, and regressions against the stated requirements/invariants.
2. Security, auth/ACL, data exposure, and error handling.
3. Contract mismatches, missing validation, or test gaps/relaxed assertions.
4. Scope creep or dead/duplicated code.

## Output Format (post to `@coordinator`)
- Verdict: **APPROVED** (or **SHIP**) vs **NOT READY**
- Findings grouped by **Critical**, **High**, **Medium**, **Low**, each with `file:line`, concrete bug/risk, and exact fix.
```

---

## 6. Stage 3 Multi-Track Fable Review Swarm (`@fable-reviewer` -> Sub-Reviewers, `model: "fable-5.2-high"`)

Use when reviewing multi-surface systems (e.g., Backend + Web SPA + Mobile/Infra).

```markdown
@fable-reviewer Adversarial Final Review Gate across {repo_path}. Do NOT modify any files.
You are the standing `fable-reviewer` on Claude Fable 5.2.

## Verified Test Baseline
{Exact suite counts, build commands, and live E2E status}

## Tracks & Contracts
- Track 1 (Core/Backend): {paths + invariants}
- Track 2 (Web/Client): {paths + contract source}
- Track 3 (Mobile/Infra/Other): {paths + contract source}

## Review Swarm Instructions
Review Track 1 directly (security, ACL/auth, core logic, data integrity).
For Tracks 2–3 and exhaustive contract diffs, spawn read-only sub-reviewers via `swarm{action:"add"}`:
- Domain reviewers on `model: "fable-5.2-high"` (e.g., `web-reviewer`, `android-reviewer`)
- Exhaustive schema/route diffing on `model: "hydrogen-l-tf-high"` (e.g., `contract-auditor`)
Instruct every sub-reviewer: read-only, cite exact `file:line`, report concrete bugs/mismatches only, and reply to `@fable-reviewer`.

Consolidate all findings into one prioritized **Critical / High / Medium / Low** gate report for `@coordinator` with verdict **APPROVED** or **NOT READY**.
```

---

## 7. Stage 4 Re-Verification Pass (Standing `@fable-reviewer`)

```markdown
@fable-reviewer Re-check pass for fixes from #{review_seq}. Do NOT modify files.
- Fixed items & worker reports: {H1..Hn, #seq1, #seq2}
- Post-fix build & test results: {exact re-run commands and pass counts}

Inspect the targeted files/diffs and regression tests. Reply `@coordinator`: **APPROVED** (or remaining blocking items with `file:line`).
```
