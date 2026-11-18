---
name: bakeoff
description: >-
  Run fair, blind-first multi-model swarm bake-offs (strict one-shot or
  self-checked) with exact transcript telemetry, a single self-contained
  Zipline-ready `index.html` comparison viewer (`base64` -> `iframe.srcdoc`),
  sortable stats table, and embedded prompt and `/bakeoff` skill tabs. Use when
  invoked via `/bakeoff` or when the user asks to compare models side-by-side,
  run a blind model bake-off, benchmark multiple models on one prompt, or
  publish a single-file comparison viewer to Zipline.
---

# Multi-Model Swarm Bake-Off (`/bakeoff`)

Run fair, parallel, blind-first comparisons across multiple models, extract exact transcript telemetry, and stitch a **single self-contained `index.html`** viewer (`hydrogen-l-tf-high`) ready to open locally or upload directly to Zipline — zero `.zip` archives and zero external/relative `.html` dependencies.

---

## Phase 1 — Interactive Setup & Contract Lock

1. **Discover available models:** Call `swarm{action:"models", all:true}` before proposing a roster so every model ID is verified live.
2. **Lock setup in 2–4 concise questions** (use `ask_question` when multiple-choice fits):
   * **Model roster** — Default: 4-model Gemini High lineup (`gemini-4-carbon-high`, `gemini-launch-candidate-high`, `gemini-4-neon-high`, `hydrogen-l-tf-high`), or any subset/models from `swarm models`.
   * **Rules / Strictness** — Default: **strict one-shot** (single `write_file` call, zero cross-reading of sibling files, zero preview/browser/iteration loops). Alternative: allow local build/test self-check before finishing.
   * **Output directory** — Default: fresh directory outside the active repo (e.g. `~/work/personal/<slug>-bakeoff/`).
   * **Viewer & publishing options** — Default: blind-first randomized grid, `Tab` to reveal/hide model titles, sortable stats table, embedded verbatim prompt + `/bakeoff` skill tabs, compiled into a single self-contained `index.html` for direct Zipline upload.
3. **Approve the exact contestant prompt:** Present the verbatim draft prompt (with a `<model>.html` target placeholder) to the user for a quick go-ahead before spawning any contestant.

---

## Phase 2 — Fair Parallel Swarm Execution

1. **Prepare the directory:** Create `<dir>` cleanly (`mkdir -p <dir>`).
2. **Launch in one parallel turn:**
   * Name the swarm (`swarm{action:"title", title:"<Topic> Bake-Off"}`).
   * Spawn `monitor` (ONLY if `swarm_monitor` is in your active skill list).
   * Launch all contestant workers in **one turn** via `swarm{action:"add"}`, each pinned to its exact `model` ID, owning only `<dir>/<slug>.html` (`workspace: "inherit"` since paths are disjoint).
3. **Record every `conversation_id`** returned by `swarm add` — Phase 3 needs them to read each worker's transcript.
4. **Fairness guardrails (enforce in every contestant brief):**
   * **Identical prompt** across all contestants, differing **only** in the target output path (`<dir>/<slug>.html`).
   * **Zero identifying UI chrome:** Contestant outputs must omit titles, headers, badges, watermarks, or model names so blind evaluation stays unspoiled.
   * **Isolation:** Contestants must never read sibling files or inspect other workers' outputs. In strict one-shot mode, require a single `write_file` call and immediate `@coordinator` report with zero test/preview loops.

---

## Phase 3 — Exact Telemetry Extraction

Once every contestant reports completion, run the bundled telemetry script (never invent, estimate, or round-by-hand any numbers):

```bash
python3 /Users/jamesknight/work/skills/bakeoff/scripts/extract_metrics.py \
  --brain-dir <appDataDir>/brain \
  --out-dir <dir> \
  --contestants '[
    {"slug":"carbon","display":"Gemini 4 Carbon (High)","model_id":"gemini-4-carbon-high","file":"carbon.html","conversation_id":"<id>"},
    {"slug":"argon","display":"Gemini 4 Argon (High)","model_id":"gemini-launch-candidate-high","file":"argon.html","conversation_id":"<id>"},
    {"slug":"neon","display":"Gemini 4 Neon (High)","model_id":"gemini-4-neon-high","file":"neon.html","conversation_id":"<id>"},
    {"slug":"hydrogen","display":"Gemini 4 Hydrogen (High)","model_id":"hydrogen-l-tf-high","file":"hydrogen.html","conversation_id":"<id>"}
  ]'
```

(`--contestants` also accepts a path to a `.json` file; pass `--embed-html` to also include `html_b64` per entry if writing a JSON bundle directly for stitching.)

The script reads each worker's `<brain-dir>/<conversation_id>/.system_generated/logs/transcript.jsonl` plus its generated file and emits exact JSON fields:
`slug`, `display`, `model_id`, `file`, `gen_sec`, `total_sec`, `gen_input_tokens`, `gen_output_tokens`, `total_output_tokens`, `tok_per_sec`, `bytes`, `kb`, `lines`.

---

## Phase 4 — Final Stitcher (`hydrogen-l-tf-high`)

Spawn one `stitcher` worker pinned to `model: "hydrogen-l-tf-high"` to assemble a **single self-contained `<dir>/index.html`** using the exact telemetry from Phase 3. Keep the raw contestant HTML files untouched on disk as source artifacts.

