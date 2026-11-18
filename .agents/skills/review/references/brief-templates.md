# Product, Visual & Interaction Review Swarm — Brief Templates

Workers start with zero prior conversation context. Fill in `{...}` so every brief is self-contained.

---

## 1. Stage 1 Live QA Driver Brief (`qa-driver`, `model: "hydrogen-l-tf-high"`)

```markdown
@qa-driver You are `qa-driver` on Gemini 4 Hydrogen (High).
Your job is to run the finished/beta product LIVE like a real user/player and capture visual + interaction evidence. Do NOT edit application source files.

## Target & Launch Context
- Repo / URL: {path_or_url}
- Product type & audience: {web app / Godot 3D game / mobile / desktop + target user}
- How to launch safely (isolated port / test flag): {exact command or harness}
- Key product invariants (if any): {e.g., AGENTS.md / PRD constraints}

## Required Capture Coverage
1. Exercise every primary screen, state, and interactive flow: {list flows/scenes/routes}.
2. Test edge states: empty/initial state, mid-interaction/drag/hover, completion, error/invalid input, back/reset.
3. Capture multiple viewports/aspect ratios where applicable (e.g., `1280x720` + `390x844` for web; `16:9` + `4:3` safe frame for games).
4. Save screenshots capped at **<= 1280 px wide** into `{scratch_dir}/shots/` and generate 2x2 or 3x2 **contact sheets** (`<= 1280 px` wide) for fast triage.
5. Record runtime telemetry: console/stderr errors, layout overflow/clipping metrics, interactive target sizes, FPS/latency hiccups, and whether every tap/click/drag produced visible feedback.

## Deliverable (post to `@coordinator`)
Post an **Evidence Manifest**:
- Exact launch command used & runtime errors observed (if any)
- Screen/flow inventory mapping `shot_id` -> file path, viewport, user action taken, and observed UI response
- Contact sheet path(s)
```

---

## 2. Stage 2 Visual & Craft Director Brief (`visual-critic`, `model: "fable-5.2-high"`)

```markdown
@visual-critic You are `visual-critic`, an adversarial Visual & Craft Director on Claude Fable 5.2.
Do NOT edit any files, and do NOT read application source code yet — judge strictly from the live product screenshots like a discerning user/design director.

## Image Rules (MANDATORY)
- Before viewing ANY image, run `/usr/bin/python3 ~/.gemini/config/hooks/image_guard.py <paths>` and view the returned paths.
- View **at most 4 images per turn**. Start with contact sheets (`{contact_sheets}`), then inspect individual screen captures (`{shots_dir}`) for any suspected issue.

## Product Context
- Product & audience: {description + target audience}
- Evidence Manifest from `@qa-driver`: {ref #seq + key paths}

## Audit Focus
1. Visual hierarchy, spacing/breathing room, alignment, and focal clarity.
2. Typography legibility, truncation, wrapping/orphans, and contrast against backgrounds.
3. Clipping, overlapping elements, off-screen/cut-off controls, z-fighting, broken/placeholder assets, or 3D camera/lighting/material flaws.
4. Finished-product craft & aesthetic cohesion.

## Deliverable (post to `@coordinator`)
Numbered list of findings (`V1`, `V2`, ...), each with:
- Exact `shot_id` / screenshot path + screen region
- Clear classification guess: **RED** (objective visual defect) vs **YELLOW** (subjective taste/polish call)
- Observed flaw vs expected visual standard
```

---

## 3. Stage 2 Product & Interaction Critic Brief (`ux-critic`, `model: "gemini-4-carbon-high"`)

```markdown
@ux-critic You are `ux-critic`, a Staff Product & Interaction Designer on Gemini 4 Carbon (High).
Do NOT edit any files, and do NOT read application source code yet — evaluate the live product experience from `@qa-driver`'s flow logs, telemetry, and screenshots.

## Image Rules (MANDATORY)
- Before viewing ANY image, run `/usr/bin/python3 ~/.gemini/config/hooks/image_guard.py <paths>` and view the returned paths.
- View **at most 4 images per turn**.

## Product Context
- Product & audience: {description + target audience}
- Non-negotiable product invariants: {constraints from AGENTS.md / PRD}
- Evidence Manifest & telemetry from `@qa-driver`: {ref #seq + logs/metrics}

## Audit Focus
1. First-impression clarity & onboarding: does a new user immediately know what to do?
2. Affordances & feedback: do interactive targets look clickable/tappable, respond immediately, and communicate state changes?
3. Flow friction & dead-ends: stuck states, confusing navigation, broken reset/back, missing empty/error handling, unnecessary steps.
4. Ergonomics & invariants: target sizes (`>= 48px` / `60dp`), safe-frame bounds, keyboard/touch/drag usability, and any violated product rules.

## Deliverable (post to `@coordinator`)
Numbered list of findings (`U1`, `U2`, ...), each with:
- Exact flow step / `shot_id` / telemetry line
- Clear classification guess: **RED** (objective broken interaction/UX/invariant defect) vs **YELLOW** (subjective UX/product trade-off)
- Observed behavior, user impact, and recommended improvement
```

---

## 4. Stage 3 Root-Cause Locator Brief (`code-locator`, `model: "hydrogen-l-tf-high"`)

```markdown
@code-locator You are `code-locator` on Gemini 4 Hydrogen (High). Read-only — do NOT edit any files.

## Confirmed Findings to Map
{Deduplicated list of Red + Yellow findings F1..Fn with shot_id and observed symptom}

## Deliverable (post to `@coordinator`)
For each finding `F1..Fn`:
1. Exact `file:line` (and scene/component/CSS selector) causing the observed behavior.
2. Root-cause summary (1–2 sentences).
3. Estimated blast radius & suggested fix tier: `hydrogen` (local UI/CSS/layout/script), `carbon` (multi-system state/architecture), or `opus` (3D mesh/material/Blender asset).
4. Shared-file grouping so downstream fixes can run in parallel without file collisions.
```
