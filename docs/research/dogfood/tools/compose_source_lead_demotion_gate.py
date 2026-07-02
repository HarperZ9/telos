"""Compose pass 0126 source-lead demotion gate receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "SourceLeadDemotionGateReceipt/v1"
PASS_ID = "0126"
STATUS_MATCH = "SOURCE_LEAD_DEMOTION_GATE_MATCH"
STATUS_DRIFT = "SOURCE_LEAD_DEMOTION_GATE_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PASS_0125 = ROOT / "schemas" / "youtube-experiment-router-pass-0125.json"
PASS_0124 = ROOT / "schemas" / "agent-action-proof-packet-factory-adapter-pass-0124.json"

INDEPENDENT_EVIDENCE = {"crucible_match", "formal_artifact", "runtime_receipt", "experiment_receipt", "code_receipt", "paper"}
SAFE_SOURCE_STATUSES = {"SOURCE_LEAD_ONLY", "HYPOTHESIS"}
FACT_STATUSES = {"VERIFIED_FACT", "PROBE_MATCH", "CRUCIBLE_MATCH", "LAW_CANDIDATE", "PROMOTED_LAW"}

FIXTURES = [
    {
        "fixture_id": "source_lead_only_ok",
        "requested_status": "SOURCE_LEAD_ONLY",
        "video_ids": ["HbKzqvey5PA"],
        "raw_transcript_included": False,
        "evidence": [{"kind": "video_metadata", "ref": "HbKzqvey5PA", "source": "video"}],
        "expected_status": "ACCEPTED",
    },
    {
        "fixture_id": "hypothesis_routing_ok",
        "requested_status": "HYPOTHESIS",
        "video_ids": ["4MQbd5wTlI8", "EdVG5qNm2rY"],
        "raw_transcript_included": False,
        "evidence": [{"kind": "video_transcript_hash", "ref": "pass-0125", "source": "video"}],
        "expected_status": "ACCEPTED",
    },
    {
        "fixture_id": "independent_probe_ok",
        "requested_status": "PROBE_MATCH",
        "video_ids": ["nYwid6Q5HXk"],
        "raw_transcript_included": False,
        "evidence": [{"kind": "crucible_match", "ref": "pass-0124-run", "source": "local_artifact"}],
        "expected_status": "ACCEPTED",
    },
    {
        "fixture_id": "video_only_fact_rejected",
        "requested_status": "VERIFIED_FACT",
        "video_ids": ["EdVG5qNm2rY"],
        "raw_transcript_included": False,
        "evidence": [{"kind": "video_transcript_hash", "ref": "EdVG5qNm2rY", "source": "video"}],
        "expected_status": "REJECTED",
        "expected_failures": ["video_only_promotion", "missing_independent_evidence"],
    },
    {
        "fixture_id": "video_law_rejected",
        "requested_status": "PROMOTED_LAW",
        "video_ids": ["HbKzqvey5PA"],
        "raw_transcript_included": False,
        "evidence": [{"kind": "video_metadata", "ref": "HbKzqvey5PA", "source": "video"}],
        "expected_status": "REJECTED",
        "expected_failures": ["law_promotion_forbidden", "video_only_promotion", "missing_independent_evidence"],
    },
    {
        "fixture_id": "raw_transcript_rejected",
        "requested_status": "HYPOTHESIS",
        "video_ids": ["4MQbd5wTlI8"],
        "raw_transcript_included": True,
        "evidence": [{"kind": "raw_transcript", "ref": "inline", "source": "video"}],
        "expected_status": "REJECTED",
        "expected_failures": ["raw_transcript_included"],
    },
    {
        "fixture_id": "keyword_count_as_proof_rejected",
        "requested_status": "CRUCIBLE_MATCH",
        "video_ids": ["nYwid6Q5HXk"],
        "raw_transcript_included": False,
        "evidence": [{"kind": "keyword_signal_count", "ref": "pass-0125", "source": "derived_video_signal"}],
        "expected_status": "REJECTED",
        "expected_failures": ["keyword_count_not_proof", "missing_independent_evidence"],
    },
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def has_independent_evidence(fixture: dict[str, Any]) -> bool:
    for row in fixture["evidence"]:
        if row["kind"] in INDEPENDENT_EVIDENCE and row.get("source") != "video":
            return True
    return False


def evaluate_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    requested = fixture["requested_status"]
    evidence_kinds = {row["kind"] for row in fixture["evidence"]}
    independent = has_independent_evidence(fixture)

    if fixture.get("raw_transcript_included"):
        failures.append("raw_transcript_included")
    if "keyword_signal_count" in evidence_kinds and requested in FACT_STATUSES:
        failures.append("keyword_count_not_proof")
    if requested == "PROMOTED_LAW":
        failures.append("law_promotion_forbidden")
    if requested in FACT_STATUSES and not independent:
        if any(row.get("source") in {"video", "derived_video_signal"} for row in fixture["evidence"]):
            failures.append("video_only_promotion")
        failures.append("missing_independent_evidence")
    if requested not in SAFE_SOURCE_STATUSES and requested in FACT_STATUSES and independent and requested == "PROMOTED_LAW":
        failures.append("promoted_law_requires_external_review")

    failures = sorted(set(failures))
    status = "REJECTED" if failures else "ACCEPTED"
    return {
        **fixture,
        "gate_status": status,
        "failures": failures,
        "independent_evidence": independent,
        "matches_expected": status == fixture["expected_status"] and set(failures) >= set(fixture.get("expected_failures", [])),
    }


def run_json(command: list[str], timeout: int = 60) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0126 source-lead demotion gate for video-derived claims."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def compose() -> dict[str, Any]:
    router = read_json(PASS_0125)
    adapter = read_json(PASS_0124)
    results = [evaluate_fixture(row) for row in FIXTURES]
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {
            "youtube_router_pass": router["pass"],
            "youtube_router_seal": router["seal"],
            "agent_action_adapter_pass": adapter["pass"],
            "agent_action_adapter_seal": adapter["seal"],
        },
        "policy": {
            "source_lead_safe_statuses": sorted(SAFE_SOURCE_STATUSES),
            "fact_statuses_requiring_independent_evidence": sorted(FACT_STATUSES - {"PROMOTED_LAW"}),
            "promoted_law_policy": "always_reject_in_this_gate",
            "independent_evidence_kinds": sorted(INDEPENDENT_EVIDENCE),
            "raw_transcript_policy": "reject_packet_exports",
            "keyword_count_policy": "routing_signal_only_not_proof",
        },
        "source_lead_summary": [{"video_id": row["video_id"], "claim_status": row["claim_status"], "dominant_signal": row["dominant_signal"], "raw_transcript_included": row["raw_transcript_included"]} for row in router["youtube_source_leads"]],
        "gate_fixtures": results,
        "accepted_count": sum(row["gate_status"] == "ACCEPTED" for row in results),
        "rejected_count": sum(row["gate_status"] == "REJECTED" for row in results),
        "primary_guardrail": "reject unsupported video-to-fact or video-to-law promotion before runtime router execution",
        "non_promotion_statement": "Pass 0126 is a demotion and rejection gate. It does not validate video claims, expose raw transcripts, declare market fit, or promote a natural law.",
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "flagship_receipts": flagship_receipts(),
    }
    errors = []
    if len(results) != 7 or any(not row["matches_expected"] for row in results):
        errors.append("fixture_expectations")
    if artifact["accepted_count"] != 3 or artifact["rejected_count"] != 4:
        errors.append("gate_counts")
    if any(row["raw_transcript_included"] for row in artifact["source_lead_summary"]):
        errors.append("source_summary_raw_transcripts")
    if not all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "source-lead-demotion-gate-pass-0126.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
