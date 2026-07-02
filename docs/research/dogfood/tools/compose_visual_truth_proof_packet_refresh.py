"""Compose pass 0081 visual-truth proof-packet refresh."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


SCHEMA = "VisualTruthProofPacketRefresh/v1"
PASS_ID = "0081"
STATUS_MATCH = "VISUAL_TRUTH_PROOF_PACKET_REFRESH_MATCH"
STATUS_DRIFT = "VISUAL_TRUTH_PROOF_PACKET_REFRESH_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BUILD_COLOR_ROOT = Path("C:/dev/public/build-color")
TEST_COMMAND = [
    "python",
    "-m",
    "pytest",
    "tests/test_spaces.py",
    "tests/test_tonemap.py::TestPQRoundtrip",
    "tests/test_difference.py::TestCIEDE2000KnownPairs",
]
FORUM_TEXT = (
    "Package a visual truth and color calibration proof packet for Project Telos: "
    "bind Build Color software metrics, color calibration market gaps, negative "
    "hardware-calibration boundaries, and buyer-facing proof evidence without "
    "claiming physical display calibration."
)
SOURCE_PATHS = [
    "README.md",
    "pyproject.toml",
    "build_color/spaces.py",
    "build_color/tonemap.py",
    "build_color/difference.py",
    "tests/test_spaces.py",
    "tests/test_tonemap.py",
    "tests/test_difference.py",
]


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def source_refs() -> list[dict[str, Any]]:
    refs = []
    for rel in SOURCE_PATHS:
        path = BUILD_COLOR_ROOT / rel
        refs.append({
            "schema": "project-telos.source-ref/v1",
            "kind": "file",
            "repo": "build-color",
            "path": rel,
            "exists": path.exists(),
            "sha256": sha256_file(path) if path.exists() else None,
            "raw_payload_included": False,
        })
    return refs


def run_tests() -> dict[str, Any]:
    result = subprocess.run(TEST_COMMAND, cwd=BUILD_COLOR_ROOT, capture_output=True, text=True)
    text = result.stdout + "\n" + result.stderr
    match = re.search(r"(\d+) passed in ([0-9.]+)s", text)
    passed = int(match.group(1)) if match else 0
    seconds = float(match.group(2)) if match else None
    return {
        "command": " ".join(TEST_COMMAND),
        "cwd": str(BUILD_COLOR_ROOT),
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "passed": passed,
        "seconds": seconds,
        "status": "MATCH" if result.returncode == 0 and passed == 88 else "DRIFT",
    }


def run_forum_route() -> dict[str, Any]:
    result = subprocess.run(["forum", "route", "--json", FORUM_TEXT], cwd=REPO, capture_output=True, text=True)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    return {
        "command": f"forum route --json {FORUM_TEXT!r}",
        "exit_code": result.returncode,
        "stdout_sha256": sha256_text(result.stdout),
        "stderr_sha256": sha256_text(result.stderr),
        "decided": parsed.get("decided"),
        "confidence": parsed.get("confidence"),
        "needs_escalation": parsed.get("needs_escalation"),
        "top_candidates": parsed.get("candidates", [])[:5],
        "status": "MATCH" if result.returncode == 0 and parsed.get("needs_escalation") is True else "DRIFT",
    }


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "claims_physical_display_calibration", "expected_status": "REJECT", "reject_reason": "no_meter_probe_or_display_mutation"},
        {"fixture_id": "claims_icc_profile_installed", "expected_status": "REJECT", "reject_reason": "icc_profile_installed_false"},
        {"fixture_id": "claims_lut_written", "expected_status": "REJECT", "reject_reason": "lut_written_false"},
        {"fixture_id": "claims_new_color_science_law", "expected_status": "REJECT", "reject_reason": "bounded_software_probe_only"},
        {"fixture_id": "missing_targeted_regression", "expected_status": "REJECT", "reject_reason": "fresh_88_test_slice_required"},
        {"fixture_id": "market_uniqueness_as_fact", "expected_status": "REJECT", "reject_reason": "market_gap_is_inferred"},
        {"fixture_id": "raw_source_payload_required", "expected_status": "REJECT", "reject_reason": "source_refs_only_boundary"},
        {"fixture_id": "unsupported_claim_promoted", "expected_status": "REJECT", "reject_reason": "unsupported_claim_count_nonzero"},
    ]


def compose() -> dict[str, Any]:
    proof_kit = read_json(ROOT / "schemas" / "build-color-calibration-proof-kit-pass-0011.json")
    market_map = read_json(ROOT / "schemas" / "color-calibration-market-map-pass-0011.json")
    test_receipt = run_tests()
    route = run_forum_route()
    refs = source_refs()
    metric_statuses = [row["status"] for row in proof_kit["metrics"]]
    boundary = proof_kit["calibration_boundary"]
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "demo_id": "visual-truth-proof-packet-0081",
        "proof_kit_source": {
            "pass": "0011",
            "schema": proof_kit["schema"],
            "status": proof_kit["status"],
            "metric_count": len(proof_kit["metrics"]),
            "metric_statuses": metric_statuses,
            "failure_labels": proof_kit["failure_labels"],
        },
        "market_map": {
            "pass": "0011",
            "schema": market_map["schema"],
            "row_count": len(market_map["rows"]),
            "gap_statuses": sorted({row["gap_status"] for row in market_map["rows"]}),
        },
        "source_refs": refs,
        "source_ref_count": len(refs),
        "targeted_regression": test_receipt,
        "forum_route": route,
        "calibration_boundary": boundary,
        "proof_packet_layers": [
            "source_refs",
            "software_color_metrics",
            "targeted_regression",
            "market_gap_map",
            "forum_route_receipt",
            "negative_calibration_boundaries",
            "crucible_verdicts",
        ],
        "buyer_brief": {
            "audience": "VFX, color pipeline, scientific visualization, AI review, and display-validation teams",
            "offer": "Visual truth proof packets for bounded color math, transform assumptions, market evidence, and calibration-boundary clarity.",
            "demo_claim": "This demo proves a read-only visual proof-packet surface, not physical display calibration.",
            "primary_risk": "Hardware claims require sensor-backed receipts and display mutation/restore records.",
        },
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0081 refreshes a visual-truth proof-packet surface. It does not calibrate a physical display, install ICC profiles, write LUTs, prove market uniqueness, or promote a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("proof_kit_source", {}).get("status") != "PROOF_KIT_MATCH":
        errors.append("proof_kit")
    if any(status != "PASS" for status in artifact.get("proof_kit_source", {}).get("metric_statuses", [])):
        errors.append("metrics")
    if artifact.get("market_map", {}).get("row_count") != 8:
        errors.append("market_map")
    if artifact.get("source_ref_count") != len(SOURCE_PATHS) or not all(ref["exists"] for ref in artifact.get("source_refs", [])):
        errors.append("source_refs")
    if artifact.get("targeted_regression", {}).get("status") != "MATCH":
        errors.append("targeted_regression")
    if artifact.get("forum_route", {}).get("status") != "MATCH":
        errors.append("forum_route")
    boundary = artifact.get("calibration_boundary", {})
    if any(boundary.get(key) is not False for key in ["hardware_measurement_used", "display_state_mutated", "icc_profile_installed", "lut_written", "physical_calibration_claim"]):
        errors.append("calibration_boundary")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("promotion_boundary")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"out": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
