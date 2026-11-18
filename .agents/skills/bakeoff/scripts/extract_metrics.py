#!/usr/bin/env python3
"""Extract exact timing, token, and file-size metrics for /bakeoff runs.

Reads each contestant's Jetski transcript (`transcript.jsonl`) and generated
output file, then emits a JSON array ready to embed in the bake-off viewer.
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


WRITE_TOOLS = {
    "write_file",
    "edit_file",
    "replace_file_content",
    "multi_replace_file_content",
}


def parse_iso_ts(value: str) -> datetime:
    """Parse an ISO-8601 timestamp string (including trailing 'Z')."""
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def tool_names(step: dict[str, Any]) -> list[str]:
    """Return tool call names invoked in a transcript step."""
    calls = step.get("tool_calls") or []
    names: list[str] = []
    for call in calls:
        if isinstance(call, dict) and call.get("name"):
            names.append(str(call["name"]))
    return names


def step_completion_ts(steps: list[dict[str, Any]], planner_idx: int) -> datetime:
    """Find completion timestamp for a PLANNER_RESPONSE using following GENERIC steps."""
    base_ts = parse_iso_ts(steps[planner_idx]["created_at"])
    latest = base_ts
    j = planner_idx + 1
    while j < len(steps):
        nxt = steps[j]
        if nxt.get("type") != "GENERIC":
            break
        ts_str = nxt.get("created_at")
        if ts_str:
            ts = parse_iso_ts(ts_str)
            if ts > latest:
                latest = ts
        j += 1
    return latest


def extract_transcript_metrics(transcript_path: Path) -> dict[str, Any]:
    """Compute exact timing and token metrics from a worker's transcript.jsonl."""
    steps: list[dict[str, Any]] = []
    with transcript_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            steps.append(json.loads(line))

    if not steps:
        raise ValueError(f"Empty transcript: {transcript_path}")

    planner_indices = [
        i for i, s in enumerate(steps) if s.get("type") == "PLANNER_RESPONSE"
    ]
    if not planner_indices:
        raise ValueError(f"No PLANNER_RESPONSE steps found in {transcript_path}")

    first_planner_idx = planner_indices[0]
    first_ts = parse_iso_ts(steps[first_planner_idx]["created_at"])

    write_indices = [
        i
        for i in planner_indices
        if any(name in WRITE_TOOLS for name in tool_names(steps[i]))
    ]

    if write_indices:
        last_write_idx = write_indices[-1]
        gen_indices = [i for i in planner_indices if i <= last_write_idx]
    else:
        gen_indices = list(planner_indices)

    gen_start_ts = parse_iso_ts(steps[gen_indices[0]]["created_at"])
    gen_end_ts = step_completion_ts(steps, gen_indices[-1])

    post_after_gen = [
        i
        for i in planner_indices
        if i >= gen_indices[-1] and "post_message" in tool_names(steps[i])
    ]
    last_run_idx = post_after_gen[0] if post_after_gen else gen_indices[-1]
    all_run_indices = [i for i in planner_indices if i <= last_run_idx]
    total_end_ts = step_completion_ts(steps, last_run_idx)

    gen_sec = max(0, int(round((gen_end_ts - gen_start_ts).total_seconds())))
    total_sec = max(gen_sec, int(round((total_end_ts - first_ts).total_seconds())))

    gen_input_tokens = sum(
        int(steps[i].get("input_tokens") or 0) for i in gen_indices
    )
    gen_output_tokens = sum(
        int(steps[i].get("output_tokens") or 0) for i in gen_indices
    )
    total_output_tokens = sum(
        int(steps[i].get("output_tokens") or 0) for i in all_run_indices
    )
    tok_per_sec = round(gen_output_tokens / gen_sec, 1) if gen_sec > 0 else 0.0

    return {
        "gen_sec": gen_sec,
        "total_sec": total_sec,
        "gen_input_tokens": gen_input_tokens,
        "gen_output_tokens": gen_output_tokens,
        "total_output_tokens": total_output_tokens,
        "tok_per_sec": tok_per_sec,
    }


