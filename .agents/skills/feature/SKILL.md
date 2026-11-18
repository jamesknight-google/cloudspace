---
name: feature
description: >-
  Full multi-tier engineering workflow and adversarial Fable 5.2 review swarm.
  Uses Gemini Pro Coordinator (`gemini-pro-coordinator`) for orchestration,
  Gemini 4 Carbon High (`gemini-4-carbon-high`) for contract-locked planning,
  Gemini 4 Hydrogen High (`hydrogen-l-tf-high`) for default parallel coding,
  Gemini 4 Argon Medium (`gemini-launch-candidate-medium`) for parallel
  spec-driven testing, Gemini 4 Carbon Medium (`gemini-4-carbon-medium`) for
  flagged complex cores and 1-strike escalations, Claude Opus 5.5
  (`opus-5.5-high`) for Blender 3D work, and Claude Fable 5.2
  (`fable-5.2-high`) for adversarial Final Review Gates. Use when invoked via
  `/feature` or when the user asks for the full multi-model build and review
  workflow, Fable review swarm, production-grade architectural planning with
  adversarial sign-off, or a thorough multi-reviewer code review gate.
---

# Multi-Tier Build & Fable Review Swarm (Plan -> Multi-Tier Build -> Adversarial Review Gate)

Run high-rigor engineering tasks through the four-stage multi-model lifecycle:
**Carbon High contract-locked planning** -> **Hydrogen High coding + Argon Medium parallel testing (+ Opus 3D / Carbon Medium escalation)** -> **adversarial Fable 5.2 review gate** -> **fix-and-reverify sign-off**.

> **Review-only invocation:** If the user asks to run the Fable review swarm on an **already-built** codebase, branch, or diff, skip Stages 1–2 and start directly at **Stage 3**.

---

## Model Routing

| Work | Model | How to Invoke |
|---|---|---|
| **Coordinator / Orchestrator** | **Gemini Pro Orchestrator** | Session coordinator on `gemini-pro-coordinator` (`swarm{action:"model", model:"gemini-pro-coordinator"}` if started on another model). |
| **High-level planning & locked contracts** (architecture, exact interfaces, invariants, file ownership) | **Gemini 4 Carbon (High)** | `swarm` worker (`carbon-planner`) with `model: "gemini-4-carbon-high"`. |
| **Default implementation & research** (feature code, UI, backend, CRUD, importers, surveying 3+ files) | **Gemini 4 Hydrogen (High)** | `swarm` worker(s) (e.g., `hydrogen-coder`, `researcher`) with `model: "hydrogen-l-tf-high"`. |
| **Spec-driven testing & verification** (unit, contract, visual, E2E, regression suites) | **Gemini 4 Argon (Medium)** | `swarm` worker (`argon-tester`) with `model: "gemini-launch-candidate-medium"`. |
| **Complex core & 1-strike escalation** (flagged security/ACL, sync, multi-system concurrency, or Hydrogen fix miss) | **Gemini 4 Carbon (Medium)** | `swarm` worker (`carbon-coder`) with `model: "gemini-4-carbon-medium"`. |
| **Blender 3D modeling** (`bpy`/`bmesh`, materials, scene layout, viewport QA) | **Claude Opus 5.5** | `swarm` worker with `model: "opus-5.5-high"` (or `blender-artist`). |
| **Adversarial review & Final Review Gate** | **Claude Fable 5.2** | Standing `fable-reviewer` `swarm` worker with `model: "fable-5.2-high"`. |

**Key rules:**
* **Keep the coordinator on `gemini-pro-coordinator`:** Once the swarm exists, switch the coordinator to `gemini-pro-coordinator` if the session started on Opus, Fable, or Carbon so orchestration never burns Frontier/Anthropic quota.
* **Pin exact model IDs via `swarm`:** `invoke_subagent` only accepts `inherit`, `flash_lite`, `flash`, `pro` and cannot select `hydrogen-l-tf-high`, `gemini-launch-candidate-medium`, `gemini-4-carbon-medium`, or `fable-5.2-high`.
* **True 3-way diversity:** Hydrogen codes (`hydrogen-l-tf-high`) -> Argon tests from locked contracts (`gemini-launch-candidate-medium`) -> Fable reviews adversarially (`fable-5.2-high`).
* **Separate planning from review, and conserve Anthropic quota:** Stage 1 plans on `gemini-4-carbon-high`. Stage 3 uses one standing `fable-reviewer` (`fable-5.2-high`) kept warm for Stage 4 re-verification; only spawn Fable sub-reviewers on genuinely multi-surface builds (3+ surfaces) since Fable and Opus share the Anthropic quota pool.
* When surveying 3+ unfamiliar files or docs before planning, delegate research to a `hydrogen-l-tf-high` swarm researcher rather than bloating the coordinator/planner context.

---

## 4-Stage Execution Lifecycle

