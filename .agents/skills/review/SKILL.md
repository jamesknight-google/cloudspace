---
name: review
description: >-
  Live product, visual, and interaction design review swarm for a finished or
  beta app, game, or UI. Runs the product live, captures multi-viewport
  screenshots and interaction telemetry, dispatches independent dual-lab
  Visual (Claude Fable 5.2) and UX/Product (Gemini 4 Carbon High) critics, maps
  root causes to code, and triages findings into Red flags (auto-queued for
  fixing) and Yellow flags (held for human review) with a structured handoff to
  /fix or /feature. Use when invoked via /review or when the user asks for a
  live UI/UX/design review, visual polish audit, playtest critique, or
  red/yellow flag triage of a finished product.
---

# Product, Visual & Interaction Design Review Swarm (`/review`)

Audit a **finished or beta** app, game, or UI from the **user's / player's perspective first** — using live execution and screenshots rather than reading source code to rationalize bugs — then produce an actionable **Red / Yellow Flag** report ready for `/fix` or `/feature`.

---

## Model Routing

| Role | Model | Purpose |
|---|---|---|
| **Coordinator** | `gemini-pro-coordinator` | Orchestrates swarm, enforces `image_guard`, triages Red/Yellow flags, runs human Yellow-flag gate, produces handoff. |
| **Live QA Driver(s)** (`qa-driver`) | `hydrogen-l-tf-high` | Runs the live product, exercises flows/viewports/edge states, captures `<= 1280px` screenshots + contact sheets + runtime telemetry. |
| **Visual & Craft Director** (`visual-critic`) | `fable-5.2-high` | Independent visual audit of screenshots (hierarchy, typography, contrast, clipping/overlap, polish, 3D framing/lighting). |
| **Product & Interaction Critic** (`ux-critic`) | `gemini-4-carbon-high` | Independent UX/product audit of flows + screenshots (affordances, feedback, dead-ends, ergonomics, onboarding, product invariants). |
| **Root-Cause Locator** (`code-locator`) | `hydrogen-l-tf-high` | Read-only code mapping **after** critics report, linking each confirmed symptom to `file:line` and estimated fix tier. |

**Key rules:**
* **Keep the coordinator on `gemini-pro-coordinator`:** Switch immediately via `swarm{action:"model", model:"gemini-pro-coordinator"}` if the session started on another model.
* **Read-only on product code:** `/review` NEVER edits application or test files (write only scratch captures/artifacts to `<artifact_dir>/review/` or `/tmp/`).
* **Blind product review first, code second:** `visual-critic` and `ux-critic` inspect the **live product evidence** (`qa-driver` screenshots + interaction logs) without reading source code first, and report independently to `@coordinator` before seeing each other's findings.
* **Image Size Guard (Mandatory):** Every agent generating or viewing screenshots MUST:
  1. Cap captured screenshots at **`<= 1280 px`** longest side (and generate **contact sheets** when >6 screens exist).
  2. Run `/usr/bin/python3 ~/.gemini/config/hooks/image_guard.py <img1> [<img2> ...]` before viewing/embedding any image and use the returned path.
  3. View **at most 4 images per turn** (contact sheets first, then individual screens for suspected flags).

---

## 4-Stage Execution Lifecycle