def extract_file_metrics(file_path: Path) -> dict[str, Any]:
    """Compute exact byte size, KiB, and line count for a generated file."""
    size_bytes = file_path.stat().st_size
    with file_path.open("rb") as fh:
        lines = sum(1 for _ in fh)
    return {
        "bytes": size_bytes,
        "kb": round(size_bytes / 1024.0, 1),
        "lines": lines,
    }


def load_contestants(raw_spec: str) -> list[dict[str, Any]]:
    """Load contestant definitions from an inline JSON string or JSON file path."""
    stripped = raw_spec.strip()
    if stripped.startswith("[") or stripped.startswith("{"):
        parsed = json.loads(stripped)
    else:
        spec_path = Path(raw_spec).expanduser()
        parsed = json.loads(spec_path.read_text(encoding="utf-8"))

    if isinstance(parsed, dict) and "contestants" in parsed:
        parsed = parsed["contestants"]
    if not isinstance(parsed, list):
        raise ValueError("--contestants must decode to a JSON array of objects")
    return parsed


def resolve_output_file(out_dir: Path, file_field: str) -> tuple[Path, str]:
    """Resolve disk path and clean relative './<name>' path for the viewer."""
    candidate = Path(file_field)
    if candidate.is_absolute():
        resolved = candidate
        rel_path = f"./{candidate.name}"
    else:
        clean_rel = str(candidate).lstrip("./")
        resolved = out_dir / clean_rel
        rel_path = f"./{clean_rel}"
    return resolved, rel_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract exact timing, token, and file metrics for /bakeoff runs."
    )
    parser.add_argument(
        "--brain-dir",
        default="~/.gemini/jetski/brain",
        help="Path to <appDataDir>/brain directory containing worker transcripts.",
    )
    parser.add_argument(
        "--out-dir",
        required=True,
        help="Directory containing generated contestant output files.",
    )
    parser.add_argument(
        "--contestants",
        required=True,
        help=(
            "JSON array (or path to JSON file) of contestant objects with "
            "slug, display, model_id, file, and conversation_id."
        ),
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write the resulting JSON array in addition to stdout.",
    )
    parser.add_argument(
        "--embed-html",
        action="store_true",
        help="Include base64-encoded file contents as 'html_b64' for single-file iframe.srcdoc stitching.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    brain_dir = Path(args.brain_dir).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()

    try:
        contestants = load_contestants(args.contestants)
    except Exception as exc:
        print(f"Error parsing --contestants: {exc}", file=sys.stderr)
        return 2

    results: list[dict[str, Any]] = []
    for idx, entry in enumerate(contestants):
        required = ("slug", "display", "model_id", "file", "conversation_id")
        missing = [k for k in required if not entry.get(k)]
        if missing:
            print(
                f"Error: contestant[{idx}] missing required keys: {', '.join(missing)}",
                file=sys.stderr,
            )
            return 2

        conv_id = str(entry["conversation_id"])
        transcript_path = (
            brain_dir / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
        )
        if not transcript_path.is_file():
            print(f"Error: transcript not found: {transcript_path}", file=sys.stderr)
            return 1

        file_path, rel_file = resolve_output_file(out_dir, str(entry["file"]))
        if not file_path.is_file():
            print(f"Error: output file not found: {file_path}", file=sys.stderr)
            return 1

        t_metrics = extract_transcript_metrics(transcript_path)
        f_metrics = extract_file_metrics(file_path)

        record: dict[str, Any] = {
            "slug": str(entry["slug"]),
            "display": str(entry["display"]),
            "model_id": str(entry["model_id"]),
            "file": rel_file,
            "gen_sec": t_metrics["gen_sec"],
            "total_sec": t_metrics["total_sec"],
            "gen_input_tokens": t_metrics["gen_input_tokens"],
            "gen_output_tokens": t_metrics["gen_output_tokens"],
            "total_output_tokens": t_metrics["total_output_tokens"],
            "tok_per_sec": t_metrics["tok_per_sec"],
            "bytes": f_metrics["bytes"],
            "kb": f_metrics["kb"],
            "lines": f_metrics["lines"],
        }
        if args.embed_html:
            record["html_b64"] = base64.b64encode(file_path.read_bytes()).decode("ascii")
        results.append(record)

    rendered = json.dumps(results, indent=2)
    if args.output:
        out_path = Path(args.output).expanduser()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered + "\n", encoding="utf-8")

    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