### Stage 1: Contract-Locked Plan (`carbon-planner`)
1. Switch coordinator to `gemini-pro-coordinator` if not already on it.
2. Spawn `carbon-planner` (`swarm{action:"add", name:"carbon-planner", model:"gemini-4-carbon-high", ...}`) in **read-only** mode (no repo edits).
3. Brief it with the user request, verified workspace context, and hard constraints (see [brief-templates.md](file:///Users/jamesknight/work/skills/feature/references/brief-templates.md)).
4. Require `carbon-planner` to output **locked contracts**—not just architecture prose:
   * Exact public function signatures, types/schemas, node hierarchies, routes, and invariants.
   * Disjoint file ownership per worker (separating `src/` implementation tracks from `tests/`).
   * Explicit flag on any high-risk slice that should go straight to `carbon-coder` (`gemini-4-carbon-medium`) instead of `hydrogen-coder`.
5. Coordinator reconciles the plan and gets user approval before Stage 2 implementation.

### Stage 2: Parallel Multi-Tier Implementation (`Hydrogen High` + `Argon Medium` + `Opus` / `Carbon Medium`)
1. Partition work with **strictly disjoint file ownership** (`workspace: "inherit"` when paths do not collide; `workspace: "share"` if concurrent edits/builds could overlap).
2. **Default coding (`hydrogen-coder`, `hydrogen-l-tf-high`):** Assign ~90% of implementation tracks to Hydrogen High workers briefed with the locked Stage 1 contracts.
3. **Parallel spec-driven testing (`argon-tester`, `gemini-launch-candidate-medium`):** Launch `argon-tester` **at the same time as `hydrogen-coder`**—do NOT wait for implementation to finish. `argon-tester` owns `tests/` exclusively, writes unit/contract/visual/E2E tests directly against `carbon-planner`'s locked contract (black-box, without reading Hydrogen's in-progress code), and runs the full verification suite once `hydrogen-coder` reports ready.
4. **Complex core (`carbon-coder`, `gemini-4-carbon-medium`):** Only assign slices that `carbon-planner` explicitly flagged as high-risk/complex core (security/ACL, state-machine sync, multi-system concurrency).
5. **3D modeling (`opus-5.5-high`):** Assign Blender/3D asset work when needed.
6. Verify cross-track contract alignment and ensure `argon-tester` passes the full build + test suite before triggering Stage 3.

### Stage 3: Adversarial Fable Review Swarm (`fable-reviewer`)
1. Spawn (or call back) the **standing Fable worker** (`fable-reviewer`, `model: "fable-5.2-high"`) for an adversarial, read-only code-level gate — never rubber-stamp summaries without checking code.
2. **Choose review topology by scope:**
   * **Default (1–2 surfaces / focused change):** Single standing `fable-reviewer` audits all changed files, security/auth/privacy boundaries, edge cases, regressions, and test rigor directly.
   * **Multi-surface build (3+ distinct surfaces, e.g., Backend + Web + Mobile/Infra):** Instruct `fable-reviewer` to lead a **review swarm** and spawn read-only sub-reviewers via `swarm{action:"add"}`:
     * Domain reviewers on `fable-5.2-high` only where needed (e.g., `web-reviewer`, `android-reviewer`).
     * Exhaustive schema/API contract auditors on `hydrogen-l-tf-high` (e.g., `contract-auditor`) — read-only on source code.
3. **Strict Reviewer Contract:**
   * **Read-only:** Reviewers and sub-reviewers MUST NOT modify application or test files.
   * **Concrete evidence only:** Cite exact `file:line`, failure scenario, and required fix.
   * **Prioritized severity:** `Critical` / `High` (blocking) vs. `Medium` / `Low`.
   * **Explicit verdict:** **`APPROVED` / `SHIP`** or **`NOT READY`** with a numbered blocking list.

### Stage 4: Fix, 1-Strike Escalation, and Final Sign-Off
1. **Never hand over on `NOT READY`.** Route blocking `Critical`/`High` (and targeted `Medium`) fixes back to the owning `hydrogen-coder` (or `carbon-coder`) with explicit `file:line` references and non-overlapping ownership.
2. **1-Strike Escalation Valve:** If `hydrogen-coder` fails to resolve a blocking finding cleanly in **one pass**, escalate that slice **straight to `carbon-coder` (`gemini-4-carbon-medium`)**.
3. Have `argon-tester` (`gemini-launch-candidate-medium`) update/add regression tests covering every blocking finding (without overlapping app code owners) and re-run all builds, unit/integration, and visual/E2E checks **after** the final edits.
4. Kill finished one-off sub-reviewers to keep the board clean, then post the targeted diff summary and post-fix verification output to the **standing `fable-reviewer`** for re-verification.
5. Repeat until `fable-reviewer` posts **`APPROVED`** / **`SHIP`**, then post `[done] <summary>` (if a monitor is active) and report verified results to the user. If blocked on any unresolved item, report it explicitly.
