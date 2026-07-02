"""Compose pass 0134 all-video author/theory index receipt."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from all_video_author_theory_index_sources import (
    REPO,
    ROOT,
    SOURCE_FILES,
    author_nodes,
    collect_corpus,
    negative_fixtures,
    reference_queue,
    sha256_obj,
    sha256_text,
    theory_lanes,
    write_json,
)

SCHEMA = "AllVideoAuthorTheoryIndexReceipt/v1"
PASS_ID = "0134"
STATUS_MATCH = "ALL_VIDEO_AUTHOR_THEORY_INDEX_MATCH"
STATUS_DRIFT = "ALL_VIDEO_AUTHOR_THEORY_INDEX_DRIFT"


def run_json(command: list[str], timeout: int = 90) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "All-video author reference theory index across Telos dogfood source leads."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1600", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def validation_errors(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if len(artifact["video_sources"]) < 50:
        errors.append("video_source_count")
    if len(artifact["author_nodes"]) < 20:
        errors.append("author_node_count")
    if len(artifact["theory_lanes"]) < 8 or not all(lane["status"] == "HYPOTHESIS_SOURCE_LEAD" for lane in artifact["theory_lanes"]):
        errors.append("theory_lanes")
    if len(artifact["reference_expansion_queue"]) < 15:
        errors.append("reference_queue")
    if any(row["claim_status"] != "SOURCE_LEAD_ONLY" for row in artifact["video_sources"]):
        errors.append("claim_boundary")
    if any(row["status"] != "REJECTED" for row in artifact["negative_fixtures"]):
        errors.append("negative_fixtures")
    if any(row["status"] != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagship_receipts")
    return errors


def compose() -> dict[str, Any]:
    videos, channels, invalid = collect_corpus()
    authors = author_nodes(videos)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_files": {name: str(path.relative_to(REPO)) for name, path in SOURCE_FILES.items()},
        "recovery_boundary": {
            "thread_search": "codex_app list_threads query for video/youtube/learning returned no older matching threads; current Research market gaps thread was readable and confirmed Brandom, Kane B, and compaction events.",
            "corpus_policy": "This pass indexes locally recoverable repo and Gather receipts. Anything not represented by a receipt remains outside the verified corpus.",
        },
        "video_sources": videos,
        "channel_sources": channels,
        "invalid_source_inputs": invalid,
        "author_nodes": authors,
        "theory_lanes": theory_lanes(videos, authors),
        "reference_expansion_queue": reference_queue(authors),
        "negative_fixtures": negative_fixtures(),
        "current_promoted_natural_laws": [],
        "unsupported_claim_count": 0,
        "flagship_receipts": flagship_receipts(),
    }
    artifact["validation_errors"] = validation_errors(artifact)
    artifact["status"] = STATUS_MATCH if not artifact["validation_errors"] else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "all-video-author-theory-index-pass-0134.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"], "videos": len(artifact["video_sources"]), "authors": len(artifact["author_nodes"])}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
