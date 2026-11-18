# Red / Yellow Flag Rubric & Handoff Schema

## Classification Rubric

### RED FLAGS (`severity: "red"`, `auto_fix: true`)
Objective defects any user or product owner would agree are broken or wrong:
- **Broken or dead-end interaction:** Control does not respond, action fails silently, modal traps user, flow cannot complete or reset.
- **Runtime / console error:** Uncaught exceptions, script errors, failed asset loads, or broken network calls during normal use.
- **Layout & clipping defects:** Overlapping text/buttons, clipped labels, horizontal overflow, controls pushed outside `4:3` / mobile viewport safe frames.
- **Legibility & contrast failures:** Text/icons unreadable against background (`< 4.5:1` for normal text, `< 3:1` for large UI), unintended placeholder text (`TODO`, `Lorem`, debug labels).
- **Missing state feedback:** No visible hover/press/loading/disabled/confirmation feedback on interactive controls, or frozen/laggy state transition.
- **Ergonomic & product invariant violations:** Undersized touch targets (`< 48px` web / `< 60dp` child UX), missing tap fallback for drag-only controls, or broken project rules (e.g., text in a zero-text child UI).

### YELLOW FLAGS (`severity: "yellow"`, `auto_fix: false`, `needs_human_review: true`)
Subjective design, product, or scope calls that **must not** be auto-fixed without human approval:
- **Aesthetic & taste choices:** Alternative color harmony, icon style, animation pacing, typography weight tweaks when current version is already legible.
- **UX density & layout trade-offs:** Reordering sections, collapsing vs. expanding panels, changing onboarding copy/tone, adding new shortcuts or helper hints.
- **Scope / feature additions:** Nice-to-have polish features, extra celebration effects, or new settings that were not clearly broken.
- **Ambiguous intent:** Quirks that might be intentional stylistic choices (e.g., playful asymmetry, minimal chrome, deliberate friction).

---

## Machine-Readable Manifest (`review_flags.json`)

Write to `<artifact_dir>/scratch/review/review_flags.json` (or `<repo>/review_flags.json` if the user asks to commit/track it):

```json
{
  "target": "string (app/game name or path)",
  "reviewed_at": "ISO-8601 timestamp",
  "target_state": "beta | final",
  "launch_command": "exact command to run/verify live",
  "summary": {
    "red_count": 0,
    "yellow_count": 0,
    "approved_yellow_ids": []
  },
  "flags": [
    {
      "id": "R1",
      "severity": "red",
      "category": "layout | interaction | visual | contrast | ergonomics | invariant | runtime",
      "title": "Short descriptive title",
      "evidence": {
        "shot_id": "screen_03",
        "screenshot_path": "/abs/path/to/shot.png",
        "viewport": "1280x720",
        "repro_steps": ["Step 1", "Step 2"]
      },
      "observed": "What actually happened on screen",
      "expected": "Clear objective bar",
      "root_cause": {
        "files": ["src/ui/hud.gd:42"],
        "summary": "Brief technical cause",
        "fix_tier": "hydrogen | carbon | opus"
      },
      "auto_fix": true,
      "approved_for_fix": true,
      "human_decision": "auto"
    }
  ]
}
```

For Yellow flags, initialize `"auto_fix": false`, `"approved_for_fix": false`, and `"human_decision": "pending"` until the user approves (`"approved"`) or rejects (`"wont_fix"`) each item in Stage 4.
