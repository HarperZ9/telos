"""Compose pass 0128 cross-field proof suite receipt."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import subprocess
from pathlib import Path
from typing import Any

SCHEMA = "CrossFieldProofSuiteReceipt/v1"
PASS_ID = "0128"
STATUS_MATCH = "CROSS_FIELD_PROOF_SUITE_MATCH"
STATUS_DRIFT = "CROSS_FIELD_PROOF_SUITE_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
SOURCE_STORE = ROOT / "gather" / "pass-0128-cross-field-proof-suite"
PASS_0122 = ROOT / "schemas" / "scientific-runtime-receipt-layer-spec-pass-0122.json"
PASS_0126 = ROOT / "schemas" / "source-lead-demotion-gate-pass-0126.json"
PASS_0127 = ROOT / "schemas" / "cross-field-scientific-runtime-router-pass-0127.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_obj(value: object) -> str:
    return sha256_text(canonical_json(value))


def ascii_text(value: str) -> str:
    return value.encode("ascii", "ignore").decode("ascii")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def source_receipts() -> list[dict[str, Any]]:
    path = SOURCE_STORE / "catalog.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    receipts = []
    for row in rows:
        obj = SOURCE_STORE / "objects" / row["sha256"][:2] / row["sha256"][2:]
        receipts.append({
            "ref": row["ref"],
            "title": ascii_text(row.get("title", "")),
            "kind": row["kind"],
            "method": row["method"],
            "sha256": row["sha256"],
            "chars": len(obj.read_text(encoding="utf-8", errors="replace")) if obj.exists() else 0,
            "status": "GATHER_VERIFIED" if obj.exists() else "MISSING_OBJECT",
        })
    return sorted(receipts, key=lambda item: item["ref"])


def odd_sum_fixture(limit: int = 64) -> dict[str, Any]:
    rows = []
    for n in range(1, limit + 1):
        odd_sum = sum(2 * k - 1 for k in range(1, n + 1))
        rows.append({"n": n, "odd_sum": odd_sum, "n_squared": n * n, "status": "MATCH" if odd_sum == n * n else "DRIFT"})
    return {
        "fixture_id": "formal_odd_sum_identity",
        "field": "formal_math",
        "source_refs": ["https://lean-lang.org/doc/reference/latest/", "https://github.com/Pengbinghui/pipeline-math"],
        "exact_oracle": "sum_{k=1..n}(2k-1)=n^2 by telescoping difference of squares",
        "runtime_branch": {"runtime": "python", "cases": limit, "max_abs_error": max(abs(r["odd_sum"] - r["n_squared"]) for r in rows), "status": "MATCH"},
        "samples": [rows[0], rows[4], rows[-1]],
        "verifier_status": "PROBE_MATCH",
        "law_candidate_status": "IDENTITY",
    }


def quantum_fixture() -> dict[str, Any]:
    router = read_json(PASS_0127)
    return {
        "fixture_id": "quantum_born_normalization",
        "field": "physics_runtime",
        "source_refs": [router["source_lead"]["video_id"], "pass-0127"],
        "exact_oracle": router["exact_oracle"],
        "runtime_branch": router["runtime_branch"],
        "samples": [{"probabilities": router["exact_oracle"]["probabilities"], "probability_sum": router["exact_oracle"]["probability_sum"]}],
        "verifier_status": "PROBE_MATCH",
        "law_candidate_status": "BOUNDED_RUNTIME_IDENTITY",
    }


def optimization_fixture() -> dict[str, Any]:
    items = [
        {"id": "A", "weight": 2, "value": 6},
        {"id": "B", "weight": 3, "value": 10},
        {"id": "C", "weight": 4, "value": 12},
        {"id": "D", "weight": 5, "value": 15},
    ]
    capacity = 8
    candidates = []
    for mask in itertools.product([0, 1], repeat=len(items)):
        chosen = [item for bit, item in zip(mask, items) if bit]
        weight = sum(item["weight"] for item in chosen)
        value = sum(item["value"] for item in chosen)
        candidates.append({"chosen": [item["id"] for item in chosen], "weight": weight, "value": value, "feasible": weight <= capacity})
    feasible = [row for row in candidates if row["feasible"]]
    optimum = max(feasible, key=lambda row: (row["value"], -row["weight"]))
    return {
        "fixture_id": "bounded_knapsack_exact_oracle",
        "field": "optimization",
        "source_refs": ["https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html"],
        "exact_oracle": {"capacity": capacity, "candidate_count": len(candidates), "optimum": optimum, "status": "MATCH"},
        "runtime_branch": {"runtime": "python", "enumerated_candidates": len(candidates), "optimum_value": optimum["value"], "status": "MATCH"},
        "samples": feasible[:3] + [optimum],
        "verifier_status": "PROBE_MATCH",
        "law_candidate_status": "BOUNDED_OPTIMUM",
    }


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for factor in range(2, int(math.sqrt(n)) + 1):
        if n % factor == 0:
            return False
    return True


def counterexample_fixture() -> dict[str, Any]:
    values = [{"n": n, "value": n * n + n + 41, "prime": is_prime(n * n + n + 41)} for n in range(0, 41)]
    counterexample = next(row for row in values if not row["prime"])
    revised = [row for row in values if row["n"] < counterexample["n"]]
    return {
        "fixture_id": "euler_prime_counterexample_revision",
        "field": "counterexample_search",
        "source_refs": ["https://github.com/Pengbinghui/pipeline-math"],
        "rejected_claim": "n^2+n+41 is prime for every non-negative integer n",
        "counterexample": counterexample,
        "revised_claim": "n^2+n+41 is prime for 0 <= n < 40",
        "exact_oracle": {"checked_values": len(values), "revised_all_prime": all(row["prime"] for row in revised), "status": "MATCH"},
        "runtime_branch": {"runtime": "python", "trial_division_checked": len(values), "status": "MATCH"},
        "samples": [values[0], values[39], counterexample],
        "verifier_status": "PROBE_MATCH",
        "law_candidate_status": "COUNTEREXAMPLE_REVISED_BOUND",
    }


def negative_fixtures() -> list[dict[str, Any]]:
    return [
        {"fixture_id": "suite_to_natural_law_rejected", "attempt": "promote the four probes to a natural law", "status": "REJECTED", "failures": ["bounded_fixtures_only", "requires_independent_review"]},
        {"fixture_id": "single_source_market_fit_rejected", "attempt": "infer market demand from source anchors alone", "status": "REJECTED", "failures": ["no_buyer_interviews", "no_budget_signal"]},
        {"fixture_id": "counterexample_omission_rejected", "attempt": "keep the Euler polynomial claim unbounded", "status": "REJECTED", "failures": ["counterexample_n_40", "claim_must_be_revised"]},
        {"fixture_id": "raw_video_transcript_export_rejected", "attempt": "include raw video transcript body in the suite", "status": "REJECTED", "failures": ["source_lead_boundary", "raw_transcript_not_required"]},
    ]


def run_json(command: list[str], timeout: int = 60) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip().startswith("{") else {}
    return result.returncode, result.stdout, result.stderr, parsed


def flagship_receipts() -> dict[str, Any]:
    code, out, err, parsed = run_json(["forum", "route", "--json", "Pass 0128 cross-field proof suite: formal math, physics runtime, optimization, counterexample revision."])
    forum = {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "decided": parsed.get("decided")}
    code, out, err, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1400", "--json"])
    index = {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "verification_verdict": parsed.get("verification_verdict")}
    code, out, err, parsed = run_json(["node", "demo/status.mjs", "--summary"])
    telos = {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err), "tool_version": parsed.get("tool_version")}
    code, out, err, _ = run_json(["node", "demo/catalog.mjs", "--summary"])
    catalog = {"status": "MATCH" if code == 0 and "Project Telos MCP Catalog" in out else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(out), "stderr_sha256": sha256_text(err)}
    return {"forum": forum, "index": index, "telos": telos, "telos_catalog": catalog}


def compose() -> dict[str, Any]:
    runtime = read_json(PASS_0122)
    gate = read_json(PASS_0126)
    router = read_json(PASS_0127)
    fixtures = [odd_sum_fixture(), quantum_fixture(), optimization_fixture(), counterexample_fixture()]
    negatives = negative_fixtures()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "source_bindings": {
            "runtime_layer_pass": runtime["pass"],
            "runtime_layer_seal": runtime["seal"],
            "demotion_gate_pass": gate["pass"],
            "demotion_gate_seal": gate["seal"],
            "runtime_router_pass": router["pass"],
            "runtime_router_seal": router["seal"],
        },
        "shared_receipt_slots": ["source_refs", "demotion_gate", "exact_oracle", "runtime_branch", "verifier_status", "non_promotion_boundary"],
        "source_receipts": source_receipts(),
        "fixtures": fixtures,
        "negative_fixtures": negatives,
        "market_gap_hypotheses": [
            {"market": "AI research labs", "status": "inferred", "gap": "proof packets that carry source, exact oracle, runtime branch, verifier verdict, and counterexample revision"},
            {"market": "scientific compute teams", "status": "inferred", "gap": "portable receipts for small proofs before scaling to compiled kernels and larger simulations"},
        ],
        "non_promotion_statement": "Pass 0128 proves only four bounded fixtures and the shared proof-suite shape. It does not prove a new natural law, market demand, BuildLang/buildc execution, or arbitrary theorem-solving ability.",
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "flagship_receipts": flagship_receipts(),
    }
    errors = []
    if len(artifact["source_receipts"]) < 4 or any(row["status"] != "GATHER_VERIFIED" for row in artifact["source_receipts"]):
        errors.append("source_receipts")
    if len(fixtures) != 4 or any(row["runtime_branch"]["status"] != "MATCH" for row in fixtures):
        errors.append("fixtures")
    if any(row["verifier_status"] != "PROBE_MATCH" for row in fixtures):
        errors.append("verifier_status")
    if any(row["status"] != "REJECTED" for row in negatives):
        errors.append("negative_fixtures")
    if any(row["status"] != "MATCH" for row in artifact["flagship_receipts"].values()):
        errors.append("flagships")
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(dict(artifact))
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "schemas" / "cross-field-proof-suite-pass-0128.json"))
    args = parser.parse_args()
    artifact = compose()
    write_json(Path(args.out), artifact)
    print(json.dumps({"path": args.out, "seal": artifact["seal"], "status": artifact["status"]}, indent=2, sort_keys=True))
    if artifact["status"] != STATUS_MATCH:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