### Stage 1: Live Exploration & Evidence Capture (`qa-driver`)
1. Switch coordinator to `gemini-pro-coordinator` if needed, title the swarm (`swarm{action:"title", title:"Product Review: <target>"}`), and identify the product type & launch path in one quick check (e.g., Web app via Playwright/dev server on ephemeral port, Godot game via visual harness / windowed run, or CLI/native UI).
2. Spawn `qa-driver` (`model: "hydrogen-l-tf-high"`) — or `qa-driver-1..N` partitioned by surface/route/scene for multi-surface products — using the template in [brief-templates.md](file:///Users/jamesknight/work/skills/review/references/brief-templates.md).
3. `qa-driver` runs the product live and captures:
   * **Happy-path & state transitions:** Boot/landing -> core actions -> completion/empty/error/reset states.
   * **Responsive / aspect-ratio coverage:** e.g., Desktop (`1280x720`) + Mobile (`390x844`) for web, or `16:9` + `4:3` safe-frame (`Rect2(160, 0, 960, 720)`) for games/tablets.
   * **Runtime telemetry:** Console/stderr errors, layout overflow/overlap checks, touch-target/hit-box sizes, contrast/FPS/timing notes, and interactive state changes (did clicking/dragging visibly respond?).
   * **Contact sheets + capped (`<= 1280px`) PNGs** stored in the scratch directory (`<artifact_dir>/scratch/review/`), returned as an **Evidence Manifest** to `@coordinator`.

### Stage 2: Independent Dual-Lab Critique (`visual-critic` + `ux-critic`)
Launch **both** critics in parallel against `qa-driver`'s Evidence Manifest (strictly read-only; do NOT cross-post between them before they report):
1. **`visual-critic` (`model: "fable-5.2-high"`):** Audits the visual craft across contact sheets + key screen captures:
   * Visual hierarchy, focal point, whitespace/breathing room, alignment, and grid consistency.
   * Typography scale, readability, truncation, orphan/widow lines, and text-over-background contrast.
   * Clipping, overlapping controls, z-fighting, awkward crops, broken icons/assets, and 3D lighting/camera framing/material polish.
   * Aesthetic cohesion against the product's design system or target audience.
2. **`ux-critic` (`model: "gemini-4-carbon-high"`):** Audits interaction & product quality across the live flow logs + screenshots:
   * Discoverability & affordances (is it obvious what is interactive without guessing?).
   * Immediate feedback & state clarity (hover/press/loading/disabled/success/error states).
   * Dead-ends, stuck modals, confusing navigation, broken back/reset paths, and edge/empty-state handling.
   * Touch/pointer ergonomics (target sizes, safe-frame compliance, drag/tap fallbacks) and product-specific invariants (e.g., `AGENTS.md` / PRD rules).

### Stage 3: Root-Cause Mapping (`code-locator`)
1. Once both critics report, coordinator deduplicates overlapping findings and passes the list of **confirmed observed issues** to a read-only `code-locator` (`model: "hydrogen-l-tf-high"`).
2. `code-locator` locates exact `file:line` / scene/component owners, verifies whether a bug is isolated or systemic, and tags each item's likely fix tier (`hydrogen` / `carbon` / `opus`) and disjoint file group.

### Stage 4: Red / Yellow Triage, Human Gate & Fix Handoff
1. Coordinator classifies every finding using the strict rubric in [flag-schema.md](file:///Users/jamesknight/work/skills/review/references/flag-schema.md):
   * **RED (`auto_fix: true`):** Objective visual, interaction, layout, contrast, runtime-error, or invariant defects with a clear unambiguous fix. **Marked for fixing automatically.**
   * **YELLOW (`auto_fix: false`):** Subjective design/product calls, taste preferences, copy/pacing alternatives, or trade-offs with multiple valid directions. **Held for human review.**
2. Write two artifacts in `<artifact_dir>`:
   * `review_report.md` (user-facing artifact with `UserFacing: true`): Executive summary, Red Flag table (auto-queued), Yellow Flag decision cards (with screenshots run through `image_guard.py`), and sign-off checklist.
   * `review_flags.json` (scratch/handoff manifest matching [flag-schema.md](file:///Users/jamesknight/work/skills/review/references/flag-schema.md)).
3. **Human Yellow-Flag Gate:** Present the Red flags (ready to fix automatically) and ask the user which Yellow flags (e.g., `Y1, Y3`, `all`, or `none`) to promote to `approved_for_fix: true`.
4. **Handoff:** Once Yellow decisions are locked in `review_flags.json`:
   * For visual/UI/interaction/polish fixes -> recommend or invoke **`/fix`** (if available) using `review_flags.json` as input.
   * For deep architectural or feature-level rewrites -> hand off to **`/feature`**.