### Single-File or Directory Zipline Packaging
* **Single-file contestants (default — HTML/Three.js/Canvas):** Embed every contestant's HTML inside `<dir>/index.html` as **UTF-8 base64** strings (generated via Python `base64.b64encode(Path(f).read_bytes()).decode("ascii")`, never raw unescaped HTML so `</script>` inside contestant files can never break the outer page) and decode into `iframe.srcdoc`. This produces one portable `index.html` that works both uploaded solo or as a directory.
* **Multi-file contestants (apps with assets/bundles):** Zipline also accepts uploading the whole `<dir>/` directory directly, so when contestants output subdirectories (`<dir>/<slug>/index.html` + assets), point each iframe at `./<slug>/index.html` (same-origin key forwarding still works when served).
* **Runtime UTF-8 decode into `iframe.srcdoc`:**
  ```js
  function decodeUtf8Base64(b64) {
    const bin = atob(b64);
    const bytes = Uint8Array.from(bin, (c) => c.charCodeAt(0));
    return new TextDecoder("utf-8").decode(bytes);
  }
  iframe.srcdoc = decodeUtf8Base64(entry.html_b64);
  ```
* **Same-origin guarantee:** Because `srcdoc` iframes inherit the parent document's exact origin, `iframe.contentWindow.addEventListener("keydown", ...)` works reliably when `index.html` is uploaded standalone to Zipline OR opened directly from disk (`file://`) or `http.server`.

### Required Viewer UX
* **Self-contained shell:** Pure vanilla HTML/CSS/JS, zero external CSS/JS dependencies, system UI + monospace (`tabular-nums`) fonts.
* **Responsive full-viewport grid:** `100vw × 100vh`, dark slate frame (`#0b0f17`), crisp `1px` hairlines, zero page scrollbars, grid geometry matched to contestant count (`1×2`, `1×3`, `2×2`, `2×3`, etc.).
* **Blind-first randomized order:** Shuffle contestants on page load into slots `Entry A`, `Entry B`, `Entry C`, ... (include a `Shuffle` button in the bottom pill bar). While blind, never leak filenames or model names in visible text, badges, or tooltips.
* **`Tab` to reveal / hide model titles:**
  * Pressing `Tab` (with `e.preventDefault()`) toggles blind vs. revealed badges (e.g., `Entry A` ↔ `A · Gemini 4 Neon (High)` with subtle accent).
  * **CRITICAL iframe key forwarding:** Attach the exact same `keydown` handler (`Tab`, `S`, `P`, `?`, `1–N`, `Esc`) to **both** the parent `window` **and** every `iframe.contentWindow` inside each iframe's `load` handler (wrapped in `try/catch`). Otherwise clicking or orbiting inside an interactive/3D iframe traps keyboard focus and breaks `Tab`.
* **Solo / Fullscreen view:** Keys `1–N` or each pane's corner expand button solo that slot; `Esc` or clicking again returns to the grid. Keep all iframes mounted via CSS (never destroy/reload them) so WebGL scenes and camera state persist.
* **3-Tab Overlay Modal** (compact bottom pill bar + hotkeys `S`, `P`, `?`, plus a tab switcher inside the modal; `Esc` or backdrop click closes):
  1. **Comparison Stats Table (`S`):** Sortable table with Entry (`A–N`), Model (masked while blind and synced with `Tab` + an in-modal Reveal/Hide toggle), Gen Time (`m:ss`), Output Tokens (`gen_output_tokens`, with footnote noting this includes thinking + generated code tokens), Throughput (`tok/s`), Input Tokens (`gen_input_tokens`), File Size (`KB`) & Lines of Code, inline visual bars, and a per-row `Inspect` button to solo that pane.
  2. **Prompt (`P`):** Exact verbatim contestant prompt used in the bake-off (with `<model>.html` placeholder) in a readable `<pre>` block with a one-click **Copy** button.
  3. **`/bakeoff` Skill (`?`):** Full verbatim contents of `/Users/jamesknight/work/skills/bakeoff/SKILL.md` in a scrollable `<pre>` block with a one-click **Copy** button.

---

## Phase 5 — Verification & Zipline Delivery

1. **Verify `<dir>/index.html` cleanly before delivery:**
   * Extract the outer `<script>` block from `<dir>/index.html` and check syntax with `node --check` (zero JS syntax errors).
   * Verify via Python that every embedded `html_b64` payload in `<dir>/index.html` decodes cleanly as UTF-8 to valid HTML (`<!DOCTYPE html>` / `<html`) matching its source `<slug>.html` byte-for-byte, and that no raw relative `<iframe src="./...">` dependency remains.
   * Confirm all raw source `<slug>.html` files remain untouched on disk alongside the standalone `index.html`.
2. **Deliver for Zipline & local viewing:**
   * Upload either `<dir>/index.html` alone (for single-file bake-offs) or the whole `<dir>/` directory directly to Zipline. *(Optional extension: if a Zipline CLI or upload API URL/token is configured in the environment, chain the direct upload command and return the live URL.)*
   * Post `[done] <summary>` on the board if `monitor` is active, then kill finished workers once verified.
   * Report to the user:
     * Standalone Zipline-ready file path: `<dir>/index.html` (and file size)
     * Local preview command: `python3 -m http.server 8000 --directory <dir>` (or open `<dir>/index.html` directly)
     * Concise telemetry summary table and reminder of hotkeys (`Tab` reveal, `1–N` solo, `S` stats, `P` prompt, `?` skill, `Esc` back).
