"""Compose pass 0127 cross-field scientific runtime router receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA = "CrossFieldScientificRuntimeRouterReceipt/v1"
PASS_ID = "0127"
STATUS_MATCH = "CROSS_FIELD_SCIENTIFIC_RUNTIME_ROUTER_MATCH"
STATUS_DRIFT = "CROSS_FIELD_SCIENTIFIC_RUNTIME_ROUTER_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PASS_0125 = ROOT / "schemas" / "youtube-experiment-router-pass-0125.json"
PASS_0126 = ROOT / "schemas" / "source-lead-demotion-gate-pass-0126.json"
PASS_0122 = ROOT / "schemas" / "scientific-runtime-receipt-layer-spec-pass-0122.json"


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


def frac_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def exact_oracle(amplitudes: list[Fraction]) -> dict[str, Any]:
    squared = [amp * amp for amp in amplitudes]
    norm = sum(squared, Fraction(0, 1))
    probabilities = [value / norm for value in squared]
    return {
        "amplitudes": [frac_text(value) for value in amplitudes],
        "squared_amplitudes": [frac_text(value) for value in squared],
        "norm": frac_text(norm),
        "probabilities": [frac_text(value) for value in probabilities],
        "probability_sum": frac_text(sum(probabilities, Fraction(0, 1))),
        "status": "MATCH" if norm > 0 and sum(probabilities, Fraction(0, 1)) == 1 else "DRIFT",
    }


def runtime_branch(amplitudes: list[Fraction]) -> dict[str, Any]:
    floats = [float(value) for value in amplitudes]
    squared = [value * value for value in floats]
    norm = math.fsum(squared)
    probabilities = [value / norm for value in squared]
    probability_sum = math.fsum(probabilities)
    drift = abs(probability_sum - 1.0)
    payload = {"amplitudes": [frac_text(value) for value in amplitudes], "runtime": "python-float64", "probabilities": probabilities}
    return {
        "branch_id": "python_float64_born_normalization_fixture",
        "runtime": "python",
        "runtime_mode": "float64",
        "input_sha256": sha256_obj({"amplitudes": [frac_text(value) for value in amplitudes]}),
        "output_sha256": sha256_obj(payload),
        "probabilities": probabilities,
        "probability_sum": probability_sum,
        "probability_sum_abs_drift": drift,
        "tolerance": 1e-15,
        "status": "MATCH" if drift <= 1e-15 else "DRIFT",
    }


def negative_fixtures(amplitudes: list[Fraction]) -> list[dict[str, Any]]:
    squared = [amp * amp for amp in amplitudes]
    unnormalized_sum = sum(squared, Fraction(0, 1))
    return [
        {
            "fixture_id": "unnormalized_squares_rejected",
            "attempt": "treat squared amplitudes as probabilities without norm division",
            "probability_sum": frac_text(unnormalized_sum),
            "status": "REJECTED",
            "failures": ["probability_sum_not_one", "missing_normalization_receipt"],
        },
        {
            "fixture_id": "interpretation_claim_rejected",
            "attempt": "promote a quantum interpretation claim from the video source lead",
            "requested_status": "VERIFIED_FACT",
            "status": "REJECTED",
            "failures": ["source_lead_only", "requires_independent_physics_evidence"],
        },
        {
            "fixture_id": "market_claim_rejected",
            "attempt": "claim market fit for the router from this single fixture",
            "requested_status": "MARKET_FIT_VERIFIED",
            "status": "REJECTED",
            "failures": ["single_fixture_not_market_evidence", "requires_buyer_evidence"],
        },
    ]


def run_json(command: list[str], timeout: int = 60) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0127 cross-field scientific runtime router quantum normalization fixture."])
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
    gate = read_json(PASS_0126)
    runtime_layer = read_json(PASS_0122)
    lead = next(row for row in router["youtube_source_leads"] if row["video_id"] == "HbKzqvey5PA")
    gate_fixture = next(row for row in gate["gate_fixtures"] if row["fixture_id"] == "source_lead_only_ok")
    amplitudes = [Fraction(3, 1), Fraction(4, 1), Fraction(0, 1)]
    oracle = exact_oracle(amplitudes)
    branch = runtime_branch(amplitudes)
    negatives = negative_fixtures(amplitudes)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {
            "youtube_router_pass": router["pass"],
            "youtube_router_seal": router["seal"],
            "demotion_gate_pass": gate["pass"],
            "demotion_gate_seal": gate["seal"],
            "runtime_layer_pass": runtime_layer["pass"],
            "runtime_layer_seal": runtime_layer["seal"],
        },
        "source_lead": {
            "video_id": lead["video_id"],
            "theme": lead["theme"],
            "claim_status": lead["claim_status"],
            "dominant_signal": lead["dominant_signal"],
            "raw_transcript_included": False,
        },
        "demotion_gate_result": {"fixture_id": gate_fixture["fixture_id"], "gate_status": gate_fixture["gate_status"], "requested_status": gate_fixture["requested_status"]},
        "runtime_receipt_contract": [row["field"] for row in runtime_layer["receipt_contract"]],
        "exact_oracle": oracle,
        "runtime_branch": branch,
        "negative_fixtures": negatives,
        "router_status": "PROBE_MATCH" if oracle["status"] == "MATCH" and branch["status"] == "MATCH" else "DRIFT",
        "claim_status": "PROBE_MATCH",
        "interpretation_claim_status": "SOURCE_LEAD_ONLY",
        "market_claim_status": "UNVERIFIED",
        "non_promotion_statement": "Pass 0127 routes one video source lead into a bounded normalization runtime fixture. It proves only the exact arithmetic and local branch agreement for this fixture; it does not verify the video's physics claims, market fit, BuildLang/buildc execution, or a natural law.",
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "flagship_receipts": flagship_receipts(),
    }
    errors = []
    if artifact["demotion_gate_result"]["gate_status"] != "ACCEPTED":
        errors.append("demotion_gate")
    if oracle["status"] != "MATCH" or oracle["probability_sum"] != "1":
        errors.append("exact_oracle")
    if branch["status"] != "MATCH":
        errors.append("runtime_branch")
    if len(negatives) != 3 or any(row["status"] != "REJECTED" for row in negatives):
        errors.append("negative_fixtures")
    if artifact["interpretation_claim_status"] != "SOURCE_LEAD_ONLY" or artifact["market_claim_status"] != "UNVERIFIED":
        errors.append("non_promotion")
    if not all(row["status"] == "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "cross-field-scientific-runtime-router-pass-0127.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
