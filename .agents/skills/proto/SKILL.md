---
name: proto
description: >-
  Rapid flash-prototyping workflow using EXCLUSIVELY Gemini 4 Hydrogen
  (`hydrogen-l-tf-high`). Skips multi-model planning and Fable review swarms in
  favor of fast parallel Hydrogen workers with disjoint file ownership, upfront
  shared contracts, self-verified builds, and immediate run or Cloud Run
  deployment. Use when invoked via `/proto` or when the user asks to flash
  prototype, rapid prototype, build a quick live demo or MVP fast, or requests
  Hydrogen-only execution without Fable review gates.
---

# Hydrogen Flash Prototype (100% Gemini 4 Hydrogen, Zero Review Ceremony)

Build and ship working demos, MVPs, and live prototypes at maximum speed using **EXCLUSIVELY Gemini 4 Hydrogen (`hydrogen-l-tf-high`)**.

---

## Hard Rule: EXCLUSIVELY Hydrogen

Every agent participating in this workflow MUST run on Hydrogen:

1. **Pin every swarm worker to `model: "hydrogen-l-tf-high"`** — including builders, frontend, backend, deployer, verifier, **and `monitor`** (if `swarm_monitor` is active in your skill list).
2. **Switch the coordinator to Hydrogen if it isn't already:** Once the swarm exists, call `swarm{action:"model", model:"hydrogen-l-tf-high"}` (with `name` omitted or `"coordinator"`) if your session didn't start on Hydrogen.
3. **Never use non-Hydrogen models:**
   * **NEVER** spawn `fable-*`, `carbon-*`, `opus-*`, or `gemini-3.8-flash-*` workers.
   * **NEVER** use `invoke_subagent` with `flash`, `flash_lite`, `pro`, or non-Hydrogen `inherit` (`invoke_subagent` cannot select `hydrogen-l-tf-high`). Route all delegated/parallel work through `swarm`!
   * **Propagate to helpers:** Tell every worker in its brief: *"If you spawn helpers via `swarm add`, pin `model: "hydrogen-l-tf-high"`."*
4. **Quota fallback:** Only switch a member to `hydrogen-l-tf-medium` if `hydrogen-l-tf-high` hits quota exhaustion (and tell the user). Never cross to non-Hydrogen models unless the user explicitly asks.

---

## Speed-First Prototyping Loop

### 1. 30-Second Preflight & Contract Lock (No Separate Planner Phase)
* Run **one** quick read-only check of the target directory and local/cloud toolchain (e.g., `ls`, `node`/`python3`, and `gcloud config list` / `gcloud projects list` if deploying).
* **Skip** `fable-planner`, multi-page blueprint documents, and formal plan-review gates.
* If the prototype is a **web app**, lock in the **UI Direction** below right in the initial worker briefs.
* **Lock the shared contract upfront** before spawning workers: exact routes, JSON payloads, ports, env vars, and visual tokens.

### 2. Immediate Parallel Fan-Out (`hydrogen-l-tf-high`)
* **Scale proportionally:** For a tiny single-file script, build it directly (if on Hydrogen) or with 1–2 workers. For a full-stack or multi-view prototype, launch all workers in **one turn**, each with **strictly disjoint file ownership** (`workspace: "inherit"` when paths never overlap; `"share"` if edits/builds collide):
  * `backend`: server, scoring/domain logic, persistence (keep lightweight — in-memory + `/tmp` JSON or SQLite unless DB explicitly requested), `Dockerfile` + `.dockerignore`, and endpoint smoke tests.
  * `frontend` (or separate `presenter-ui` / `survey-ui` / `admin-ui` workers when views are distinct): HTML/CSS/JS, syntax checks (`node --check` / `tsc --noEmit`), and live UI/viewport verification against `backend` on an isolated ephemeral port.
  * `deployer` (when cloud deployment is requested):
    * **Phase 1 (immediately in parallel while builders code):** check target project, org policies (e.g., whether `--allow-unauthenticated` / `allUsers` works if mobile/public access is needed), and enabled APIs (`run`, `cloudbuild`, `artifactregistry`), and report ready.
    * **Phase 2 (after builders report ready):** run quick local smoke check, deploy, verify every live endpoint with `curl`, and reset any test/seed data so the demo starts clean.
  * `monitor` (ONLY if `swarm_monitor` is in your skill list): `model: "hydrogen-l-tf-high"`.

### 3. Self-Verification & Contract Sync (No Fable Review Swarm)
* Every Hydrogen builder verifies its own slice **before** reporting done (syntax checks, isolated test port `curl` checks, or headless viewport check for UI).
* Do **not** spawn `fable-reviewer` or a multi-reviewer audit swarm.
* As coordinator, verify schema alignment across worker posts on the board (`#seq`), forward small contract deltas immediately if fields drift, and **hold `deploy` until all builders report green** so static/frontend files are not snapshotted mid-write.

### 4. Ship Live & Iterate Fast
* Once live URL / local run commands are verified, post `[done] <summary>` on the board (if `monitor` is active).
* Hand over to the user immediately with:
  * Exact live URL(s) or local launch command
  * Quick test/seed instructions for demoing
  * Concise file & verification summary — ready for rapid follow-up iterations on the same standing Hydrogen swarm (keep workers warm in `waiting` state if the user is actively iterating!).

---

## UI Direction (Default for Web Prototypes)

Unless the user asks for a different aesthetic, default to a **super simple, minimalist, high-contrast UI** with generous whitespace and a restrained color palette:

* **Clean, spacious layout:** Prioritize breathing room over density (`32–48px` section gaps, `24–32px` internal padding). Separate sections with whitespace and subtle `1px` hairlines (`rgba(15, 23, 42, 0.10)`) rather than heavy drop shadows or nested cards-within-cards.
* **One clear focus per view:** Keep navigation slim, surface only essential controls for the task, and trim decorative chrome, multi-column clutter, and filler copy.
* **High contrast, simple colors:** Pair a calm light canvas (e.g., `#FFFFFF` / `#F8F9FA` or `#F6F4EF` with `#FFFFFF` surfaces) with deep ink (`#0F172A` / `#141619`) and readable slate secondary text (`#475569`–`#5B6370`) — never faint low-contrast gray. Use **one confident primary color** (e.g., cobalt `#1D4ED8` or deep emerald `#0E6B5E` with a soft tint wash) plus at most one supporting semantic accent (e.g., warm amber `#B4690E` or terracotta/crimson `#C4532D`/`#E11D48`). Keep all text/button contrast `>= 4.5:1`.
* **Sharp typography & ergonomics:** Use `Plus Jakarta Sans` (or `Inter`) with clear size hierarchy and tight heading tracking, `JetBrains Mono` with `tabular-nums` for numbers/codes, a single `<h1>`, unique `id`s on interactive controls, `>= 48px` touch targets on mobile, and zero horizontal overflow.
* **Avoid AI-template clutter:** No purple-on-dark themes, glowing/neon borders, gradient headline text, pulsing-dot pills above headlines, grid/mesh backgrounds, or icon-stuffed bento boxes.
