"""Compose pass 0089 external solver adapter receipt."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import subprocess
import sys
import warnings
from pathlib import Path
from typing import Any

SCHEMA = "ExternalSolverAdapterReceipt/v1"
PASS_ID = "0089"
STATUS_MATCH = "EXTERNAL_SOLVER_ADAPTER_RECEIPT_MATCH"
STATUS_DRIFT = "EXTERNAL_SOLVER_ADAPTER_RECEIPT_DRIFT"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
BASELINE = ROOT / "schemas" / "optimization-branch-comparison-receipt-pass-0088.json"
SEEDS = list(range(8900, 8916))
MAXITER = 128
SOURCE_ANCHORS = [
    {"source_id": "scipy-dual-annealing", "url": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html", "verification_status": "SOURCE_LEAD"},
    {"source_id": "or-tools-mip", "url": "https://developers.google.com/optimization/mip/mip_example", "verification_status": "SOURCE_LEAD"},
    {"source_id": "pass-0088-branch-comparison", "url": "docs/research/dogfood/pass-0088-ledger.md", "verification_status": "LOCAL_BASELINE"},
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


def dependency_receipt(name: str) -> dict[str, Any]:
    spec = importlib.util.find_spec(name)
    if spec is None:
        return {"package": name, "available": False, "version": None, "origin": None}
    module = importlib.import_module(name)
    return {"package": name, "available": True, "version": getattr(module, "__version__", "unknown"), "origin": spec.origin}


def dependency_receipts() -> dict[str, Any]:
    return {
        "python": {"version": sys.version.split()[0], "executable": sys.executable},
        "scipy": dependency_receipt("scipy"),
        "numpy": dependency_receipt("numpy"),
        "ortools": dependency_receipt("ortools"),
    }


def score(bits: list[int], items: list[dict[str, Any]], capacity: int, penalty: int) -> dict[str, Any]:
    value = sum(bit * item["value"] for bit, item in zip(bits, items))
    weight = sum(bit * item["weight"] for bit, item in zip(bits, items))
    violation = max(0, weight - capacity)
    return {
        "bits": bits,
        "selected": [item["id"] for bit, item in zip(bits, items) if bit],
        "value": value,
        "weight": weight,
        "capacity_violation": violation,
        "energy": -value + penalty * violation * violation,
        "feasible": violation == 0,
    }


def rounded_bits(values: list[float]) -> list[int]:
    return [1 if value >= 0.5 else 0 for value in values]


def scipy_adapter(baseline: dict[str, Any], deps: dict[str, Any]) -> dict[str, Any]:
    if not deps["scipy"]["available"]:
        return {"adapter": "scipy.optimize.dual_annealing", "adapter_status": "UNAVAILABLE", "runs": [], "best": None}
    from scipy.optimize import dual_annealing

    problem = baseline["problem"]
    items = problem["items"]
    capacity = int(problem["capacity"])
    penalty = int(problem["penalty"])

    def objective(values: list[float]) -> float:
        return float(score(rounded_bits(list(values)), items, capacity, penalty)["energy"])

    runs = []
    warning_rows = []
    for seed in SEEDS:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = dual_annealing(
                objective,
                [(0.0, 1.0)] * len(items),
                maxiter=MAXITER,
                seed=seed,
                no_local_search=True,
            )
        candidate = score(rounded_bits(list(result.x)), items, capacity, penalty)
        warning_rows.extend({"seed": seed, "category": item.category.__name__, "message": str(item.message)} for item in caught)
        runs.append({
            "seed": seed,
            "maxiter": MAXITER,
            "nit": int(getattr(result, "nit", -1)),
            "nfev": int(getattr(result, "nfev", -1)),
            "fun": float(result.fun),
            "message": str(getattr(result, "message", "")),
            "candidate": candidate,
        })
    best = min((run["candidate"] for run in runs), key=lambda row: (row["energy"], -row["value"], row["weight"]))
    exact_bits = baseline["exact_branch"]["best"]["bits"]
    exact_value = baseline["exact_branch"]["best"]["value"]
    return {
        "adapter": "scipy.optimize.dual_annealing",
        "adapter_status": "MATCH",
        "rounding_policy": "continuous_values_greater_equal_0_5_map_to_binary_1",
        "run_count": len(runs),
        "seed_range": [SEEDS[0], SEEDS[-1]],
        "maxiter": MAXITER,
        "no_local_search": True,
        "runs_sha256": sha256_obj(runs),
        "warning_count": len(warning_rows),
        "warnings_sha256": sha256_obj(warning_rows),
        "runs": runs,
        "best": best,
        "comparison_to_exact": {
            "exact_value_gap": exact_value - best["value"],
            "hit_exact_bits": best["bits"] == exact_bits,
            "exact_hit_count": sum(run["candidate"]["bits"] == exact_bits for run in runs),
            "feasible_run_count": sum(run["candidate"]["feasible"] for run in runs),
            "value_distribution": sorted({run["candidate"]["value"] for run in runs}),
        },
    }


def run_json(command: list[str], timeout: int = 45) -> tuple[int, str, str, dict[str, Any]]:
    result = subprocess.run(command, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    parsed = json.loads(result.stdout) if result.returncode == 0 and result.stdout.strip() else {}
    return result.returncode, result.stdout, result.stderr, parsed


def forum_route() -> dict[str, Any]:
    prompt = "Project Telos pass 0089: external SciPy dual_annealing solver adapter receipt for the exact optimization branch baseline."
    code, stdout, stderr, parsed = run_json(["forum", "route", "--json", prompt], timeout=30)
    return {"status": "MATCH" if code == 0 else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "decided": parsed.get("decided"), "confidence": parsed.get("confidence"), "needs_escalation": parsed.get("needs_escalation"), "top_candidates": parsed.get("candidates", [])[:5]}


def index_receipt() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["index", "context-envelope", "--root", ".", "--budget", "1200", "--json"], timeout=45)
    return {"status": "MATCH" if code == 0 and parsed.get("verification_verdict") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "schema": parsed.get("schema"), "verification_verdict": parsed.get("verification_verdict"), "graph_pack_sha256": parsed.get("recheck", {}).get("graph_pack_sha256"), "source_refs_only": parsed.get("privacy", {}).get("source_refs_only")}


def telos_status() -> dict[str, Any]:
    code, stdout, stderr, parsed = run_json(["node", "demo/status.mjs", "--summary"], timeout=30)
    return {"status": "MATCH" if code == 0 and parsed.get("status") == "MATCH" else "DRIFT", "exit_code": code, "stdout_sha256": sha256_text(stdout), "stderr_sha256": sha256_text(stderr), "tool_version": parsed.get("tool_version"), "tool": parsed.get("tool")}


def negative_fixtures() -> list[dict[str, str]]:
    return [
        {"fixture_id": "missing_dependency_receipt", "expected_status": "REJECT", "reject_reason": "external_adapter_requires_dependency_version"},
        {"fixture_id": "unstamped_seed", "expected_status": "REJECT", "reject_reason": "stochastic_solver_requires_seed_records"},
        {"fixture_id": "missing_exact_baseline", "expected_status": "REJECT", "reject_reason": "adapter_comparison_requires_baseline_or_no_ground_truth_lane"},
        {"fixture_id": "unsealed_runs", "expected_status": "REJECT", "reject_reason": "external_solver_runs_require_digest"},
        {"fixture_id": "solver_superiority_claim", "expected_status": "REJECT", "reject_reason": "single_toy_adapter_does_not_prove_superiority"},
    ]


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    adapter = artifact.get("external_adapter", {})
    comparison = adapter.get("comparison_to_exact", {})
    boundary = artifact.get("promotion_boundary", {})
    if artifact.get("schema") != SCHEMA:
        errors.append("schema")
    if artifact.get("prior_binding", {}).get("source_pass") != "0088":
        errors.append("prior_binding")
    if artifact.get("upstream_research_binding", {}).get("dominant_cluster") != "enterprise_quantum_optimization":
        errors.append("upstream_research_binding")
    if not artifact.get("dependency_receipts", {}).get("scipy", {}).get("available"):
        errors.append("scipy_dependency")
    if adapter.get("adapter_status") != "MATCH" or adapter.get("run_count") != len(SEEDS):
        errors.append("adapter_runs")
    if comparison.get("hit_exact_bits") is not True or comparison.get("exact_value_gap") != 0:
        errors.append("exact_comparison")
    if not adapter.get("runs_sha256"):
        errors.append("runs_digest")
    if any(receipt.get("status") != "MATCH" for receipt in artifact.get("flagship_receipts", {}).values()):
        errors.append("flagship_receipts")
    if any(boundary.get(key) for key in ["solver_superiority_claim", "quantum_hardware_claim", "quantum_advantage_claim", "new_natural_law_claim"]):
        errors.append("promotion_boundary")
    if artifact.get("unsupported_claim_count") != 0 or artifact.get("current_promoted_natural_laws") != []:
        errors.append("unsupported_claims")
    return errors


def compose() -> dict[str, Any]:
    baseline = read_json(BASELINE)
    deps = dependency_receipts()
    adapter = scipy_adapter(baseline, deps)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "pass": PASS_ID,
        "generated_on": "2026-07-01",
        "prior_binding": {"source_pass": "0088", "source_schema": baseline["schema"], "source_seal": baseline["seal"], "exact_value": baseline["exact_branch"]["best"]["value"]},
        "upstream_research_binding": baseline["upstream_research_binding"],
        "source_anchors": SOURCE_ANCHORS,
        "dependency_receipts": deps,
        "external_adapter": adapter,
        "promotion_boundary": {"adapter_receipt_only": True, "solver_superiority_claim": False, "quantum_hardware_claim": False, "quantum_advantage_claim": False, "new_natural_law_claim": False},
        "flagship_receipts": {"forum": forum_route(), "index": index_receipt(), "telos": telos_status()},
        "negative_fixtures": negative_fixtures(),
        "unsupported_claim_count": 0,
        "current_promoted_natural_laws": [],
        "non_promotion_statement": "Pass 0089 records a local SciPy adapter run against a bounded exact baseline; it does not claim solver superiority, quantum advantage, hardware execution, or a natural law.",
    }
    errors = validate_artifact(artifact)
    artifact["validation_errors"] = errors
    artifact["status"] = STATUS_MATCH if not errors else STATUS_DRIFT
    artifact["seal"] = sha256_obj(artifact)
    return artifact


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
